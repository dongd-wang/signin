#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-09-19 15:42:41
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
import httpx
import json

class BarkNotification:
    def __init__(self, title, msg):
        self.title = title
        self.msg = msg
        self.bark_url = os.environ.get('BARK_URL')
        self.bark_token = os.environ.get('BARK_TOKEN')
    
    async def send(self):
        async with httpx.AsyncClient(timeout=10) as client:
            url = self.bark_url + '/push'
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            payload = {
                    "title": self.title,
                    "body": json.dumps(json.loads(self.msg), ensure_ascii=False),
                    "device_key": self.bark_token,
                    "badge": 1,
                    "sound": "minuet.caf",
                    "icon": "https://day.app/assets/images/avatar.jpg",
                    "group": "签到",
                    }
            await client.post(url, headers=headers, data=json.dumps(payload))


async def notify(notify_broker:str = None, title: str=None, msg: str=None):
    if not notify_broker or notify_broker == 'bark':
        notifier = BarkNotification(title, msg)
        await notifier.send()
    else:
        raise NotImplementedError('other notifier not implemented')