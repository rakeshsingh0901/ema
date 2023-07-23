import pandas as pd

class TradeHis:
  def __init__(self):
    try:
      self.df = pd.read_csv("trade_his.csv")
    except FileNotFoundError:
      self.df = pd.DataFrame()

  def insert_row(self, data):
    self.df.loc[len(self.df)] = data
    self.df.to_csv('trade_his.csv', index=False)

  def update_row(self, data):
    if not self.df.empty:
      self.df.loc[self.df.index[-1], data.keys()] = data.values()
      self.df.to_csv('trade_his.csv', index=False)