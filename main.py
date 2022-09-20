#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-09-19 15:33:21
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import ast
import asyncio
import json
import random
import sqlite3
import time

import trio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from src.jobs import Task


async def main():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM TASKS")
        records = res.fetchall()
    logger.info(f'get {len(records)} records')
    for r in records:
        time.sleep(random.randint(0, 1000))
        if r[4]:
            task = Task(r[1], r[2], json.loads(r[3]), r[4], title=r[5])
        else:
            task = Task(r[1], r[2], json.loads(r[3]), title=r[5])
        await task.execute('bark')
    logger.info('complete job')

if __name__ == "__main__":
    # trio.run(main)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, "cron", hour=3, max_instances=1, misfire_grace_time=300)
    scheduler.start()
    asyncio.get_event_loop().run_forever()


