import pandas as pd

class Store():
   def __init__(self):
      self.data = pd.Series()
   def store(self, data):
      print(self.data.append(data))
   def show(self):
      print(self.data)
