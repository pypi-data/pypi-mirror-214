import json
import httpx
import asyncio
import requests
import platform
import nest_asyncio
from websockets.client import connect, WebSocketClientProtocol
# > Local Imports
from .excetions import NotConnectedError
# > Typing
from typing import Optional, Dict, Any

# ! Initialized
nest_asyncio.apply()

# ! Functions
def generate_friendly_name(
    name: str="Python (v{python_version})",
    platname: str="{system}"
) -> str:
    return (f"{name} On {platname}").format(
        python_version=platform.python_version(),
        system=platform.system()
    )

# ! Main Class
class API:
    def __init__(
        self,
        ws_url: Optional[str]=None
    ) -> None:
        response_node: Dict[str, Any] = requests.get("https://app.revolt.chat/api/").json()
        self.ws_url: str = ws_url or response_node["ws"]
        self.version: str = response_node["version"]
        self.ws: Optional[WebSocketClientProtocol] = None
    
    async def connect(self) -> None:
        self.ws = await connect(self.ws_url)
    
    async def disconnect(self) -> None:
        await self.ws.close()
        self.ws = None
    
    async def connected(self) -> bool:
        return self.ws is not None
    
    async def send(self, data: Dict[str, Any]) -> None:
        if await self.connected():
            return await self.ws.send(json.dumps(data))
        raise NotConnectedError()
    
    async def recv(self) -> Dict[str, Any]:
        if await self.connected():
            return json.loads(await self.ws.recv())
        raise NotConnectedError()
    
