import aiohttp
from async_clash.config import *
from constants import *

async def test_configs():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        configs = await get_configs(auth)
        c = Config(configs, auth)
        await c.async_set_mode(ClashMode.Global)
        await c.async_update()
        assert c.mode == ClashMode.Global
        await c.async_set_mode(ClashMode.Rule)
        assert c.mode != ClashMode.Rule

async def test_rules():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        rules = await get_rules(auth)
        for r in rules:
            print(r)
            assert "type" in r.keys()
            assert "payload" in r.keys()
            assert "proxy" in r.keys()