"""API Placeholder for clash."""

from .auth import Auth
import logging
import json
# from websockets.asyncio.client import connect, ClientConnection

_LOGGER = logging.getLogger(__name__)


async def get_proxies(auth: Auth):
    """Get all proxies raw data."""
    resp = await auth.request("get", "proxies")
    resp.raise_for_status()
    return json.loads(await resp.text())["proxies"]


class Proxy:
    """Class that represents a Proxy object."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a proxy object."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def type(self) -> str:
        """Return the type of the proxy."""
        return self._raw_data["type"]

    @property
    def name(self) -> str:
        """Return the name of the proxy."""
        return self._raw_data["name"]

    @property
    def udp(self) -> bool:
        """Return the proxy transfer udp or not."""
        return self._raw_data["udp"]

    @property
    def history(self) -> list:
        """Return the history of the proxy."""
        return self._raw_data["history"]

    @property
    def now(self) -> str | None:
        """Return current selector of the proxy."""
        return self._raw_data["now"]

    @property
    def all(self) -> list[str]:
        """Return all selectors of the proxy."""
        return self._raw_data["all"]

    async def async_select(self, select: str) -> str:
        """Select the proxy outbound and return response."""
        resp = await self._auth.request(
            "put", f"proxies/{self.name}", json={"name": select}
        )
        resp.raise_for_status()
        return await resp.text()

    async def async_update(self):
        """Update the proxy data."""
        resp = await self._auth.request("get", f"proxies/{self.name}")
        resp.raise_for_status()
        self._raw_data = json.loads(await resp.text())