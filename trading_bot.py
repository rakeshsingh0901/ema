from trade.data_collector import DataCollector
from sessions.session import KiteApp
from trade.trade_executor import TradeExecutor
from signals.trading_signal import TradingSignal
from signals.instrument import Instrument
from signals.data import Data
from datetime import datetime, time
from time import sleep

class TradingBot:
  def __init__(self, enctoken, fix_instrument):
    self.kit = KiteApp(enctoken)
    self.fix_instrument = fix_instrument
    self.data_collector = DataCollector(self.kit, self.fix_instrument)
    self.trade_executor = TradeExecutor(self.kit, self.fix_instrument)
    self.first_time = True
    self.buy_signal = False
    self.sell_signal = False
    self.in_trade = False
  
  def his_data(self):
    data = self.data_collector.collect_data()
    date_data = data[0]
    open_data = data[1]
    high_data = data[2]
    low_data = data[3]
    close_data = data[4]
    return date_data, open_data, high_data, low_data, close_data
  
  def indicator(self, date_data, open_data, high_data, low_data, close_data):
    adx = Data().adx(self, high_data, low_data, close_data)
    ema_5 = Data().ema(self, close_data, time_period=5)
    bolliger_band = Data().bollinger_band(self, close_data)
    return adx, ema_5, bolliger_band
  
  def run(self):
    desired_time = time(9, 20)

    while True:
      current_time = datetime.now().time()
      print("current_time", current_time)

      if current_time > desired_time:
        if self.first_time and not self.in_trade:
          date_data, open_data, high_data, low_data, close_data = self.his_data()
          adx, ema_5, bolliger_band = self.indicator(date_data, open_data, high_data, low_data, close_data)
          self.buy_signal = TradingSignal.is_buy_signal(high_data[-2], ema_5[-2], adx[-2], low_data[-2], bolliger_band[2][-2])
          self.sell_signal = TradingSignal.is_sell_signal(high_data[-2], ema_5[-2], low_data[-2], bolliger_band[0][-2])
          self.first_time = False
          print("????????")
        
        if current_time.minute % 5 == 0 and current_time.second == 0 and not self.in_trade:
          date_data, open_data, high_data, low_data, close_data = self.his_data()
          adx, ema_5, bolliger_band = self.indicator(date_data, open_data, high_data, low_data, close_data)
          self.buy_signal = TradingSignal.is_buy_signal(high_data[-2], ema_5[-2], adx[-2], low_data[-2], bolliger_band[2][-2])
          self.sell_signal = TradingSignal.is_sell_signal(high_data[-2], ema_5[-2], low_data[-2], bolliger_band[0][-2])
          print("-------------")
        
        if self.buy_signal and not self.in_trade:
          trade_type = "BUY"
          self.check_entry_condition(trade_type, high_data[-2], low_data[-2])

        if self.sell_signal and not self.in_trade:
          trade_type = "SELL"
          self.check_entry_condition(trade_type, high_data[-2], low_data[-2])

        if self.in_trade:
          rsi_data = Data.rsi(self, close_data)[-2]
          self.trade_executor.check_exit_condition(trade_type, low_data[-2], rsi_data)

        # if datetime.now().hour == 15 and datetime.now().minute == 15:
        #   break

      sleep(1)

  def check_entry_condition(self, trade_type, high_price, low_price):
    current_price = self.trade_executor.get_current_price(self.fix_instrument)
    name_type = "CE" if trade_type == "BUY" else "PE"
    if trade_type == "BUY" and high_price < current_price:
      instrument = Instrument(current_price).search_instrument(self.kit, name_type)
      self.trade_executor.execute_trade(instrument, trade_type, high_price, low_price)
      self.in_trade = True
    elif trade_type == "SELL" and low_price > current_price:
      instrument = Instrument(current_price).search_instrument(self.kit, name_type)
      self.trade_executor.execute_trade(instrument, trade_type, high_price, low_price)
      self.in_trade = True

# Define the WSGI application callable
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    print('>>>>>>>>>>>>>>>>>>>>>>>')
    enctoken = "ogDV+YjtzqFIxralu0no91L3Glod28EOrtH5PXWPB2qzcTbcDgWYjRfMKcUeDm2dyL9IQXQxsl7PMpalqVeZQ3q9mpFJBSbIuYLp+wmyfYlJpqRMsYMU9g=="
    fix_instrument = 256265
    bot = TradingBot(enctoken, fix_instrument)
    return [bot.run().encode('utf-8')]
# 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