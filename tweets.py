# -*- coding: utf-8 -*-
"""tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XmF6HEjbkKDEb0GJG3sKKcmBh9MPXnZk
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

import nltk
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence #unique id

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout, Embedding
import warnings
warnings.filterwarnings("ignore")



df=pd.read_csv("/content/tweets.csv")

df

df.head()

df["keyword"].value_counts()

!pip install emot

df.drop(["id","keyword","location"],axis=1,inplace=True)

df

def cleantext(text):
  tokens = word_tokenize(text.lower())
  ftoken = [t for t in tokens if(t.isalpha())]
  stop = stopwords.words("english")
  ctoken = [t for t in ftoken if(t not in stop)]
  lemma = WordNetLemmatizer()
  ltoken = [lemma.lemmatize(t) for t in ctoken]
  return " ".join(ltoken)

df["clean_text"]=df["text"].apply(cleantext)

x = df["clean_text"]
y = df["target"]

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=1)

sentlen = []

for sent in df["clean_text"]:
  sentlen.append(len(word_tokenize(sent)))

df["SentLen"] = sentlen 
df.head()

max(sentlen)

np.quantile(sentlen, 0.95)

max_len = np.quantile(sentlen, 0.95)

tok = Tokenizer(char_level=False, split=" ")
#char_level	if True, every character will be treated as a token.

tok.fit_on_texts(xtrain)
tok.index_word

vocab_len = len(tok.index_word)
vocab_len

seqtrain = tok.texts_to_sequences(xtrain) #step1
seqtrain

seqmattrain = sequence.pad_sequences(seqtrain, maxlen= int(max_len)) #step2
seqmattrain

seqtest = tok.texts_to_sequences(xtest)
seqmattest = sequence.pad_sequences(seqtest, maxlen=int(max_len))

vocab_len

rnn = Sequential()

rnn.add(Embedding(vocab_len+1,700, input_length=int(max_len), mask_zero=True))
rnn.add(SimpleRNN(units=32, activation="tanh"))
rnn.add(Dense(units=32, activation="relu"))
rnn.add(Dropout(0.2))

rnn.add(Dense(units=1, activation="sigmoid"))

rnn.compile(optimizer="adam", loss="binary_crossentropy")

rnn.fit(seqmattrain, ytrain, batch_size=50, epochs=25)

ypred = rnn.predict(seqmattest)

ypred = ypred>0.5

from sklearn.metrics import classification_report
print(classification_report(ytest,ypred))

