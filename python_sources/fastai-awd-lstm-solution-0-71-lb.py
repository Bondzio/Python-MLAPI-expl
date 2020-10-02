#!/usr/bin/env python
# coding: utf-8

# # Coreference resolution with fast.ai
# 
# In this notebook, we will explore ULMFiT approach to solve this task. With proper fine-tuning, you can get decent results in a matter of 20 minutes. Some 15 epochs of fine-tuning will get you up to 20-ish place.
# 
# Changes in this version:
# 1. More civilized approach to validation.
# 2. The model uses the representation of the last token of the entity instead of the first token. With a unidirectional encoder, this might be the right thing to do.
# 
# I will be grateful for any suggestions, especially about converting two logits/probabilities into the three classes without the need for an additional layer.
# 
# ## Collect the data

# In[ ]:


from fastai.text import *
from tqdm import tqdm_notebook as tqdm


# In[ ]:


get_ipython().system('wget https://github.com/google-research-datasets/gap-coreference/raw/master/gap-development.tsv -q')
get_ipython().system('wget https://github.com/google-research-datasets/gap-coreference/raw/master/gap-test.tsv -q')
get_ipython().system('wget https://github.com/google-research-datasets/gap-coreference/raw/master/gap-validation.tsv -q')


# In[ ]:


data_path = Path(".")


# In[ ]:


train = pd.read_csv(data_path/"gap-development.tsv", sep="\t")
val = pd.read_csv(data_path/"gap-validation.tsv", sep="\t")
test = pd.read_csv(data_path/"gap-test.tsv", sep="\t")


# In[ ]:


print(len(train), len(val), len(test))


# In[ ]:


train["is_valid"] = True
test["is_valid"] = False
val["is_valid"] = True

df_pretrain = pd.concat([train, test, val])


# Finetune the language model:

# In[ ]:


db = (TextList.from_df(df_pretrain, data_path/"db", cols="Text").split_from_df(col="is_valid").label_for_lm().databunch())


# In[ ]:


vocab = db.vocab


# In[ ]:


lm = language_model_learner(db, AWD_LSTM, drop_mult=0.5, pretrained=True)


# As the language model is already trained on Wikipedia, which is also the source of the excerpts, we can proceed to unfreezing right away:

# In[ ]:


lm.unfreeze()


# In[ ]:


lm.lr_find()


# In[ ]:


lm.recorder.plot()


# In[ ]:


lm.fit_one_cycle(3, 1e-3)


# In[ ]:


lm.fit_one_cycle(3, 1e-3)


# ## Preprocess the dataset for classification

# In[ ]:


spacy_tok = SpacyTokenizer("en")
tokenizer = Tokenizer(spacy_tok)


# In[ ]:


df_pretrain.Text.apply(lambda x: len(tokenizer.process_text(x, spacy_tok))).describe()


# Note that for simplicity we only use the first token of the entity, this is a point that can be improved.

# In[ ]:


import spacy
nlp = spacy.blank("en")

def get_token_num_by_offset(s, offset):
  s_pre = s[:offset]
  return len(spacy_tok.tokenizer(s_pre))

# note that 'xxunk' is not special in this sense
special_tokens = ['xxbos','xxfld','xxpad', 'xxmaj','xxup','xxrep','xxwrep']


def adjust_token_num(processed, token_num):
  """
  As fastai tokenizer introduces additional tokens, we need to adjust for them.
  """
  counter = -1
  do_unrep = None
  for i, token in enumerate(processed):
    if token not in special_tokens:
      counter += 1
    if do_unrep:
      do_unrep = False
      if processed[i+1] != ".":
        token_num -= (int(token) - 2) # one to account for the num itself
      else:  # spacy doesn't split full stops
        token_num += 1
    if token == "xxrep":
      do_unrep = True
    if counter == token_num:
      return i
  else:
    counter = -1
    for i, t in enumerate(processed):
      if t not in special_tokens:
        counter += 1
      print(i, counter, t)
    raise Exception(f"{token_num} is out of bounds ({processed})")


# In[ ]:


