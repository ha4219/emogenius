from flask import Flask, jsonify
from flask import request
from kobert import get_pytorch_kobert_model, get_tokenizer
import torch
import gluonnlp as nlp
from mxnet import gluon
import torch.nn as nn
from flask_cors import CORS

PATH = 'server/app/kobert_init.pt'

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
transform = nlp.data.BERTSentenceTransform(
        tok, max_seq_length=max_len, pad=True, pair=False)
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

model.load_state_dict(torch.load(PATH, map_location='cpu'), strict=False)

model.eval()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def predict():
  params = request.get_json()
  print(params)
  text = params['text']
  # text = request.args.get('text')
  sent_dataset = gluon.data.SimpleDataset([text,])
  sentences = sent_dataset.transform(transform)

  token_ids, valid_length, segment_ids = sentences[0]

  token_ids = torch.from_numpy(token_ids.reshape((1, -1)))
  valid_length = torch.from_numpy(valid_length.reshape((1, -1)))
  segment_ids = torch.from_numpy(segment_ids.reshape((1, -1)))

  token_ids = token_ids.long().to(device)
  segment_ids = segment_ids.long().to(device)
  valid_length= valid_length
  out = model(token_ids, valid_length, segment_ids)
  _, pred = torch.max(out, 1)
  pred = pred.cpu().numpy()[0]
  res = {'result': int(pred)}
  print(res)
  return jsonify(res)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80)