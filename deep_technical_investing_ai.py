# -*- coding: utf-8 -*-

import random
import io
import fastai
import mplfinance as fplt
import numpy as np
import pandas as pd

ticker_dataframe = pd.read_csv(
    'resources\\aapl.csv', index_col='Date', parse_dates=True).drop(['Volume'], axis=1)
foresight = 7
hindsight = 7
number_of_training_sets = 5  # see about 5 years of ticks 
number_of_test_sets = 1

def get_ticker_slice(ticker_data, pointer, forecast_in_ticks, hindsight_in_ticks):
    ticker_data_slice = ticker_data[:pointer + forecast_in_ticks]
    ticker_data_slice = ticker_data_slice[-forecast_in_ticks - hindsight_in_ticks:]
    return ticker_data_slice


def foresight_buy_or_sell(ticker_data, forecast_in_ticks):
    return 'buy' if ticker_data['Close'][-forecast_in_ticks] < ticker_data['Close'][-1] else 'sell' 


def generate_sets(ticker_data, number_of_training_sets, number_of_test_sets, forecast_in_ticks, hindsight_in_ticks):
    training_set = list()
    test_set = list()

    random_pointers = list()
    for x in range(number_of_test_sets + number_of_training_sets):
        random_pointers.append(random.randint(hindsight_in_ticks, len(ticker_data) - forecast_in_ticks))
    print(random_pointers)

    for x in range(number_of_training_sets):
        data = get_ticker_slice(ticker_data, random_pointers[x], forecast_in_ticks, hindsight_in_ticks)
        chart = io.BytesIO()
        fplt.plot(data[-forecast_in_ticks:], type='candle', savefig=chart)
        chart.seek(0)
        buy_or_sell = foresight_buy_or_sell(ticker_data, forecast_in_ticks)
        training_set.append([chart, buy_or_sell])

    for x in range(number_of_test_sets):
        data = get_ticker_slice(ticker_data, random_pointers[x + number_of_training_sets], forecast_in_ticks, hindsight_in_ticks)
        chart = io.BytesIO()
        fplt.plot(data[-forecast_in_ticks:], type='candle', savefig=chart)
        chart.seek(0)
        buy_or_sell = foresight_buy_or_sell(ticker_data, forecast_in_ticks)
        test_set.append([chart, buy_or_sell])
        
    return (training_set, test_set)


def train_model():
    pass


def test_model():
    pass


def save_model():
    pass

training_set, test_set = generate_sets(ticker_dataframe, number_of_training_sets, number_of_test_sets, foresight, hindsight)
