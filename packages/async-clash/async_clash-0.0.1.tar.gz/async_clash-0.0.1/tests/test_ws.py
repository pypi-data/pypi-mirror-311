import aiohttp
import time
from async_clash.auth import *
import re

HOST = "http://192.168.0.123:9090"
SECRET = "ytf@105105"

async def test_traffic():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        ws = await auth.websocket("traffic")
        async def callback(msg):
            print(msg)
            assert re.match(r'^{"up":\d*,"down":\d*}$', msg)
        count = 0
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await callback(msg.data)                
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
            count += 1
            if (count > 5):
                break

async def test_logs():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        ws = await auth.websocket("logs")
        async def callback(msg):
            print(msg)
            assert re.match(r'^{"type":".*","payload":".*"}$', msg)
        count = 0
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await callback(msg.data)                
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
            count += 1
            if (count > 5):
                break