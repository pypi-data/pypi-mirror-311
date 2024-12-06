from client_events import ClientEvents
from client_stats import ClientStats
from ibkr_engine.src.ibkr_engine_osy.logger import Logger


class BaseClient(
    ClientEvents,
    ClientStats
):

    # client requests
    _max_requests = 45
    _requests_interval = 1
    # client versions
    _min_client_version = 157
    _max_client_version = 178
    # client id
    _client_id: int = 1

    # logger
    _logger: Logger = None

    @staticmethod
    def _prefix(msg):
        # prefix a message with its length
        return struct.pack('>I', len(msg)) + msg
