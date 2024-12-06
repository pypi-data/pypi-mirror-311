import aiohttp
from aiohttp import ClientResponseError
from async_clash.proxy import *
import random
import pytest
from constants import *

OUTBOUNDS = ['Fallback', 'Direct', 'Reject', 'Selector', 'URLTest', 'DNS', 'Shadowsocks',
             'Trojan', 'VMess', 'Hysteria', 'Hysteria2', 'VLESS', 'SSH', 'TUIC', 'Tor', 'SSH']


async def test_get_proxy():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET)
        proxies = await get_proxies(auth)
        for k, v in proxies.items():
            assert k == v['name']
            p = Proxy(v, auth)
            assert p.type in OUTBOUNDS
            assert isinstance(p.udp, bool)
            if p.type == 'Selector':
                assert p.now in p.all
                select = random.choice(p.all)
                await p.async_select(select)
                await p.async_update()
                assert p.now == select


async def test_proxy_exp():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, HOST, SECRET+"wrong")
        with pytest.raises(ClientResponseError) as excinfo:
            await get_proxies(auth)
        assert excinfo.value.code == 401
        assert excinfo.value.message == "Unauthorized"

        auth = Auth(session, HOST, SECRET)
        proxies = await get_proxies(auth)
        for k, v in proxies.items():
            p = Proxy(v, auth)
            if p.type == 'Selector':
                with pytest.raises(ClientResponseError) as excinfo:
                    assert (await p.async_select('not a proxy')) == "Selector update error: not found"
                assert excinfo.value.code == 400
            if p.type == 'URLTest':
                with pytest.raises(ClientResponseError) as excinfo:
                    assert (await p.async_select(p.now)) == "Must be a Selector"
                assert excinfo.value.code == 400
