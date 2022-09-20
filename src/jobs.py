#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-09-19 15:23:25
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

from typing import Dict
import httpx
from loguru import logger
from src.notifier import notify

class Task:

    def __init__(self, url: str, method: str, headers: Dict=None, payload: Dict=None, title: str=None):
        self.url = url
        self.method = method
        if not headers:
            self.headers = {'Content-Type': 'application/json'}
        else:
            self.headers = headers
        self.payload = payload
        self.title = title
    

    async def execute(self, notify_broker: str=None):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                if self.method == 'GET':
                    response = await client.get(self.url, headers=self.headers)
                elif self.method == 'POST':
                    response = await client.post(self.url, headers=self.headers, data= self.payload)
                if notify_broker:
                    logger.info(f'send notification {self.title}')
                    await notify(notify_broker, self.title, response.text)
        except Exception as e:
            logger.exception(e)
