from datetime import datetime
import pandas as pd
from trade_his.trade_his import TradeHis
class TradeExecutor:
  def __init__(self, kit, fix_instrument):
    self.kit = kit
    self.trade_his = TradeHis()
    self.fix_instrument = fix_instrument
    self.instrument_ltp = None
    self.entry_price = None
    self.stoploss = None
    self.target_price = None
    self.tradling_target = None
    self.in_entry = False
    self.in_trade = False
    self.final_target = False
  
  def get_current_price(self, instrument):
    return self.kit.ltp(instrument)[str(instrument)]['last_price']

  def execute_trade(self, instrument, trade_type, high_data, low_data):
    print("=========Execute Trade==========")
    self.stoploss = high_data if trade_type == "SELL" else low_data
    self.entry_price, self.stoploss, self.target_price = self.entry_trade(self.fix_instrument, self.stoploss)
    self.stoploss = self.stoploss + 5 if trade_type == "SELL" else self.stoploss - 5
    instrument_token, tradingsymbol, ltp_price = self.trade_info(instrument)
    self.instrument_ltp = instrument_token

    data = [trade_type, tradingsymbol, datetime.now(), self.entry_price, 0, 0, self.target_price, self.stoploss, 0, ltp_price, 0]
    self.trade_his.insert_row(data)

    self.in_entry = True

  def trade_info(self, instrument):
    instrument_token = instrument['instrument_token']
    tradingsymbol = instrument['tradingsymbol']
    ltp_price = self.get_current_price(instrument_token)
    return instrument_token, tradingsymbol, ltp_price

  def entry_trade(self, instrument_token, stoploss):
    print("=========Entry Trade========")
    current_price = self.get_current_price(instrument_token)
    entry_price = current_price
    target_price = entry_price + ((entry_price - stoploss) * 2)
    self.tradling_target = entry_price + ((entry_price - stoploss) * 1.5)
    return entry_price, stoploss, target_price

  def check_exit_condition(self, trade_type, low_price, rsi_data):
    current_price = self.get_current_price(self.fix_instrument)
    if self.in_entry and trade_type == "BUY" and (self.target_price < current_price or self.stoploss > current_price):
      self.final_target = True
    elif self.in_entry and trade_type == "SELL" and (self.target_price > current_price or self.stoploss < current_price):
      self.exit()
    
    if self.final_target:
      self.rsi_trale(low_price, rsi_data)

  def exit(self):
    print("========Exit===============")
    exit_price = self.get_current_price(self.fix_instrument)
    profit = exit_price - self.entry_price
    ltp_price = self.get_current_price(self.instrument_ltp)
    self.in_trade = False
    self.in_entry = False
    data = {'exit': exit_price, 'exit_time': datetime.now(), 'profit': profit, 'exit_price': ltp_price}
    self.trade_his.update_row(data)

  def rsi_trale(self, low_price, rsi_data):
    print("=======Rsi Trale===========")
    if self.tradling_target < low_price:
      if rsi_data > 60:
        rsi_60 = True
      if rsi_60 and (rsi_data < 60):
        self.exit()
        rsi_60 = False
        self.final_target = False
    else:
      self.exit()
      self.final_target = False
