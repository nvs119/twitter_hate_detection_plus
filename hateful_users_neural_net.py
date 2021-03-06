# -*- coding: utf-8 -*-
"""hateful users neural net.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oDJXp1lJi_zbfRaP0wcOudDp19S-BQkU
"""

import pandas as pd

df = pd.read_csv("users_neighborhood_anon.csv")
df

dataset = df.values
dataset

import numpy as np

hateful_users = []

for user in dataset:
  if user[1] != "other":
    hateful_users.append(user)

np_hateful_users = np.array(hateful_users)

from tensorflow.python.ops.math_ops import reduced_shape
num_cols = []

for i in range(2, 1039):
  if isinstance(np_hateful_users[1][i], int):
    num_cols.append(i)
  elif isinstance(np_hateful_users[1][i], float):
    num_cols.append(i)

reduced_stuff = []
norm_count = 0
for i in range(0, len(np_hateful_users)):
  if np_hateful_users[i][1] == "normal":
    if norm_count % 4 == 0: 
      reduced_stuff.append(i)
    norm_count += 1
  elif np_hateful_users[i][1] == "hateful":
    reduced_stuff.append(i)

X = np_hateful_users[reduced_stuff, :][:, num_cols[0:10]]

labels = np_hateful_users[reduced_stuff, :][:, [1]]

binary_labels = []
for label in labels:
  if label == "normal":
    binary_labels.append(0)
  elif label == "hateful":
    binary_labels.append(1)

Y = np.array(binary_labels)

print(len(X))
print(len(Y))

from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)

X_scale

from sklearn.model_selection import train_test_split

X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X_scale, Y, test_size=0.30)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)

print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import tensorflow as tf

model = Sequential([
    Dense(10, activation='relu', input_shape=(10,)),
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid'),
])

opt = tf.keras.optimizers.SGD(learning_rate=0.001)

model.compile(optimizer=opt,
              loss='binary_crossentropy',
              metrics=['accuracy'])

hist = model.fit(X_train, Y_train,
          batch_size=32, epochs=300,
          validation_data=(X_val, Y_val))

model.evaluate(X_test, Y_test)[1]

ones = 0
for thing in Y_test:
  if thing == 1:
    ones += 1

print(ones)
print(len(Y_test))

print(0.97*248)