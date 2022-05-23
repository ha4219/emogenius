import mxnet
import gluonnlp as nlp
import pandas as pd

TRAIN_PATH = '/home/dongha/code/data/conversation/Training/final_Training.xlsx'

data = pd.read_excel(TRAIN_PATH)
print(data.sample(10))