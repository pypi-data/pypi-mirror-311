from ibkr_engine.ib import IB
from ibkr_engine.contracts import Forex


HOST = '127.0.0.1'
PORT = 4002

ib = IB(
    host=HOST,
    port=PORT,
    client_id=1
)


def main():
    ib.connect()
    contract = Forex('EURUSD')
    bars = ib.reqHistoricalData(
        contract, endDateTime='', durationStr='30 D',
        barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

    # convert to pandas dataframe (pandas needs to be installed):
    df = util.df(bars)
    print(df)


if __name__ == '__main__':
    main()
