from copy import deepcopy
from time import time
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm
#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

#transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from dataset import CustomDataset
from model import BERTClassifier
from preprocessing import preprocessing_test
import matplotlib.pyplot as plt
from data.customPath import _get_path_name, _mkdir_path, _plot_acc, _plot_loss
from matplotlib import font_manager, rc
font_path = "./fonts/NanumGothic.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
plt.rcParams["font.family"] = "NanumGothic"

#GPU 사용
device = torch.device("cuda:3")
#BERT 모델, Vocabulary 불러오기
bertmodel, vocab = get_pytorch_kobert_model()

# Setting parameters
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 50
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

PATH = '/home/dongha/code/nlp/runs/2022-05-24-03:35:46_kobert_init_/kobert_init.pt'

#토큰화
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

data, enc = preprocessing_test()


data_test = CustomDataset(data, 0, 1, tok, max_len, True, False)

test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size, num_workers=5)

model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

ckpt = torch.load(PATH, map_location='cpu')
csd = ckpt.float().state_dict()
model.load_state_dict(csd, strict=False)

model.eval()

logs = []
running_loss = 0.0
running_corrects = 0

for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(test_dataloader)):
  token_ids = token_ids.long().to(device)
  segment_ids = segment_ids.long().to(device)
  valid_length= valid_length
  label = label.long().to(device)
  out = model(token_ids, valid_length, segment_ids)
  

  _, preds = torch.max(out, 1)
  
  preds = preds.cpu()
  label = label.cpu()
  for i in range(token_ids.size(0)):
    logs.append((preds[i], label[i]))

  running_corrects += torch.sum(preds.cpu() == label.cpu().data)

test_acc = running_corrects.double() / len(test_dataloader.dataset)

cnts = [[0] * 58 for _ in range(58)]

d = [i for i in enc.keys()]

for truth, predict in logs:
  # if truth != predict:
  cnts[truth][predict] += 1

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

ax.imshow(cnts)

# for i in range(58):
#     for j in range(58):
#         text = ax.text(j, i, cnts[i][j],
#                        ha="center", va="center", color="w")

ax.set_title(f'acc: {test_acc}')
ax.set_ylabel('truth')
ax.set_xlabel('predict')
ax.set_xticks(np.arange(len(d)), labels=d)
ax.set_yticks(np.arange(len(d)), labels=d)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
plt.rc('font', family=font)
plt.savefig('plot/check.png')