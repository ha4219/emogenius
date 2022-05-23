import mxnet
import gluonnlp as nlp
import pandas as pd

TRAIN_PATH = '/home/dongha/code/data/conversation/Training/final_Training.xlsx'

# Index(['번호', '연령', '성별', '상황키워드', '신체질환', '감정_대분류', '감정_소분류', '사람문장1',
#  '시스템응답1', '사람문장2', '시스템응답2', '사람문장3', '시스템응답3', '사람문장4', '시스템응답4'],
# dtype='object')
data = pd.read_excel(TRAIN_PATH)
for i in data['감정_소분류']:
  print(i)

