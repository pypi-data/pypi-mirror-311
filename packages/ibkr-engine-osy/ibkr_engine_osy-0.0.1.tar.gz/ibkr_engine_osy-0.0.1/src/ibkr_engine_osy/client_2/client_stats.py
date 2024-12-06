from collections import deque
from typing import Deque
import time

from ibkr_engine.src.ibkr_engine_osy.enums import ClientConnectionStatus
from ibkr_engine.src.ibkr_engine_osy.objects import ConnectionStats


class ClientStats:
    # client connection
    _connection_state: ClientConnectionStatus = ClientConnectionStatus.DISCONNECTED
    # api
    _is_api_ready: bool = False
    # server version
    _server_version: int = 0
    _data: bytes = b''
    # about Ids
    _has_req_id: bool = False
    _req_id_seq: int = 0
    # client accounts
    _accounts: list = []
    _start_time: float = time.time()
    # received deta
    _num_bytes_recv: int = 0
    _num_msg_recv: int = 0
    # throttling
    _is_throttling: bool = False
    # sets
    _msgQ: Deque[str] = deque()
    _timeQ: Deque[float] = deque()

    def reset(self):
        self._connection_state = ClientConnectionStatus.DISCONNECTED
        self._is_api_ready = False
        self._server_version = 0
        self._data = b''
        self._has_req_id = False
        self._req_id_seq = 0
        self._accounts = []
        self._start_time = time.time()
        self._num_bytes_recv = 0
        self._num_msg_recv = 0
        self._is_throttling = False
        self._msgQ: Deque[str] = deque()
        self._timeQ: Deque[float] = deque()

    @property
    def server_version(self) -> int:
        return self._server_version

    @property
    def is_connected(self):
        return self._connection_state == ClientConnectionStatus.CONNECTED

    @property
    def is_ready(self) -> bool:
        """Is the API connection up and running?"""
        return self._is_api_ready

    @property
    def connection_stats(self) -> ConnectionStats:
        """Get statistics about the connection."""
        if not self.is_ready:
            raise ConnectionError('Not connected')
        return ConnectionStats(
            start_time=self._start_time,
            duration=time.time() - self._start_time,
            num_bytes_recv=self._num_bytes_recv,
            num_bytes_sent=self.conn._num_byte_sent,
            num_msg_recv=self._num_msg_recv,
            num_msg_sent=self.conn.num_msgs_sent
        )