def dataframe_to_tensors(df, max_len=512):
  # offsets are: pron_tok_offset, a_tok_offset, a_tok_right_offset, b_tok_offset, b_tok_right_offset
  offsets = list()
  labels = np.zeros((len(df),), dtype=np.int64)
  processed = list()
  for i, row in tqdm(df.iterrows()):
    try:
      text = row["Text"]
      a_offset = row["A-offset"]
      a_len = len(nlp(row["A"]))
      
      b_offset = row["B-offset"]
      b_len = len(nlp(row["B"]))

      pron_offset = row["Pronoun-offset"]
      is_a = row["A-coref"]
      is_b = row["B-coref"]
      a_tok_offset = get_token_num_by_offset(text, a_offset)
      b_tok_offset = get_token_num_by_offset(text, b_offset)
      a_right_offset = a_tok_offset + a_len - 1
      b_right_offset = b_tok_offset + b_len - 1
      pron_tok_offset = get_token_num_by_offset(text, pron_offset)
      tokenized = tokenizer.process_text(text, spacy_tok)[:max_len]
      tokenized = ["xxpad"] * (max_len - len(tokenized)) + tokenized  # add padding
      a_tok_offset = adjust_token_num(tokenized, a_tok_offset)
      a_tok_right_offset = adjust_token_num(tokenized, a_right_offset)
      b_tok_offset = adjust_token_num(tokenized, b_tok_offset)
      b_tok_right_offset = adjust_token_num(tokenized, b_right_offset)
      pron_tok_offset = adjust_token_num(tokenized, pron_tok_offset)
      numericalized = vocab.numericalize(tokenized)
      processed.append(torch.tensor(numericalized, dtype=torch.long))
      offsets.append([pron_tok_offset, a_tok_offset, a_tok_right_offset, b_tok_offset, b_tok_right_offset])
      if is_a:
        labels[i] = 0
      elif is_b:
        labels[i] = 1
      else:
        labels[i] = 2
    except Exception as e:
      print(i)
      raise
  processed = torch.stack(processed)
  offsets = torch.tensor(offsets, dtype=torch.long)
  labels = torch.from_numpy(labels)
  return processed, offsets, labels


# In[ ]:


train_ds = TensorDataset(*dataframe_to_tensors(test))
valid_ds = TensorDataset(*dataframe_to_tensors(val))
test_ds = TensorDataset(*dataframe_to_tensors(train))


# In[ ]:


train_dl = DataLoader(train_ds, batch_size=64, shuffle=True)
valid_dl = DataLoader(valid_ds, batch_size=32, shuffle=False)
test_dl = DataLoader(test_ds, batch_size=32, shuffle=False)


# ## Classifier architecture 
# 
# Unfortunately, the magic of fast.ai stops here: we need to create a custom classifier on top. What we do here is:
# 1. Extract hidden states corresponding to entities and the pronoun.
# 2. For each pair (pronoun, entity) we run it through a hidden layer to retrieve a 25-dimensional vector that describes their similarity.
# 3. Concat the vectors.
# 4. Use another layer to turn these into probabilities.

# In[ ]:


lm.freeze()


# In[ ]:


encoder_hidden_sz = 400

device = torch.device("cuda")

class CorefResolver(nn.Module):
  def __init__(self, encoder, dropout_p=0.3):
    super(CorefResolver, self).__init__()
    self.encoder = encoder
    self.dropout = nn.Dropout(dropout_p)
    self.hidden2hidden = nn.Linear(encoder_hidden_sz * 2 + 1, 25)
    self.hidden2logits = nn.Linear(50, 3)
    self.relu = nn.ReLU()
    self.activation = nn.LogSoftmax(dim=1)
    self.loss = nn.NLLLoss()
    
  def forward(self, seqs, offsets, labels=None):
    encoded = self.dropout(self.encoder(seqs)[0][2])
    a_q = list()
    b_q = list()
    for enc, offs in zip(encoded, offsets):
      # extract the hidden states that correspond to A, B and the pronoun, and make pairs of those 
      a_repr = enc[offs[2]]
      b_repr = enc[offs[4]]
      a_q.append(torch.cat([enc[offs[0]], a_repr, torch.dot(enc[offs[0]], a_repr).unsqueeze(0)]))
      b_q.append(torch.cat([enc[offs[0]], b_repr, torch.dot(enc[offs[0]], b_repr).unsqueeze(0)]))
    a_q = torch.stack(a_q)
    b_q = torch.stack(b_q)
    # apply the same "detector" layer to both batches of pairs
    is_a = self.relu(self.dropout(self.hidden2hidden(a_q)))
    is_b = self.relu(self.dropout(self.hidden2hidden(b_q)))
    # concatenate outputs of the "detector" layer to get the final probability distribution
    is_a_b = torch.cat([is_a, is_b], dim=1)
    is_logits = self.hidden2logits(self.dropout(self.relu(is_a_b)))

    activation = self.activation(is_logits)
    if labels is not None:
      return activation, self.loss(activation, labels)
    else:
      return activation


