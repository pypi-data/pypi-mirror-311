import asyncio
from enum import IntEnum
from typing import Any, Dict, Optional, Union

import aiohttp
import websockets
from pydantic import BaseModel

from .emitter import EnhancedEventEmitter
from .log import base_logger
from .proto.client import request_pb2, response_pb2

logger = base_logger.getChild("Socket")


class Geolocation(BaseModel):
    region: str
    country: str


class ConnectionState:
    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class SocketCloseCode(IntEnum):
    NORMAL_CLOSURE = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    NO_STATUS_RECEIVED = 1005
    ABNORMAL_CLOSURE = 1006
    INVALID_FRAME_PAYLOAD_DATA = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MISSING_EXTENSION = 1010
    INTERNAL_ERROR = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013
    BAD_GATEWAY = 1014
    TLS_HANDSHAKE = 1015
    ROOM_CLOSED = 4000
    CONNECTION_ERROR = 4001
    CONNECTION_EXPIRED = 4002
    ROOM_ENTRY_DENIED = 4003
    KICKED = 4004
    MAX_PEERS_REACHED = 4005
    ROOM_EXPIRED = 4006
    BROWSER_TAB_CLOSE = 4007


SocketCloseReason: Dict[SocketCloseCode, str] = {
    SocketCloseCode.ROOM_CLOSED: "ROOM_CLOSED",
    SocketCloseCode.ABNORMAL_CLOSURE: "ABNORMAL_CLOSURE",
    SocketCloseCode.NORMAL_CLOSURE: "NORMAL_CLOSURE",
    SocketCloseCode.BROWSER_TAB_CLOSE: "BROWSER_TAB_CLOSE",
    SocketCloseCode.GOING_AWAY: "GOING_AWAY",
    SocketCloseCode.CONNECTION_ERROR: "CONNECTION_ERROR",
    SocketCloseCode.CONNECTION_EXPIRED: "CONNECTION_EXPIRED",
    SocketCloseCode.ROOM_ENTRY_DENIED: "ROOM_ENTRY_DENIED",
    SocketCloseCode.KICKED: "KICKED",
    SocketCloseCode.MAX_PEERS_REACHED: "MAX_PEERS_REACHED",
    SocketCloseCode.ROOM_EXPIRED: "ROOM_EXPIRED",
}


class Socket(EnhancedEventEmitter):
    def __init__(self):
        super(Socket, self).__init__()

        logger.info("[constructor] Socket, initializing")

        self.connection_state = ConnectionState.IDLE
        # self.__apira_url = "http://localhost:8000/api/v1/getSushiUrl"
        self.__apira_url = "https://apira.huddle01.media/api/v1/getSushiUrl"

        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.token: Optional[str] = None
        self.geo_data: Optional[Geolocation] = None
        self.endpoint: Optional[str] = None

        self.__reconnect_attempts = 0
        self.__max_reconnect_attempts = 5
        self.__reconnect_delay = 5

    async def __get_geo_data(self):
        """Get the geolocation data"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://shinigami.huddle01.com/api/get-geolocation"
                ) as reponse:
                    data = await reponse.json()
                    self.geo_data = Geolocation(
                        region=data["globalRegion"], country=data["country"]
                    )
                    return self.geo_data

        except Exception as e:
            logger.error(f"Error getting socket URL: {e}")
            raise

    async def __get_socket_url(self, token: str) -> str:
        """Get the socket URL"""
        try:
            if not token:
                raise ValueError("Token or geo data is missing")

            await self.__get_geo_data()

            if not self.geo_data:
                raise ValueError("Geo data is missing")

            headers = {"authorization": f"Bearer {token}"}

            async with aiohttp.ClientSession() as session:
                async with session.get(self.__apira_url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(
                            f"Failed to get socket URL. Status: {response.status}"
                        )

                    data = await response.json()

                    socket_url = data["url"]

                    logger.info(f"Socket URL: {socket_url}")

                    if not isinstance(socket_url, str) or not socket_url:
                        raise Exception("Socket URL is missing")

                    socket_url = socket_url.replace("https://", "wss://").replace(
                        "http://", "ws://"
                    )
                    self.endpoint = f"{socket_url}/ws?token={token}&region={self.geo_data.region}&country={self.geo_data.country}"

                    return self.endpoint

        except Exception as e:
            logger.error(f"Error getting socket URL: {e}")

            raise

    async def connect(self, token: str):
        self.token = token
        self.connection_state = ConnectionState.CONNECTING

        try:
            endpoint = await self.__get_socket_url(self.token)

            self.ws = await websockets.connect(endpoint, logger=logger)

            self.connection_state = ConnectionState.CONNECTED

            self.__reconnect_attempts = 0

            asyncio.create_task(self._listen())

            logger.info("Connected to socket")
        except Exception as e:
            logger.error(f"Error connecting to socket: {e}")
            self.connection_state = ConnectionState.DISCONNECTED

            if self.ws:
                await self.ws.close()
            raise

    async def _listen(self):
        """
        Listen to the socket for incoming messages
        and handle the context for the message recieved
        on the socket
        """
        try:
            if self.ws is None:
                raise ValueError("WebSocket is not connected")

            async for message in self.ws:
                await self._handle_message(message)

        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")

        except Exception as e:
            logger.error(f"Error listening to socket: {e}")

        finally:
            self.connection_state = ConnectionState.DISCONNECTED
            self.emit("disconnected")

    async def _handle_message(self, message: Union[bytes, str]):
        """
        Handle the incoming message from the socket
        and emit the appropriate event based on the message type
        """
        if isinstance(message, str):
            raise ValueError("Message should be bytes")

        resp = response_pb2.Response()

        resp.ParseFromString(message)

        response_type = resp.WhichOneof("Response")

        logger.info(f"New Socket Message received {response_type}")

        if response_type:
            self.emit(response_type, getattr(resp, response_type))

        else:
            logger.info(f"Unknown response type: {response_type}")

            self.emit("message", message)

    async def request(self, event: str, data: Any):  # TODO: Add type hint for data
        """
        Request sends the data over the socket connection attached to the requested event
        """
        if self.ws:
            logger.info(f"Publishing event: {event}")

            req = request_pb2.Request(**{event: data})

            binaryData = req.SerializeToString()

            await self.ws.send(binaryData)
        else:
            logger.error("Socket is not connected")

    async def close(self, code: SocketCloseCode):
        """Close the socket connection"""

        logger.info(f"Closing socket connection with code: {code}")

        close_reason = SocketCloseReason.get(code, "ABNORMAL_CLOSURE")

        if self.ws:
            await self.ws.close(code=code, reason=close_reason)

        logger.info("Closing socket connection")
        self.connection_state = ConnectionState.DISCONNECTED
