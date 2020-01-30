#!/usr/bin/env python
from   aiohttp import web, WSMsgType


def create_notifications_handler(broker):
    async def notifications_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await ws.send_str(f'{msg.data}/answer')
            elif msg.type == WSMsgType.ERROR:
                print(f'notifications websocket closed with exception {ws.exception()}')
            else:
                raise web.HTTPForbidden()
    return notifications_handler
