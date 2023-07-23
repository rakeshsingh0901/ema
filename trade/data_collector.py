from signals.data import Data

class DataCollector:
  def __init__(self, kit, fix_instrument):
    self.kit = kit
    self.fix_instrument = fix_instrument
    
  def collect_data(self):
    data = Data.get_historical_data(self.kit, self.fix_instrument, interval='5minute', day=10)
    date_data, open_data, high_data, low_data, close_data = Data.clean_data(data)
    return date_data, open_data, high_data, low_data, close_data
