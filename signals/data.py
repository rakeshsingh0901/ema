import pandas as pd
import numpy as np
import datetime
import talib as ta

class Data:

  @staticmethod
  def get_historical_data(kite, instrument_token, interval="day", day=30):
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=day)
    to_datetime = datetime.datetime.now()
    data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
    return data

  @staticmethod
  def clean_data(data):
    date_data = np.array([i['date'] for i in data])
    open_data = np.array([i['open'] for i in data])
    high_data = np.array([i['high'] for i in data])
    low_data = np.array([i['low'] for i in data])
    close_data = np.array([i['close'] for i in data])
    return date_data, open_data, high_data, low_data, close_data
  
  @staticmethod
  def adx(self, high_data, low_data, close_data, time_period=14):
    return ta.ADX(high_data, low_data, close_data, timeperiod=time_period)

  @staticmethod
  def ema(self, close_data, time_period=9):
    return ta.EMA(close_data, timeperiod=time_period)

  @staticmethod
  def bollinger_band(self, close_data, time_period=20):
    return ta.BBANDS(close_data, timeperiod=time_period)
  
  @staticmethod
  def rsi(self, close_data, time_period=14):
    return ta.RSI(close_data, timeperiod=time_period)