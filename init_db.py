# -*- coding: utf-8 -*-

import requests
import io
import pandas as pd
import sqlalchemy
from sqlalchemy import *

ticker = 'aapl.us'  # use ticker as in stooq.com

target_url = 'https://stooq.com/q/d/l/?s={}&i=d&o=1111111'.format(ticker)
ticker_data = requests.get(target_url)
ticker_data = ticker_data.text
buffer = io.StringIO(ticker_data)

ticker_dataframe = pd.read_csv(
    buffer, index_col='Date', parse_dates=True).drop(
    ['Volume'], axis=1)

bot_decisions_df = pd.read_excel('bot_decisions.xlsx', parse_dates=True)
portfolio_performance = pd.read_excel('portfolio_performance.xlsx', parse_dates=True)

def main():
    
    engine = create_engine('sqlite:///db.db', echo=True)

    meta = MetaData()

    stock_data = Table(
        'stock_data', meta,
        Column('Date', Date, primary_key=True),
        Column('Open', Float),
        Column('Close', Float),
        Column('Low', Float),
        Column('High', Float)
    )

    potfolio = Table(
        'potfolio', meta,
        Column('Date', Date, primary_key=True),
        Column('Value', Float),
        Column('Shares', Float)
    )

    bot_decisions = Table(
        'bot_decisions', meta,
        Column('Date', Date, primary_key=True),
        Column('Decision', String)
    )

    meta.create_all(engine)

    conn = engine.connect()

    ins = stock_data.insert()
    for index, day in ticker_dataframe.iterrows():
        ins = stock_data.insert().values(Date=index, Open=float(day['Open']), Close=float(
            day['Close']), High=float(day['High']), Low=float(day['Low']))
        conn.execute(ins)

    ins = potfolio.insert()
    for index, day in portfolio_performance.iterrows():
        ins = potfolio.insert().values(Date=day['Date'], Value=float(day['Value']), Shares=float(day['Shares']))
        conn.execute(ins)

    ins = bot_decisions.insert()
    for index, day in bot_decisions_df.iterrows():
        ins = bot_decisions.insert().values(Date=day['Date'], Decision=str(day['Decision']))
        conn.execute(ins)


    print('Job finished')


if __name__ == '__main__':
    main()
