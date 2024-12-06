"""Socket client for communicating with Interactive Brokers."""

from typing import Deque, List, Optional
from collections import deque
import asyncio
import logging
import struct
import math
import time
import io

from eventkit import Event

from .utils import UNSET_DOUBLE, UNSET_INTEGER, dataclassAsTuple, get_loop, run
from .enums import ClientConnectionStatus
from .objects import ConnectionStats
from .connection import Connection
from .decoder import Decoder
from .logger import Logger


class Client:
    """
    Replacement for ``ibapi.client.EClient`` that uses asyncio.

    The client is fully asynchronous and has its own
    event-driven networking code that replaces the
    networking code of the standard EClient.
    It also replaces the infinite loop of ``EClient.run()``
    with the asyncio event loop. It can be used as a drop-in
    replacement for the standard EClient as provided by IBAPI.

    Compared to the standard EClient this client has the following
    additional features:

    * ``client.connect()`` will block until the client is ready to
      serve requests; It is not necessary to wait for ``nextValidId``
      to start requests as the client has already done that.
      The reqId is directly available with :py:meth:`.getReqId()`.

    * ``client.connectAsync()`` is a coroutine for connecting asynchronously.

    * When blocking, ``client.connect()`` can be made to time out with
      the timeout parameter (default 2 seconds).

    * Optional ``wrapper.priceSizeTick(reqId, tickType, price, size)`` that
      combines price and size instead of the two wrapper methods
      priceTick and sizeTick.

    * Automatic request throttling.

    * Optional ``wrapper.tcpDataArrived()`` method;
      If the wrapper has this method it is invoked directly after
      a network packet has arrived.
      A possible use is to timestamp all data in the packet with
      the exact same time.

    * Optional ``wrapper.tcpDataProcessed()`` method;
      If the wrapper has this method it is invoked after the
      network packet's data has been handled.
      A possible use is to write or evaluate the newly arrived data in
      one batch instead of item by item.

    Parameters:
      MaxRequests (int):
        Throttle the number of requests to ``MaxRequests`` per
        ``RequestsInterval`` seconds. Set to 0 to disable throttling.
      RequestsInterval (float):
        Time interval (in seconds) for request throttling.
      MinClientVersion (int):
        Client protocol version.
      MaxClientVersion (int):
        Client protocol version.

    Events:
      * ``apiStart`` ()
      * ``apiEnd`` ()
      * ``apiError`` (errorMsg: str)
      * ``throttleStart`` ()
      * ``throttleEnd`` ()
    """

    events = (
        'api_start',
        'api_end',
        'api_error',
        'throttle_start',
        'throttle_end'
    )

    # requests
    max_requests = 45
    requests_interval = 1
    # client versions
    min_client_version = 157
    max_client_version = 178

    def __init__(self, conn: Connection, wrapper, client_id: int = -1):
        self.wrapper = wrapper
        self.decoder = Decoder(wrapper, 0)
        self.api_start = Event('apiStart')
        self.api_end = Event('apiEnd')
        self.api_error = Event('apiError')
        self.throttle_start = Event('throttleStart')
        self.throttle_end = Event('throttleEnd')
        self._logger = logging.getLogger('ib_insync.client')
        self.internal_logger = Logger(class_name=self.__class__.__name__)

        self.conn: Connection = conn
        self.conn._data_received_event += self._on_socket_has_data
        self.conn._disconnected_event += self._on_socket_disconnected

        # extra optional wrapper methods
        self._price_size_tick = getattr(wrapper, 'priceSizeTick', None)
        self._tcp_data_arrived = getattr(wrapper, 'tcpDataArrived', None)
        self._tcp_data_processed = getattr(wrapper, 'tcpDataProcessed', None)

        self.client_id = client_id
        self.opt_capab = ''
        self.connect_options = b''

        self.connection_state = ClientConnectionStatus.DISCONNECTED
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
        self.reset()

    def reset(self):
        self.connection_state = ClientConnectionStatus.DISCONNECTED
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

    def get_req_id(self) -> int:
        """Get new request ID."""
        if not self.is_ready:
            raise ConnectionError('Not connected')
        new_id = self._req_id_seq
        self._req_id_seq += 1
        return new_id

    def update_req_id(self, min_req_id) -> None:
        """Update the next reqId to be at least ``min_req_id``."""
        self._req_id_seq = max(self._req_id_seq, min_req_id)

    def get_accounts(self) -> List[str]:
        """Get the list of account names that are under management."""
        if not self.is_ready:
            raise ConnectionError('Not connected')
        return self._accounts

    def set_connect_options(self, connect_options: str) -> None:
        """
        Set additional connect options.

        Args:
            connect_options: Use "+PACEAPI" to use request-pacing built
                into TWS/gateway 974+ (obsolete).
        """
        self.connect_options = connect_options.encode()

    def connect(self, host: str, port: int, client_id: int, timeout: Optional[float] = 2.0) -> None:
        """
        Connect to a running TWS or IB gateway application.

        Args:
            host: Host name or IP address.
            port: Port number.
            client_id: ID number to use for this client; must be unique per
                connection.
            timeout: If establishing the connection takes longer than
                ``timeout`` seconds then the ``asyncio.TimeoutError`` exception
                is raised. Set to 0 to disable timeout.
        """
        self.internal_logger(msg=f'AT Class:{self.__class__.__name__};Func:{self.connect.__name__};Connecting...')
        run(self.connect_async(client_id, timeout))

    async def connect_async(self, client_id, timeout=2.0) -> None:
        try:
            self.internal_logger(msg=f'Connecting to {self.conn.host}:{self.conn.port} with client_id {client_id}...')
            # insure parse `client_id` to int
            self.client_id = int(client_id)
            # set connection status
            self.connection_state = ClientConnectionStatus.CONNECTING
            timeout = timeout or None
            # wait for establishing connection
            await self.conn.connect(timeout=timeout)
            self.internal_logger(msg='Connected')

            msg = b'API\0' + self._prefix(
                b'v%d..%d%s' % (
                    self.min_client_version, self.max_client_version,
                    b' ' + self.connect_options if self.connect_options else b''
                ))
            # send connection message (maybe to upgrade to websocket connection)
            self.conn.send_msg(msg)
            # await the `api_start` event to be ready
            await asyncio.wait_for(self.api_start, timeout)
            self.internal_logger(msg='API connection ready')
        # handle any exception
        except BaseException as e:
            self.disconnect()
            msg = f'API connection failed: {e!r}'
            # log the error
            self.internal_logger.error(msg=msg)
            # emit the error to the api error event
            self.api_error.emit(msg)
            # check if the error of type connection
            if isinstance(e, ConnectionRefusedError):
                self.internal_logger.error(msg='Make sure API port on TWS/IBG is open')
            raise

    def disconnect(self) -> None:
        """Disconnect from IB connection."""
        self.internal_logger(msg='Disconnecting')
        self.connection_state = ClientConnectionStatus.DISCONNECTED
        self.conn.disconnect()
        self.reset()

    def send(self, *fields, make_empty=True):
        """Serialize and send the given fields using the IB socket protocol."""
        self.internal_logger(msg=f'AT Func:{self.send.__name__}; preparing the `fields` to be sent')
        self.internal_logger(msg=f'AT Func:{self.send_msg.__name__}; fields: {fields}')
        if not self.is_connected:
            raise ConnectionError('Not connected')

        msg: StringIO = io.StringIO()
        empty = (None, UNSET_INTEGER, UNSET_DOUBLE) if make_empty else (None,)
        for field in fields:
            typ = type(field)
            if field in empty:
                s = ''
            elif typ is str:
                s = field
            elif type is int:
                s = str(field)
            elif typ is float:
                s = 'Infinite' if field == math.inf else str(field)
            elif typ is bool:
                s = '1' if field else '0'
            elif typ is list:
                # list of TagValue
                s = ''.join(f'{v.tag}={v.value};' for v in field)
            elif isinstance(field, Contract):
                c = field
                s = '\0'.join(str(f) for f in (
                    c.con_id, c.symbol, c.sec_type,
                    c.lastTradeDateOrContractMonth, c.strike,
                    c.right, c.multiplier, c.exchange,
                    c.primaryExchange, c.currency,
                    c.localSymbol, c.trading_class))
            else:
                s = str(field)
            msg.write(s)
            msg.write('\0')
        self.send_msg(msg.getvalue())

    def send_msg(self, msg: str):
        self.internal_logger(func=self.send_msg, msg=f'msg: {str(msg)}')

        loop = get_loop()
        t = loop.time()
        times = self._timeQ
        msgs = self._msgQ
        while times and t - times[0] > self.requests_interval:
            times.popleft()

        if msg:
            msgs.append(msg)

        while msgs and (len(times) < self.max_requests or not self.max_requests):
            msg = msgs.popleft()
            self.conn.sendMsg(self._prefix(msg.encode()))
            times.append(t)
            self.internal_logger.debug(
                args=msg[:-1].replace('\0', ','),
                func=self.send_msg,
                msg='>>> %s')

        if msgs:
            if not self._is_throttling:
                self._is_throttling = True
                self.throttle_start.emit()
                self.internal_logger.debug(func=self.send_msg, msg='Started to throttle requests')
            loop.call_at(
                times[0] + self.requests_interval,
                self.send_msg, None)
        else:
            if self._is_throttling:
                self._is_throttling = False
                self.throttle_end.emit()
                self.internal_logger.debug(func=self.send_msg, msg='Stopped to throttle requests')

    @staticmethod
    def _prefix(msg):
        # prefix a message with its length
        return struct.pack('>I', len(msg)) + msg

    def _on_socket_has_data(self, data):
        debug = self._logger.isEnabledFor(logging.DEBUG)

        if self._tcp_data_arrived:
            self._tcp_data_arrived()

        self._data += data
        self._num_bytes_recv += len(data)

        while True:
            if len(self._data) <= 4:
                break

            # 4 byte prefix tells the message length
            msg_end = 4 + struct.unpack('>I', self._data[:4])[0]
            if len(self._data) < msg_end:
                # insufficient data for now
                break

            msg = self._data[4:msg_end].decode(errors='backslashreplace')
            self._data = self._data[msg_end:]
            fields = msg.split('\0')
            fields.pop()  # pop off last empty element
            self._num_msg_recv += 1

            if debug:
                self._logger.debug('<<< %s', ','.join(fields))

            if not self._server_version and len(fields) == 2:
                # this concludes the handshake
                version, _connTime = fields
                self._server_version = int(version)
                if self._server_version < self.min_client_version:
                    self._on_socket_disconnected('TWS/gateway version must be >= 972')
                    return
                self.decoder.server_version = self._server_version
                self.connection_state = ClientConnectionStatus.CONNECTED
                self.api_start()
                self.wrapper.connectAck()
                self._logger.info(f'Logged on to server version {self._server_version}')
            else:
                if not self._is_api_ready:
                    # snoop for nextValidId and managedAccounts response,
                    # when both are in then the client is ready
                    msg_id = int(fields[0])
                    if msg_id == 9:
                        _, _, validId = fields
                        self.update_req_id(int(validId))
                        self._has_req_id = True
                    elif msg_id == 15:
                        _, _, accts = fields
                        self._accounts = [a for a in accts.split(',') if a]
                    if self._has_req_id and self._accounts:
                        self._is_api_ready = True
                        self.api_start.emit()

                # decode and handle the message
                self.decoder.interpret(fields)

        if self._tcp_data_processed:
            self._tcp_data_processed()

    def _on_socket_disconnected(self, msg):
        was_ready = self.is_ready
        if not self.is_connected:
            self._logger.info('Disconnected.')
        elif not msg:
            msg = 'Peer closed connection.'
            if not was_ready:
                msg += f' client_id {self.client_id} already in use?'
        if msg:
            self._logger.error(msg)
            self.api_error.emit(msg)
        self.wrapper.setEventsDone()
        if was_ready:
            self.wrapper.connectionClosed()
        self.reset()
        if was_ready:
            self.api_end.emit()

    @property
    def server_version(self) -> int:
        return self._server_version

    @property
    def is_connected(self):
        return self.connection_state == ClientConnectionStatus.CONNECTED

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
