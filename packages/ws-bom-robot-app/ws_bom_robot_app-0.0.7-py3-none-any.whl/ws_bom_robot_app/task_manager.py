import asyncio, os
from datetime import datetime, timedelta
from enum import Enum
from typing import TypeVar, Optional, Dict, Union
from pydantic import BaseModel, ConfigDict, computed_field
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from ws_bom_robot_app.config import config

T = TypeVar('T')

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

class TaskStatus(BaseModel):
    class TaskStatusEnum(str, Enum):
        pending = "pending"
        completed = "completed"
        failure = "failure"
    task_id: str
    status: TaskStatusEnum
    #result: Optional[Dict[str, Any]] = None
    result: Optional[T] = None
    metadata: TaskMetaData = None
    error: Optional[str] = None

class TaskEntry(BaseModel):
    id: str
    task: Union[asyncio.Task, None] = None
    status: TaskStatus = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = TaskStatus(
            task_id=self.id,
            status=TaskStatus.TaskStatusEnum.pending,
            metadata=TaskMetaData(start_time=datetime.now(), source=str(self.task), pid=os.getpid())
            )
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, TaskEntry] = {}

    def _task_done_callback(self, task_id: str):
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
        return callback

    def create_task(self, coroutine: asyncio.coroutines) -> str:
        _task = asyncio.create_task(coroutine)
        task = TaskEntry(id=str(uuid4()),task=_task)
        task.task.add_done_callback(self._task_done_callback(task.id))
        self.tasks[task.id] = task
        return task.id

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

