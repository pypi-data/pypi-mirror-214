import asyncio

import pytest

from kaiju_tools.app import Scheduler
from kaiju_tools.fixtures import *


@pytest.mark.asyncio
async def test_scheduler_execution(application):
    counter = 0

    async def _call_task(n=1):
        nonlocal counter
        counter += n

    scheduler = Scheduler(app=application(), refresh_rate=0.1)
    scheduler.schedule_task(_call_task, params={'n': 2}, interval=0.1, name='task_1')
    scheduler.schedule_task(_call_task, interval=0.1, name='task_2')

    async with scheduler:
        await asyncio.sleep(0.15)
        assert counter == 3, 'both tasks must be completed'


@pytest.mark.asyncio
async def test_scheduler_policy_wait(application):
    counter = 0

    async def _call_task():
        await asyncio.sleep(0.1)
        nonlocal counter
        counter += 1

    scheduler = Scheduler(app=application(), refresh_rate=0.1)
    scheduler.schedule_task(_call_task, interval=0.1, policy=scheduler.ExecPolicy.WAIT)

    async with scheduler:
        await asyncio.sleep(0.35)
        assert counter == 1, 'must wait, i.e. only one increment must happen'


@pytest.mark.asyncio
async def test_scheduler_policy_cancel(application):
    counter = 0

    async def _call_task():
        await asyncio.sleep(0.1)
        nonlocal counter
        counter += 1

    scheduler = Scheduler(app=application(), refresh_rate=0.1)
    scheduler.schedule_task(_call_task, interval=0.1, policy=scheduler.ExecPolicy.CANCEL)

    async with scheduler:
        await asyncio.sleep(0.35)
        assert counter == 0, 'no execution must happen due to cancellation'
