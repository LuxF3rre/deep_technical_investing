# -*- coding: utf-8 -*-

import random
import io
import requests

import mplfinance as fplt
import pandas as pd

ticker = 'aapl.us'  # use ticker as in stooq.com
url = 'https://stooq.com/q/d/l/?s={}&i=d'.format(ticker)
ticker_data = requests.get(target_url)
ticker_data = ticker_data.text
buffer = io.StringIO(ticker_data)

ticker_dataframe = pd.read_csv(
    buffer, index_col='Date', parse_dates=True).drop(['Volume'], axis=1)
foresight = 7
hindsight = 30
number_of_data = 1000


def get_ticker_slice(ticker_data, pointer, forecast_in_ticks, hindsight_in_ticks):
    ticker_data_slice = ticker_data[:pointer + forecast_in_ticks]
    ticker_data_slice = ticker_data_slice[-forecast_in_ticks -
                                          hindsight_in_ticks:]
    return ticker_data_slice


def foresight_buy_or_sell(ticker_data, forecast_in_ticks):
    return 'buy' if ticker_data['Close'][-forecast_in_ticks] < ticker_data['Close'][-1] else 'sell'


def generate_sets(ticker_data, number_of_data, forecast_in_ticks, hindsight_in_ticks):
    random_pointers = list()
    for x in range(number_of_data):
        random_pointers.append(random.randint(
            hindsight_in_ticks, len(ticker_data) - forecast_in_ticks))

    for x in range(number_of_data):
        data = get_ticker_slice(
            ticker_data, random_pointers[x], forecast_in_ticks, hindsight_in_ticks)
        buy_or_sell = foresight_buy_or_sell(data, forecast_in_ticks)
        save_to = 'data\\{}\\{}.png'.format(buy_or_sell, x)
        fplt.plot(data[-hindsight_in_ticks:], type='candle',
                  savefig=save_to)
        print('Finished {} of {}'.format(x + 1, number_of_data))


generate_sets(ticker_dataframe, number_of_data, foresight, hindsight)
