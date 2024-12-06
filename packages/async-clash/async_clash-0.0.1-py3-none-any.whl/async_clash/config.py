from .auth import Auth
import logging
import json
from enum import StrEnum

class ClashMode(StrEnum):
    Global = "global"
    Rule = "rule"
    Direct = "direct"


async def get_configs(auth: Auth):
    """Get configs raw data"""
    resp = await auth.request("get", "configs")
    resp.raise_for_status()
    return json.loads(await resp.text())


async def get_rules(auth: Auth):
    """Get rules raw data"""
    resp = await auth.request("get", "rules")
    resp.raise_for_status()
    return json.loads(await resp.text())["rules"]

class Config:
    """Class that represents a Config object."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a Config object."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def mode(self) -> ClashMode:
        """Return clash mode."""
        return self._raw_data["mode"]

    async def async_set_mode(self, select: ClashMode) -> str:
        """Change clash mode and return response."""
        resp = await self._auth.request(
            "patch", f"configs", json={"mode": select}
        )
        resp.raise_for_status()
        return await resp.text()

    async def async_update(self):
        """Update the config data."""
        resp = await self._auth.request("get", f"configs")
        resp.raise_for_status()
        self._raw_data = json.loads(await resp.text())