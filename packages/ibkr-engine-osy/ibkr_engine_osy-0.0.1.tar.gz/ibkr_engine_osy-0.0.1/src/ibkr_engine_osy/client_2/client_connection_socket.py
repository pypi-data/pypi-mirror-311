from ibkr_engine.src.ibkr_engine_osy.connection import Connection
from ibkr_engine.src.ibkr_engine_osy.wrapper import Wrapper
from base_client import BaseClient


class ClientConnectionSocket(BaseClient):
    _client_connection: Connection = None
    _socket_wrapper: Wrapper = None

    # extra optional wrapper methods
    _price_size_tick = getattr(_socket_wrapper, 'priceSizeTick', None)
    _tcp_data_arrived = getattr(_socket_wrapper, 'tcpDataArrived', None)
    _tcp_data_processed = getattr(_socket_wrapper, 'tcpDataProcessed', None)

    def wrap_events(self) -> None:
        if self._client_connection:
            self._client_connection._data_received_event += self._on_socket_has_data
            self._client_connection._disconnected_event += self._on_socket_disconnected

    def _on_socket_has_data(self, data) -> None:
        self._socket_wrapper.tcpDataArrived()

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

            if not self._server_version and len(fields) == 2:
                # this concludes the handshake
                version, _connTime = fields
                self._server_version = int(version)
                if self._server_version < self.min_client_version:
                    self._on_socket_disconnected('TWS/gateway version must be >= 972')
                    return
                self.decoder.server_version = self._server_version
                self.connection_state = ClientConnectionStatus.CONNECTED
                self._api_start_event()
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
                        self._api_start_event.emit()

                # decode and handle the message
                self.decoder.interpret(fields)
        self._socket_wrapper.tcpDataProcessed()

    def _on_socket_disconnected(self, msg) -> None:
        was_ready: bool = self.is_ready
        if not self.is_connected:
            self._logger.info(msg='Disconnected.')
        elif not msg:
            msg = 'Peer closed connection.'
            if not was_ready:
                msg += f' client_id {self._client_id} already in use?'
        if msg:
            self._logger.error(msg)
            self._api_error_event.emit(msg)
        self._socket_wrapper.setEventsDone()
        if was_ready:
            self._socket_wrapper.connectionClosed()
        self.reset()
        if was_ready:
            self._api_end_event.emit()
