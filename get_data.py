# -*- coding: utf-8 -*-

import io
import random
from pathlib import Path

import mplfinance as fplt
import pandas as pd
import requests

# Program arguments
ticker = 'aapl.us'  # use ticker as in stooq.com
foresight = 7  # in days
hindsight = 30  # in days
number_of_data = 1000  # to use in model


class SetGenerator():
    def __init__(self, ticker_data_, foresight_, hindsight_, number_of_data_):
        self.ticker_data = ticker_data_
        self.foresight = foresight_
        self.hindsight = hindsight_
        self.number_of_data = number_of_data_

    def get_ticker_slice(self, pointer):
        # print('Righ hand cut')
        ticker_data_slice = self.ticker_data.iloc[:pointer + self.foresight]
        # print(ticker_data_slice.tail())

        # print('Left hand cut')
        ticker_data_slice = ticker_data_slice.iloc[-self.foresight - self.hindsight:]
        # print(ticker_data_slice.head())

        assert len(ticker_data_slice) == self.foresight + self.hindsight
        return ticker_data_slice

    def foresight_buy_or_sell(self, slide_of_ticker_data):
        current = slide_of_ticker_data['Close'].iloc[-self.foresight - 1]
        # print('Current price = {}'.format(current))

        future = slide_of_ticker_data['Close'].iloc[-1]
        # print('Future price = {}'.format(future))

        return 'buy' if current < future else 'sell'

    def generate_sets(self):
        for x in range(self.number_of_data):
            random_pointer = random.randint(
                self.hindsight, len(self.ticker_data) - self.foresight)

            # print('Random pointer = {}'.format(random_pointer))

            data = self.get_ticker_slice(random_pointer)

            # print('Data slice = ')
            # print(data)

            buy_or_sell = self.foresight_buy_or_sell(data)

            # print('Recommendation = {}'.format(buy_or_sell))

            save_to = 'data\\model_data\\{}\\{}.png'.format(buy_or_sell, x)

            # print('Saving to {}'.format(save_to))
            assert len(data.iloc[:self.hindsight]) == self.hindsight
            fplt.plot(data.iloc[:self.hindsight],
                      type='candle', savefig=save_to)

            print('Finished {} of {}'.format(x + 1, self.number_of_data))


def main():

    # Get data and load it into dataframe
    target_url = 'https://stooq.com/q/d/l/?s={}&i=d&o=1111111'.format(ticker)
    ticker_data = requests.get(target_url)
    ticker_data = ticker_data.text
    buffer = io.StringIO(ticker_data)

    print('Downloading data...')
    ticker_dataframe = pd.read_csv(
        buffer, index_col='Date', parse_dates=True).drop(
            ['Volume'], axis=1)
    ticker_dataframe.to_excel("portfolio_performance.xlsx")
    print('Data downloaded')

    # Make folders if necessary
    required_paths = [Path('data\\model_data'), Path(
        'data\\model_data\\sell'), Path('data\\model_data\\buy')]

    for path in required_paths:
        if not path.exists():
            path.mkdir()
            print('Path {} does not exist. Creating path...'.format(path))

    # Generate sets
    set_generator = SetGenerator(
        ticker_dataframe, foresight, hindsight, number_of_data)
    set_generator.generate_sets()
    print('Job finished')


if __name__ == '__main__':
    main()
