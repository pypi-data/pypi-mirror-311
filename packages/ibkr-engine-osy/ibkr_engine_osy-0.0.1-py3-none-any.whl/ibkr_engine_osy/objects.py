"""Object hierarchy."""

from dataclasses import dataclass, field
from datetime import date as date_, datetime
from typing import List, NamedTuple, Optional, Union

from eventkit import Event

from .contracts import Contract, ScanData, TagValue
from .utils import EPOCH, UNSET_DOUBLE, UNSET_INTEGER

nan = float('nan')


@dataclass
class ScannerSubscription:
    number_of_rows: int = -1
    instrument: str = ''
    location_code: str = ''
    scan_code: str = ''
    above_price: float = UNSET_DOUBLE
    below_price: float = UNSET_DOUBLE
    above_volume: int = UNSET_INTEGER
    market_cap_above: float = UNSET_DOUBLE
    market_cap_below: float = UNSET_DOUBLE
    moody_rating_above: str = ''
    moody_rating_below: str = ''
    sp_rating_above: str = ''
    sp_rating_below: str = ''
    maturity_date_above: str = ''
    maturity_date_below: str = ''
    coupon_rate_above: float = UNSET_DOUBLE
    coupon_rate_below: float = UNSET_DOUBLE
    exclude_convertible: bool = False
    average_option_volume_above: int = UNSET_INTEGER
    scanner_setting_pairs: str = ''
    stock_type_filter: str = ''


@dataclass
class SoftDollarTier:
    name: str = ''
    val: str = ''
    display_name: str = ''

    def __bool__(self):
        return bool(self.name or self.val or self.display_name)


@dataclass
class Execution:
    exec_id: str = ''
    time: datetime = field(default=EPOCH)
    acct_number: str = ''
    exchange: str = ''
    side: str = ''
    shares: float = 0.0
    price: float = 0.0
    perm_id: int = 0
    client_id: int = 0
    order_id: int = 0
    liquidation: int = 0
    cum_qty: float = 0.0
    avg_price: float = 0.0
    order_ref: str = ''
    ev_rule: str = ''
    ev_multiplier: float = 0.0
    model_code: str = ''
    last_liquidity: int = 0
    pending_price_revision: bool = False


@dataclass
class CommissionReport:
    exec_id: str = ''
    commission: float = 0.0
    currency: str = ''
    realized_pnl: float = 0.0
    yield_: float = 0.0
    yield_redemption_date: int = 0


@dataclass
class ExecutionFilter:
    client_id: int = 0
    acct_code: str = ''
    time: str = ''
    symbol: str = ''
    sec_type: str = ''
    exchange: str = ''
    side: str = ''


@dataclass
class BarData:
    date: Union[date_, datetime] = EPOCH
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0
    average: float = 0.0
    bar_count: int = 0


@dataclass
class RealTimeBar:
    time: datetime = EPOCH
    end_time: int = -1
    open_: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    wap: float = 0.0
    count: int = 0


@dataclass
class TickAttrib:
    can_auto_execute: bool = False
    past_limit: bool = False
    pre_open: bool = False


@dataclass
class TickAttribBidAsk:
    bid_past_low: bool = False
    ask_past_high: bool = False


@dataclass
class TickAttribLast:
    past_limit: bool = False
    unreported: bool = False


@dataclass
class HistogramData:
    price: float = 0.0
    count: int = 0


@dataclass
class NewsProvider:
    code: str = ''
    name: str = ''


@dataclass
class DepthMktDataDescription:
    exchange: str = ''
    sec_type: str = ''
    listing_exch: str = ''
    service_data_type: str = ''
    agg_group: int = UNSET_INTEGER


@dataclass
class PnL:
    account: str = ''
    model_code: str = ''
    daily_pn_l: float = nan
    unrealized_pn_l: float = nan
    realized_pn_l: float = nan


@dataclass
class TradeLogEntry:
    time: datetime
    status: str = ''
    message: str = ''
    error_code: int = 0


@dataclass
class PnLSingle:
    account: str = ''
    model_code: str = ''
    con_id: int = 0
    daily_pn_l: float = nan
    unrealized_pn_l: float = nan
    realized_pn_l: float = nan
    position: int = 0
    value: float = nan


@dataclass
class HistoricalSession:
    start_date_time: str = ''
    end_date_time: str = ''
    ref_date: str = ''


@dataclass
class HistoricalSchedule:
    start_date_time: str = ''
    end_date_time: str = ''
    time_zone: str = ''
    sessions: List[HistoricalSession] = field(default_factory=list)


@dataclass
class WshEventData:
    con_id: int = UNSET_INTEGER
    filter: str = ''
    fill_watchlist: bool = False
    fill_portfolio: bool = False
    fill_competitors: bool = False
    start_date: str = ''
    end_date: str = ''
    total_limit: int = UNSET_INTEGER


class AccountValue(NamedTuple):
    account: str
    tag: str
    value: str
    currency: str
    model_code: str


