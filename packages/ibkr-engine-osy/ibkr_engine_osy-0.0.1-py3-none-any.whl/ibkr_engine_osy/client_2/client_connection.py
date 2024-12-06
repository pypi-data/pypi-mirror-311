from eventkit import Event
import math
import io

from ibkr_engine.src.ibkr_engine_osy.utils import UNSET_DOUBLE, UNSET_INTEGER, get_loop
from ibkr_engine.src.ibkr_engine_osy.enums import ClientConnectionStatus
from client_connection_socket import ClientConnectionSocket
from ibkr_engine.src.ibkr_engine_osy.connection import Connection
from ibkr_engine.src.ibkr_engine_osy.logger import Logger
from ibkr_engine.src.ibkr_engine_osy.utils import run
from base_client import BaseClient


class ClientConnection(
    ClientConnectionSocket,
    BaseClient
):

    # client connection
    _connection: Connection = None

    # connection stats
    _connect_options: bytes = b''

    # client details
    _client_id: int = -1

    # events
    _api_start: Event = None
    _api_error: Event = None
    _throttle_start: Event = None

    # logger
    _logger: Logger = None

    def set_connect_options(self, connect_options: str) -> None:
        """
        Set additional connect options.

        Args:
            connect_options: Use "+PACEAPI" to use request-pacing built
                into TWS/gateway 974+ (obsolete).
        """
        self._connect_options = connect_options.encode()

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
        self._logger(msg=f'AT Class:{self.__class__.__name__};Func:{self.connect.__name__};Connecting...')
        run(self.connect_async(timeout))

    async def connect_async(self, timeout=2.0) -> None:
        try:
            self._logger(msg=f'Connecting to {self._connection.host}:{self._connection.port} with client_id {self._client_id}...')
            # set connection status
            self._connection_state = ClientConnectionStatus.CONNECTING
            timeout = timeout or None
            # wait for establishing connection
            await self._connection.connect(timeout=timeout)
            self._logger(msg='Connected')

            msg = b'API\0' + self._prefix(
                b'v%d..%d%s' % (
                    self._min_client_version, self._max_client_version,
                    b' ' + self._connect_options if self._connect_options else b''
                ))
            # send connection message (maybe to upgrade to websocket connection)
            self._connection.send_msg(msg)

            # await the `api_start` event to be ready
            await asyncio.wait_for(self._api_start_event, timeout)
            self._logger(msg='API connection ready')

        # handle any exception
        except BaseException as e:
            self.disconnect()
            msg = f'API connection failed: {e!r}'
            # log the error
            self._logger.error(msg=msg)
            # emit the error to the api error event
            self._api_error_event.emit(msg)
            # check if the error of type connection
            if isinstance(e, ConnectionRefusedError):
                self._logger.error(msg='Make sure API port on TWS/IBG is open')
            raise

    def disconnect(self) -> None:
        """Disconnect from IB connection."""
        self._logger(msg='Disconnecting')
        self._connection_state = ClientConnectionStatus.DISCONNECTED
        self._connection.disconnect()
        self.reset()

    def send(self, *fields, make_empty=True):
        """Serialize and send the given fields using the IB socket protocol."""
        self._logger(msg=f'AT Func:{self.send}; preparing the `fields` to be sent')
        self._logger(msg=f'AT Func:{self.send_msg}; fields: {fields}')
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
        self._logger(func=self.send_msg, msg=f'msg: {str(msg)}')

        loop = get_loop()
        t = loop.time()
        times = self._timeQ
        msgs = self._msgQ
        while times and t - times[0] > self._requests_interval:
            times.popleft()

        if msg:
            msgs.append(msg)

        while msgs and (len(times) < self._max_requests or not self._max_requests):
            msg = msgs.popleft()
            self._connection.send_msg(self._prefix(msg.encode()))
            times.append(t)
            self._logger.debug(
                args=msg[:-1].replace('\0', ','),
                func=self.send_msg,
                msg='>>> %s')

        if msgs:
            if not self._is_throttling:
                self._is_throttling = True
                self._throttle_start_event.emit()
                self._logger.debug(func=self.send_msg, msg='Started to throttle requests')
            loop.call_at(
                times[0] + self._requests_interval,
                self.send_msg, None)
        else:
            if self._is_throttling:
                self._is_throttling = False
                self._throttle_end_event.emit()
                self._logger.debug(func=self.send_msg, msg='Stopped to throttle requests')