# In[ ]:


enc = lm.model[0]


# In[ ]:


resolver = CorefResolver(enc)


# In[ ]:


resolver.to(device)


# In[ ]:


for param in resolver.encoder.parameters():
  param.requires_grad = False


# In[ ]:


lr = 0.001

loss_fn = nn.NLLLoss()
optimizer = torch.optim.Adam(resolver.parameters(), lr=lr)


# In[ ]:


from sklearn.metrics import classification_report


# ## Define the training loop 

# In[ ]:


def train_epoch(model, optimizer, train_dl, report_every=10):
  model.train()
  step = 0
  total_loss = 0
  
  for texts, offsets, labels in train_dl:
    texts, offsets, labels = texts.to(device), offsets.to(device), labels.to(device)
    step += 1
    optimizer.zero_grad()
    _, loss = model(texts, offsets, labels)
    total_loss += loss.item()
    
    loss.backward()
    optimizer.step()
    
    if step % report_every == 0:
      print(f"Step {step}, loss: {total_loss/report_every}")
      total_loss = 0
      
def evaluate(model, optimizer, valid_dl, probas=False):
  probas = list()
  model.eval()
  predictions = list()
  total_loss = 0
  all_labels = list()
  with torch.no_grad():
    for texts, offsets, labels in valid_dl:
      texts, offsets, labels = texts.cuda(), offsets.cuda(), labels.cuda()
      preds, loss = model(texts, offsets, labels)
      total_loss += loss.item()
      probas.append(preds.cpu().detach().numpy())
      predictions.extend([i.item() for i in preds.max(1)[1]])
    
    
  print(f"Validation loss: {total_loss/len(valid_dl)}")
  print()
  print(classification_report(valid_dl.dataset.tensors[2].numpy(), predictions))
  if probas:
    return total_loss, np.vstack(probas)
  return total_loss, predictions


# ## Train 

# In[ ]:


total_epoch = 0
best_loss = 1e6

for i in range(3):
  print("Epoch", i + 1)
  total_epoch += 1
  train_epoch(resolver, optimizer, train_dl) 
  loss, labels = evaluate(resolver, optimizer, valid_dl)
  if loss < best_loss:
    best_loss = loss
    print(f"Loss improved, saving {total_epoch}")
    torch.save(resolver.state_dict(), data_path/"model_best.pt")


# Unfreeze the encoder and do fine-tuning. We do the finetuning until the model starts to recognize class `2`.

# In[ ]:


for param in resolver.encoder.parameters():
  param.requires_grad = True


# In[ ]:


lr = 3e-4
optimizer = torch.optim.Adam(resolver.parameters(), lr=lr)


# In[ ]:


for i in range(6):
  print("Epoch", i + 1)
  total_epoch += 1
  train_epoch(resolver, optimizer, train_dl)
  loss, labels = evaluate(resolver, optimizer, valid_dl)
  if loss < best_loss:
    best_loss = loss
    print(f"Loss improved, saving {total_epoch}")
    torch.save(resolver.state_dict(), data_path/"model_best.pt")


# ## Fin: get the predictions and submit!

# In[ ]:


resolver.load_state_dict(torch.load(data_path/"model_best.pt"))


# In[ ]:


loss, res = evaluate(resolver, optimizer, test_dl, True)
res_s = np.exp(res)  # don't forget that we have log-softmax outputs:
submission = pd.DataFrame(res_s, index=train["ID"], columns=["A", "B", "NEITHER"])
submission.to_csv("submission.csv", index="id")

