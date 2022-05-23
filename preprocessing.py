import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np


TRAIN_PATH = '/home/dongha/code/data/conversation/Training/final_Training.xlsx'

def preprocessing(path=TRAIN_PATH):
  data = pd.read_excel(path)
  enc = LabelEncoder()
  data['감정_소분류'] = enc.fit_transform(data['감정_소분류'])
  res = []
  for q, label in zip(data['사람문장1'], data['감정_소분류']):
    tmp = []
    tmp.append(q)
    tmp.append(label)
    res.append(tmp)
  return res


