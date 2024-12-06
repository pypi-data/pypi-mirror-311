from eventkit import Event


class ClientEvents:
    events = (
        'api_start',
        'api_end',
        'api_error',
        'throttle_start',
        'throttle_end'
    )

    _api_start_event = Event('api_start')
    _api_end_event = Event('api_end')
    _api_error_event = Event('api_error')
    _throttle_start_event = Event('throttle_start')
    _throttle_end_event = Event('throttle_end')
