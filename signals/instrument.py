import datetime

class Instrument:
  def __init__(self, strike_price):
    self.strike_price = strike_price

  @staticmethod
  def calculate_atm_strike_price(nse_value):
    # Round down the NSE value to the nearest multiple of 50
    strike_price = int(nse_value / 50) * 50
    return strike_price

  def create_trading_symbol(self, buy_sell_toggle):
    today = datetime.date.today()
    year = today.strftime("%y")
    month = today.strftime("%b").upper()
    strike_price = self.calculate_atm_strike_price(self.strike_price)
    return f"NIFTY{year}{month}{strike_price}{buy_sell_toggle}"

  def search_instrument(self, kit, buy_sell_toggle):
    ins = kit.instruments("NFO")
    tradingsymbol = self.create_trading_symbol(buy_sell_toggle)
    for i in ins:
      if i['tradingsymbol'] == tradingsymbol:
        return i
    return None