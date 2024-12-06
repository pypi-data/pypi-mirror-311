import inspect
import asyncio, os
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, TypeVar, Optional, Dict, Union, Any
from pydantic import BaseModel, ConfigDict, Field, computed_field
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.base import IdentifiableEntity
from ws_bom_robot_app.llm.utils.webhooks import WebhookNotifier

T = TypeVar('T')

class TaskHeader(BaseModel):
    x_ws_bom_msg_type: Optional[str] = None
    x_ws_bom_webhooks: Optional[str] = None
    model_config = ConfigDict(
        extra='allow'
    )

class TaskMetaData(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    @computed_field
    @property
    def elapsed_time(self) -> Union[timedelta, None]:
        return (datetime.now() if not self.end_time else self.end_time) - self.start_time
    source: Optional[str] = None
    pid: Optional[int] = None
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: str(v)
        }
    )

class TaskStatus(IdentifiableEntity):
    class TaskStatusEnum(str, Enum):
        pending = "pending"
        completed = "completed"
        failure = "failure"
    type: Optional[str] = None
    status: TaskStatusEnum
    result: Optional[T] = None
    metadata: TaskMetaData = None
    error: Optional[str] = None

class TaskEntry(IdentifiableEntity):
    task: Annotated[asyncio.Task, Field(default=None, validate_default=False)] = None
    headers: TaskHeader | None = None
    status: Union[TaskStatus, None] = None
    def _get_coroutine_name(self, coroutine: asyncio.coroutines) -> str:
        if inspect.iscoroutine(coroutine):
            return coroutine.cr_code.co_name
        return "<unknown>"
    def __init__(self, **data):
        #separate task from data to handle asyncio.Task
        task = data.pop('task',None)
        super().__init__(**data)
        #bypass pydantic validation
        object.__setattr__(self, 'task', task)
        #init status
        if not self.status:
          self.status = TaskStatus(
              id=self.id,
              type=self.headers.x_ws_bom_msg_type if self.headers and self.headers.x_ws_bom_msg_type else self._get_coroutine_name(task._coro) if task else None,
              status=TaskStatus.TaskStatusEnum.pending,
              metadata=TaskMetaData(
                 start_time=datetime.now(),
                 source=self._get_coroutine_name(task._coro) if task else None,
                 pid=os.getpid())
              )
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, TaskEntry] = {}

    def _task_done_callback(self, task_id: str, headers: TaskHeader | None = None):
        def callback(task: asyncio.Task):
            if _task := self.tasks.get(task_id):
              try:
                  result = _task.task.result()
                  _task.status.status = TaskStatus.TaskStatusEnum.completed
                  _task.status.result = result
              except Exception as e:
                  _task.status.status = TaskStatus.TaskStatusEnum.failure
                  _task.status.error = str(e)
              finally:
                  _task.status.metadata.end_time = datetime.now()
                  if headers and headers.x_ws_bom_webhooks:
                        asyncio.create_task(
                            WebhookNotifier().notify_webhook(_task.status,headers.x_ws_bom_webhooks)
                            )
        return callback

    def create_task(self, coroutine: asyncio.coroutines, headers: TaskHeader | None = None) -> IdentifiableEntity:
        _task = asyncio.create_task(coroutine)
        task = TaskEntry(
            id=str(uuid4()),
            task=_task,
            headers=headers)
        task.task.add_done_callback(self._task_done_callback(task.id, headers))
        self.tasks[task.id] = task
        return IdentifiableEntity(id=task.id)

    def get_task(self, task_id: str) -> TaskEntry | None:
        if _task := self.tasks.get(task_id):
            return _task
        return None

    def remove_task(self, task_id: str) -> None:
        if task_id in self.tasks:
            del self.tasks[task_id]

    def cleanup_task(self):
        for task_id in [task_id for task_id, task in self.tasks.items()
                        if task.status.status in {TaskStatus.TaskStatusEnum.completed, TaskStatus.TaskStatusEnum.failure}
                        and task.status.metadata.end_time < datetime.now() - timedelta(days=config.robot_task_retention_days)]:
            self.remove_task(task_id)

# global instance
task_manager = TaskManager()

router = APIRouter(prefix="/api/task", tags=["task"])
@router.get("/status/{task_id}", response_model=TaskStatus)
async def _status_task(task_id: str) -> TaskStatus:
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.status
@router.get("/status")
async def _status_task_list():
    _status_task_list = []
    for task in task_manager.tasks.values():
        _task = task_manager.get_task(task.id)
        _status_task_list.append(_task.status)
    return _status_task_list
@router.delete("/status/{task_id}")
async def _remove_task(task_id: str):
    task_manager.remove_task(task_id)
    return {"success":"ok"}
@router.delete("/cleanup")
async def _remove_task_list():
    task_manager.cleanup_task()
    return {"success":"ok"}

