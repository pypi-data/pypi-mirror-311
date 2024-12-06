from math import floor
import schedule, time, threading
import asyncio
from fastapi import APIRouter
from ws_bom_robot_app.task_manager import task_manager
from ws_bom_robot_app.llm.utils.kb import kb_cleanup_data_file
from ws_bom_robot_app.util import _log
import random

class RecurringJob():
    @staticmethod
    def __add_jitter(interval: int) -> int:
      #delay proportional with interval, min 10, max 100 sec
      jitter: int = max(10, min(100, floor(interval * 0.075)))
      return interval + random.randint(-jitter, jitter)
    def __init__(self, interval: int, job_func, tags: list[str]):
        #add a little jitter by default for better concurrency in case of multiple instances
        self.interval = RecurringJob.__add_jitter(interval)
        self.job_func = job_func
        self.is_coroutine = asyncio.iscoroutinefunction(job_func)
        self.job_func = job_func
        self.tags = tags
    def run(self):
        if self.is_coroutine:
            schedule.every(self.interval).seconds.do(self._run_async_job).tag(*self.tags)
        else:
            schedule.every(self.interval).seconds.do(self.job_func).tag(*self.tags)
    async def _run_async_job(self):
        await self.job_func()

class CronManager:

    _list: dict[str, RecurringJob] = {
      'cleanup-task': RecurringJob(5*60, task_manager.cleanup_task, tags=["cleanup","cleanup-task"]),
      'cleanup-data': RecurringJob(180*60, kb_cleanup_data_file, tags=["cleanup","cleanup-data"]),
    }

    def __init__(self):
        self.jobs: dict[str, RecurringJob] = CronManager._list
        self.__scheduler_is_running = False
    def add_job(self, name:str, job: RecurringJob):
        job = {name: job}
        self.jobs.append(job)
        return job
    def run_pending(self):
        return schedule.run_pending()
    def run_all(self):
        return schedule.run_all()
    def clear(self):
        self.__scheduler_is_running = False
        return schedule.clear()
    def get_jobs(self):
        return schedule.get_jobs()
    def start(self):
        def _target():
            while self.__scheduler_is_running:
                time.sleep(1)
                self.run_pending()
                time.sleep(59)
            _log.info(f"__scheduler_is_running={self.__scheduler_is_running}")
        #clear all jobs
        self.clear()
        #prepare jobs
        for job in self.jobs.values():
            job.run()
        #start scheduler
        if not self.__scheduler_is_running:
            self.__scheduler_is_running = True
            t = threading.Thread(target=_target,args=(),daemon=True)
            t.start()

cron_manager = CronManager()

router = APIRouter(prefix="/api/cron", tags=["cron"])
@router.get("/list")
def _list():
    def __format(job: schedule.Job) -> dict:
        return {
            "job": {'module':job.job_func.__module__,'name':job.job_func.__name__},
            "at": job.at_time,
            "interval": job.interval,
            "last_run": job.last_run,
            "next_run": job.next_run,
            "tags": job.tags}
    _list = cron_manager.get_jobs()
    return [__format(_) for _ in _list]

@router.get("/start")
def _start():
    cron_manager.start()
@router.delete("/stop")
def _stop():
    return {"_": cron_manager.clear()}
@router.get("/run/pending")
def _run_pending():
    return {"_": cron_manager.run_pending()}
@router.get("/run/all")
def _run_all():
    return {"_": cron_manager.run_all()}
