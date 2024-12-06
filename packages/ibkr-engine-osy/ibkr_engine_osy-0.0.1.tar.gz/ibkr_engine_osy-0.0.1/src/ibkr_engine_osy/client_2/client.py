from client_connection_socket import ClientConnectionSocket
from .client_events import ClientEvents
from client_stats import ClientStats
from base_client import BaseClient


class Client(
    ClientConnectionSocket,
    ClientEvents,
    ClientStats,
    BaseClient
):

    def __init__(self, conn: Connection, wrapper, client_id: int = -1):
        super().__init__()
        # logger
        self.looger = Logger(_class=self.__class__)

        self.client_id = client_id
        self.opt_capab = ''
        self.connect_options = b''

    def get_reqeust_id(self) -> int:
        """Get new request ID."""
        if not self.is_ready:
            raise ConnectionError('Not connected')
        new_id = self._req_id_seq
        self._req_id_seq += 1
        return new_id

    def update_reqeust_id(self, min_req_id) -> None:
        """Update the next reqId to be at least ``min_req_id``."""
        self._req_id_seq = max(self._req_id_seq, min_req_id)

    def get_accounts(self) -> List[str]:
        """Get the list of account names that are under management."""
        if not self.is_ready:
            raise ConnectionError('Not connected')
        return self._accounts
