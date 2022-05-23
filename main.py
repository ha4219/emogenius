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
from preprocessing import preprocessing
import matplotlib.pyplot as plt
from data.customPath import _get_path_name, _mkdir_path, _plot_acc, _plot_loss


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

NAME = 'kobert_init'
DESC = ''

#토큰화
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

#train & test 데이터로 나누기
from sklearn.model_selection import train_test_split

data = preprocessing()

dataset_train, dataset_test = train_test_split(data, test_size=0.25, random_state=0)

data_train = CustomDataset(dataset_train, 0, 1, tok, max_len, True, False)
data_test = CustomDataset(dataset_test, 0, 1, tok, max_len, True, False)

train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, num_workers=5)
test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size, num_workers=5)


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=58,   ##클래스 수 조정##
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
                 
        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

  #BERT 모델 불러오기
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

#optimizer와 schedule 설정
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]

optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()

t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total * warmup_ratio)

scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

#정확도 측정을 위한 함수 정의
def calc_accuracy(X,Y):
  max_vals, max_indices = torch.max(X, 1)
  train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
  return train_acc
    
best_acc = 0
best_model = deepcopy(model.state_dict())
train_acc_history = []
train_loss_history = []
val_acc_history = []
val_loss_history = []

since = time()


for e in range(num_epochs):
  train_acc = 0.0
  train_loss = 0.0
  test_acc = 0.0
  test_loss = 0.0
  
  running_loss = 0.0
  running_corrects = 0

  model.train()
  for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(train_dataloader)):
    optimizer.zero_grad()
    token_ids = token_ids.long().to(device)
    segment_ids = segment_ids.long().to(device)
    valid_length= valid_length
    label = label.long().to(device)
    out = model(token_ids, valid_length, segment_ids)
    loss = loss_fn(out, label)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
    optimizer.step()
    scheduler.step()  # Update learning rate schedule

    _, preds = torch.max(out, 1)
    
    running_loss += loss.item() * token_ids.size(0)
    running_corrects += torch.sum(preds == label.data)
    # if batch_id % log_interval == 0:
    #     print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
  train_loss = running_loss / len(train_dataloader.dataset)
  train_acc = running_corrects.double() / len(train_dataloader.dataset)
  
  train_acc_history.append(train_acc)
  train_loss_history.append(train_loss)

  print("epoch {} train acc {}".format(e+1, train_acc))
  

  running_loss = 0.0
  running_corrects = 0

  model.eval()
  for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(test_dataloader)):
    token_ids = token_ids.long().to(device)
    segment_ids = segment_ids.long().to(device)
    valid_length= valid_length
    label = label.long().to(device)
    out = model(token_ids, valid_length, segment_ids)
    

    _, preds = torch.max(out, 1)
    
    running_loss += loss.item() * token_ids.size(0)
    running_corrects += torch.sum(preds == label.data)
    # if batch_id % log_interval == 0:
    #     print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
  test_loss = running_loss / len(train_dataloader.dataset)
  test_acc = running_corrects.double() / len(train_dataloader.dataset)
  
  val_acc_history.append(test_acc)
  val_loss_history.append(test_loss)

  if test_acc > best_acc:
    best_acc = test_acc
    best_model = deepcopy(model.state_dict())
  print("epoch {} test acc {}".format(e+1, test_acc))


time_elapsed = time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
print('Best val Acc: {:4f}'.format(best_acc))

path = _get_path_name(NAME, DESC)
_mkdir_path(path)
_plot_acc(path, training_acc=train_acc_history, validation_acc=val_acc_history)
_plot_loss(path, training_loss=train_loss_history, validation_loss=val_loss_history)

model.load_state_dict(best_model)
torch.save(model, f"{path}/{NAME}.pt")
