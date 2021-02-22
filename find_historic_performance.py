# -*- coding: utf-8 -*-

import io

import pandas as pd
import requests
import sqlalchemy
from sqlalchemy import *

ticker = 'aapl.us'  # use ticker as in stooq.com
initial_fund = 1000


class PortfolioPerformance():
    def __init__(self, ticker_dataframe_, initial_fund_):
        self.ticker_dataframe = ticker_dataframe_
        self.portfolio_performance = pd.DataFrame({
            'Value': [],
            'Shares': [],
            'Date': []
        })
        self.number_of_shares = 0
        self.portfolio_value = initial_fund_
        self.current_decision = None
        self.previous_decision = None
        self.previous_date = None
        self.current_date = None

    def set_accumulated_returns(self):
        day_open = self.ticker_dataframe[self.ticker_dataframe.Date ==
                                         self.current_date]['Open'].item()
        day_close = self.ticker_dataframe[self.ticker_dataframe.Date ==
                                          self.current_date]['Close'].item()
        day_return = day_close - day_open
        
        if self.previous_date is None:
            after_market_return = 0
        else:
            previous_day_close = self.ticker_dataframe[self.ticker_dataframe.Date == self.previous_date]['Close'].item()
            after_market_return = day_open - previous_day_close

        self.portfolio_value = self.portfolio_value + self.number_of_shares * (day_return + after_market_return)

    def set_number_of_shares(self):
        portfolio_change = self.get_portfolio_change()
        if portfolio_change == 'buy':
            number_of_shares = self.portfolio_value / \
                self.ticker_dataframe[self.ticker_dataframe.Date ==
                                      self.current_date]['Open'].item()
        elif portfolio_change == 'hold':
            number_of_shares = self.number_of_shares
        else:
            number_of_shares = 0
        self.number_of_shares = number_of_shares

    def get_portfolio_change(self):
        if self.previous_decision is None:
            return self.current_decision
        else:
            if self.current_decision == self.previous_decision:
                return 'hold'
            elif self.current_decision == 'buy' and self.previous_decision == 'sell':
                return 'buy'
            return 'sell'

    def add_current_portfolio_performance(self):
        self.portfolio_performance = self.portfolio_performance.append(
            {
                'Date': self.current_date,
                'Shares': self.number_of_shares,
                'Value': self.portfolio_value
            },
            ignore_index=True)


def main():
    target_url = 'https://stooq.com/q/d/l/?s={}&i=d&o=1111111'.format(ticker)
    ticker_data = requests.get(target_url)
    ticker_data = ticker_data.text
    buffer = io.StringIO(ticker_data)

    ticker_dataframe = pd.read_csv(
        buffer, parse_dates=True).drop(
            ['Volume'], axis=1)

    ticker_dataframe.to_excel(
        "ticker_dataframe.xlsx")
    list_of_decision_dates = ticker_dataframe['Date'].iloc[::7]

    bot_decisions = pd.DataFrame({
        'Date': [],
        'Decision': []
    })

    for x in range(len(list_of_decision_dates) - 4):
        pointer = x + 4  # to account for the first hindsight
        decision = 'buy'  # make here the model prediction
        bot_decisions = bot_decisions.append({
            'Date': list_of_decision_dates.iloc[pointer],
            'Decision': decision
        },
            ignore_index=True)

    portfolio_performance = PortfolioPerformance(
        ticker_dataframe, initial_fund)

    for _, day_data in ticker_dataframe.iterrows():
        portfolio_performance.current_date = day_data['Date']
        print(portfolio_performance.current_date)
        if portfolio_performance.current_date in bot_decisions['Date'].array:
            portfolio_performance.current_decision = bot_decisions[bot_decisions.Date == portfolio_performance.current_date]['Decision'].item()
            portfolio_performance.set_number_of_shares()
            portfolio_performance.previous_decision = portfolio_performance.current_decision

        portfolio_performance.set_accumulated_returns()
        portfolio_performance.add_current_portfolio_performance()
        portfolio_performance.previous_date = portfolio_performance.current_date

    portfolio_performance.portfolio_performance.to_excel(
        "portfolio_performance.xlsx")
    bot_decisions.to_excel('bot_decisions.xlsx')
    print('Job finished')


if __name__ == '__main__':
    main()
