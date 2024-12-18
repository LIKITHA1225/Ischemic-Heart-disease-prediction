# -*- coding: utf-8 -*-
"""DNN with Feature Selection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eUvziWX9A1vjsVcBVRZ5sSW7HdXwxkmB
"""

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input
from keras.utils import np_utils

dataset = pd.read_csv('heart.csv')

dataset.head()

X = dataset.iloc[:, 3:-1].values
Y = dataset.iloc[:, -1].values

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
X_train.shape, Y_train.shape, X_test.shape, Y_test.shape

dataset.duplicated().sum()

dataset[dataset.duplicated()]

duplicated_features = dataset[dataset.duplicated()].index.values
print(duplicated_features)

unique_df = dataset.drop_duplicates(keep='first').T
unique_df.shape

removed_features = [col for col in dataset.columns if col not in unique_df.columns]
removed_features

from sklearn.feature_selection import VarianceThreshold
feature_selector = VarianceThreshold(threshold=0)
feature_selector.fit(X_train)

feature_selector.get_support()

sum(feature_selector.get_support())

X_train = feature_selector.transform(X_train)
X_test = feature_selector.transform(X_test)
X_train.shape, X_test.shape

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

model = Sequential()
model.add(Dense(12, input_dim=10, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history=model.fit(X, Y, epochs=60, batch_size=32)

history.history.keys()

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train'],loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train'],loc='upper left')
plt.show()

predictions = (model.predict(X) > 0.5).astype(int)
for i in range(5):
	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], Y[i]))

_, accuracy = model.evaluate(X, Y)
print('Accuracy: %.2f' % (accuracy*100))

y_pred = model.predict(X_test)
y_pred=(y_pred>0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), Y_test.reshape(len(Y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(Y_test, y_pred)
print(cm)
accuracy_score(Y_test, y_pred)

TP = cm[1][1]
TN = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
print('True Positives:', TP)
print('True Negatives:', TN)
print('False Positives:', FP)
print('False Negatives:', FN)
conf_accuracy = (float (TP+TN) / float(TP + TN + FP + FN))
conf_misclassification = 1- conf_accuracy
conf_sensitivity = (TP / float(TP + FN))
conf_specificity = (TN / float(TN + FP))
conf_precision = (TN / float(TN + FP))
conf_f1 = 2 * ((conf_precision * conf_sensitivity) / (conf_precision + conf_sensitivity))
print('-'*50)
print(f'Accuracy: {round(conf_accuracy,2)}')
print(f'Mis-Classification: {round(conf_misclassification,2)}')
print(f'Sensitivity: {round(conf_sensitivity,2)}')
print(f'Specificity: {round(conf_specificity,2)}')
print(f'Precision: {round(conf_precision,2)}')
print(f'f_1 Score: {round(conf_f1,2)}')