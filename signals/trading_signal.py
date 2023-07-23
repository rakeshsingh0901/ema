class TradingSignal:
  @staticmethod
  def is_buy_signal(candle_high, ema_5, adx, candle_low, lower_band):
    if candle_high < ema_5 and adx > 20 and candle_low < lower_band:
      return True
    return False

  @staticmethod
  def is_sell_signal(candle_high, ema_5, candle_low, higher_band):
    if candle_low > ema_5 and candle_high > higher_band and (candle_low - ema_5) > 4.0:
      return True
    return False