class TickData(NamedTuple):
    time: datetime
    tick_type: int
    price: float
    size: float


class HistoricalTick(NamedTuple):
    time: datetime
    price: float
    size: float


class HistoricalTickBidAsk(NamedTuple):
    time: datetime
    tick_attrib_bid_ask: TickAttribBidAsk
    price_bid: float
    price_ask: float
    size_bid: float
    size_ask: float


class HistoricalTickLast(NamedTuple):
    time: datetime
    tick_attrib_last: TickAttribLast
    price: float
    size: float
    exchange: str
    special_conditions: str


class TickByTickAllLast(NamedTuple):
    tick_type: int
    time: datetime
    price: float
    size: float
    tick_attrib_last: TickAttribLast
    exchange: str
    special_conditions: str


class TickByTickBidAsk(NamedTuple):
    time: datetime
    bid_price: float
    ask_price: float
    bid_size: float
    ask_size: float
    tick_attrib_bid_ask: TickAttribBidAsk


class TickByTickMidPoint(NamedTuple):
    time: datetime
    mid_point: float


class MktDepthData(NamedTuple):
    time: datetime
    position: int
    market_maker: str
    operation: int
    side: int
    price: float
    size: float


class DOMLevel(NamedTuple):
    price: float
    size: float
    market_maker: str


class PriceIncrement(NamedTuple):
    low_edge: float
    increment: float


class PortfolioItem(NamedTuple):
    contract: Contract
    position: float
    market_price: float
    market_value: float
    average_cost: float
    unrealized_pnl: float
    realized_pnl: float
    account: str


class Position(NamedTuple):
    account: str
    contract: Contract
    position: float
    avg_cost: float


class Fill(NamedTuple):
    contract: Contract
    execution: Execution
    commission_report: CommissionReport
    time: datetime


class OptionComputation(NamedTuple):
    tick_attrib: int
    implied_vol: Optional[float]
    delta: Optional[float]
    opt_price: Optional[float]
    pv_dividend: Optional[float]
    gamma: Optional[float]
    vega: Optional[float]
    theta: Optional[float]
    und_price: Optional[float]


class OptionChain(NamedTuple):
    exchange: str
    underlying_con_id: int
    trading_class: str
    multiplier: str
    expirations: List[str]
    strikes: List[float]


class Dividends(NamedTuple):
    past12_months: Optional[float]
    next12_months: Optional[float]
    next_date: Optional[date_]
    next_amount: Optional[float]


class NewsArticle(NamedTuple):
    article_type: int
    article_text: str


class HistoricalNews(NamedTuple):
    time: datetime
    provider_code: str
    article_id: str
    headline: str


class NewsTick(NamedTuple):
    time_stamp: int
    provider_code: str
    article_id: str
    headline: str
    extra_data: str


class NewsBulletin(NamedTuple):
    msg_id: int
    msg_type: int
    message: str
    orig_exchange: str


class FamilyCode(NamedTuple):
    account_id: str
    family_code_str: str


class SmartComponent(NamedTuple):
    bit_number: int
    exchange: str
    exchange_letter: str


class ConnectionStats(NamedTuple):
    start_time: float
    duration: float
    num_bytes_recv: int
    num_bytes_sent: int
    num_msg_recv: int
    num_msg_sent: int


class BarDataList(List[BarData]):
    """
    List of :class:`.BarData` that also stores all request parameters.

    Events:

        * ``updateEvent``
          (bars: :class:`.BarDataList`, hasNewBar: bool)
    """

    req_id: int
    contract: Contract
    end_date_time: Union[datetime, date_, str, None]
    duration_str: str
    bar_size_setting: str
    what_to_show: str
    use_rth: bool
    format_date: int
    keep_up_to_date: bool
    chart_options: List[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.update_event = Event('update_event')

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)


class RealTimeBarList(List[RealTimeBar]):
    """
    List of :class:`.RealTimeBar` that also stores all request parameters.

    Events:

        * ``updateEvent``
          (bars: :class:`.RealTimeBarList`, hasNewBar: bool)
    """

    req_id: int
    contract: Contract
    bar_size: int
    what_to_show: str
    use_rth: bool
    real_time_bars_options: List[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.update_event = Event('update_event')

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)


class ScanDataList(List[ScanData]):
    """
    List of :class:`.ScanData` that also stores all request parameters.

    Events:
        * ``updateEvent`` (:class:`.ScanDataList`)
    """

    req_id: int
    subscription: ScannerSubscription
    scanner_subscription_options: List[TagValue]
    scanner_subscription_filter_options: List[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.update_event = Event('updateEvent')

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)


class DynamicObject:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        clsName = self.__class__.__name__
        kwargs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{clsName}({kwargs})'


class FundamentalRatios(DynamicObject):
    """
    See:
    https://web.archive.org/web/20200725010343/https://interactivebrokers.github.io/tws-api/fundamental_ratios_tags.html
    """

    pass
