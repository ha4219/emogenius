import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np


TRAIN_PATH = '/home/dongha/code/data/conversation/Training/final_Training.xlsx'
TEST_PATH = '/home/dongha/code/data/conversation/Validation/final_Validation.xlsx'

LABEL_CNT = 58

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

def preprocessing_test(path=TEST_PATH):
  data = pd.read_excel(path)
  enc = LabelEncoder()
  data['감정_소분류'] = enc.fit_transform(data['감정_소분류'])
  res = []
  mapping = dict(zip(enc.classes_, enc.transform(enc.classes_)))
  for q, label in zip(data['사람문장1'], data['감정_소분류']):
    tmp = []
    tmp.append(q)
    tmp.append(label)
    res.append(tmp)
  return res, mapping

def preprocessing_limit(path=TRAIN_PATH):
  data = pd.read_excel(path)
  enc = LabelEncoder()
  data['감정_소분류'] = enc.fit_transform(data['감정_소분류'])
  res = []
  res_tmp = [[] for _ in range(LABEL_CNT)]
  for q, label in zip(data['사람문장1'], data['감정_소분류']):
    tmp = []
    tmp.append(q)
    tmp.append(label)
    res_tmp[label].append(tmp)
  min_val = 1e9
  for items in res_tmp:
    min_val = min(min_val, len(items))
  for items in res_tmp:
    res += items[:min_val]
  return res


{
  '가난한, 불우한': 0,
  '감사하는': 1,
  '걱정스러운': 2,
  '고립된': 3,
  '외로운': 37, 
  '괴로워하는': 4,
  '구역질 나는': 5,
  '기쁨': 6,
  '낙담한': 7,
  '남의 시선을 의식하는': 8,
  '노여워하는': 9,
  '눈물이 나는': 10, 
  '느긋': 11, 
  '당혹스러운': 12, 
  '당황': 13, 
  '두려운': 14, 
  '마비된': 15, 
  '만족스러운': 16, 
  '방어적인': 17, 
  '배신당한': 18, 
  '버려진': 19, 
  '부끄러운': 20, 
  '분노': 21, 
  '불안': 22, 
  '비통한': 23, 
  '상처': 24, 
  '성가신': 25, 
  '스트레스 받는': 26, 
  '슬픔': 27, 
  '신뢰하는': 28, 
  '신이 난': 29, 
  '실망한': 30, 
  '악의적인': 31, 
  '안달하는': 32, 
  '안도': 33, 
  '억울한': 34, 
  '열등감': 35, 
  '염세적인': 36, 
  '우울한': 38, 
  '자신하는': 39, 
  '조심스러운': 40, 
  '좌절한': 41, 
  '죄책감의': 42, 
  '질투하는': 43, 
  '짜증내는': 44, 
  '초조한': 45, 
  '충격 받은': 46, 
  '취약한': 47, 
  '툴툴대는': 48, 
  '편안한': 49, 
  '한심한': 50, 
  '혐오스러운': 51, 
  '혼란스러운': 52, 
  '환멸을 느끼는': 53, 
  '회의적인': 54, 
  '후회되는': 55, 
  '흥분': 56, 
  '희생된': 57
}
