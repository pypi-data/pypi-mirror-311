import asyncio
import aiohttp
import pytest

from async_clash.auth import Auth

HOST = "http://192.168.0.123:9090"
SECRET = "ytf@105105"

async def test_configs():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        resp = await auth.request("get", "configs")
        assert resp.status == 200
        # print("HTTP response JSON content", await resp.text())

async def test_proxies():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        resp = await auth.request("get", "proxies")
        assert resp.status == 200
        # print("HTTP response JSON content", await resp.text())