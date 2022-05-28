from kobert import get_pytorch_kobert_model, get_tokenizer
import torch
import gluonnlp as nlp
from mxnet import gluon
import torch.nn as nn
from labelTransfer import num2labelTransfer

from model import BERTClassifier

PATH = 'bert_model/runs/2022-05-27-23:25:13_kobert_init_/kobert_init.pt'

# Setting parameters
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 50
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

device = torch.device("cpu")
bertmodel, vocab = get_pytorch_kobert_model()
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
# data_train = CustomDataset(dataset_train, 0, 1, tok, max_len, True, False)

transform = nlp.data.BERTSentenceTransform(
        tok, max_seq_length=max_len, pad=True, pair=False)
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

model.load_state_dict(torch.load(PATH, map_location='cpu'), strict=False)

model.eval()


text = '친구 관계가 너무 힘들어. 베푸는 만큼 돌아오지 않는 것 같아.'
# text = request.args.get('text')
sent_dataset = gluon.data.SimpleDataset([[text,]])
sentences = sent_dataset.transform(transform)

token_ids, valid_length, segment_ids = sentences[0]

token_ids = torch.from_numpy(token_ids.reshape((1, -1)))
valid_length = torch.from_numpy(valid_length.reshape((1, -1)))
segment_ids = torch.from_numpy(segment_ids.reshape((1, -1)))

token_ids = token_ids.long().to(device)
segment_ids = segment_ids.long().to(device)
valid_length = valid_length
out = model(token_ids, valid_length, segment_ids)
print(out)
_, pred = torch.max(out, 1)
print(pred)
pred = pred.cpu().numpy()[0]
res = int(pred)


print(res, num2labelTransfer(res))