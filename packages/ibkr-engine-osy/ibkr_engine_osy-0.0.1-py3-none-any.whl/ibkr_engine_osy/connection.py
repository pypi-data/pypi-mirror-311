"""Event-driven socket connection."""

from asyncio.events import AbstractEventLoop
from typing import Optional
import asyncio

from .logger import Logger
from eventkit import Event
from .utils import run, get_loop


class BaseConnection(asyncio.Protocol):
    """
    Event-driven socket connection.

    Events:
        * ``has_data`` (data: bytes):
          Emits the received socket data.
        * ``disconnected`` (msg: str):
          Is emitted on socket disconnect, with an error message in case
          of error, or an empty string in case of a normal disconnect.
    """

    def __init__(self):
        self.logger = Logger(class_name=self.__class__.__name__)
        self.logger(msg='initialize a new Connection.')
        self._data_received_event = Event('hasData')
        self._disconnected_event = Event('disconnected')

        self.transport = None
        self._num_byte_sent = 0
        self.num_msgs_sent = 0

        self.reset()

    def reset(self):
        self.logger(msg='all Connection params rested')
        self.transport = None
        self._num_byte_sent = 0
        self.num_msgs_sent = 0

    async def initialize_async_socket_connection(self, host: str, port: int, timeout: Optional[float] = 2.0):
        self.logger(msg=f'AT Class:{self.__class__.__name__};Func:{self.initialize_async_socket_connection.__name__};Async Connecting at host:{host} ; port:{port}')
        if self.transport:
            # wait until a previous connection is finished closing
            self.disconnect()
            await self.disconnected
        # reset all params
        self.reset()
        # get current event loop
        loop = get_loop()
        # create a new connection
        self.transport, _ = await loop.create_connection(
            protocol_factory=lambda: self,
            host=host,
            port=port
        )

    def connection_lost(self, exc):
        self.transport = None
        msg = str(exc) if exc else ''
        self._disconnected_event.emit(msg)

    def data_received(self, data):
        self.logger(func=self.data_received, msg=f'data received: {data.decode()}')
        self._data_received_event.emit(data)


class Connection(BaseConnection):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host: str = host
        self.port: int = port

    async def connect(self, timeout: Optional[float] = 2.0):
        self.logger(msg='Connecting...')
        await self.initialize_async_socket_connection(
            host=self.host,
            port=self.port,
            timeout=timeout
        )

    def disconnect(self):
        self.logger(func=self.disconnect, msg='Disconnecting...')
        if self.transport:
            self.transport.write_eof()
            self.transport.close()

    def send_msg(self, msg):
        if self.transport:
            self.transport.write(msg)
            self._num_byte_sent += len(msg)
            self.num_msgs_sent += 1

    @property
    def is_connected(self):
        return self.transport is not None
