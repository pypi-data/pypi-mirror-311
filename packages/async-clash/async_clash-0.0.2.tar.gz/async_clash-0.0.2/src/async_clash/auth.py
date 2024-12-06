"""Authentication to clash server."""
from aiohttp import ClientSession, ClientResponse, ClientWebSocketResponse


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str, secret: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self.headers = {"authorization": f"Bearer {secret}"}

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""

        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs, headers=self.headers,
        )

    async def websocket(self, path: str, **kwargs):
        """Connect to websocket."""

        return await self.websession.ws_connect(
            f"{self.host}/{path}", headers=self.headers, **kwargs
        )
