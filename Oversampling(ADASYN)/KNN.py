# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 08:02:00 2019

@author: Maharvi
"""
from colorama import Fore, Back, Style 
import pandas as pd
from sklearn.svm import SVC 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,confusion_matrix, classification_report
from collections import Counter
from imblearn.over_sampling import ADASYN
df = pd.read_excel('SecondaryDataSet_PCA.xlsx',encoding='latin-1')  
df2 = df[['Positive','Negative','Neutral','Status']]
X = df2.drop('Status', axis=1)  
y = df2['Status']
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=88)
knn=KNeighborsClassifier()
print("Before Oversampling=",Counter(y_train))
ad = ADASYN(random_state=88)
x_train_res, y_train_res = ad.fit_sample(X_train_raw, y_train)
print("After Oversampling=",Counter(y_train_res))
k_range=range(1,31)
param_grid = dict({'n_neighbors':k_range,
              'algorithm':['auto', 'ball_tree', 'kd_tree', 'brute']
              })
grid = GridSearchCV(knn, param_grid, cv=5)
grid.fit(x_train_res, y_train_res)
predictions = grid.predict(X_test_raw)
print(grid.best_params_)
print('Best score for training data:', round(grid.best_score_,4)) 
print (Fore.WHITE+Style.BRIGHT+Back.BLACK+'Best score for test data/Test Accuracy:', round(accuracy_score(y_test, predictions),4)," "+Style.RESET_ALL)
print ('F1 score:', round(f1_score(y_test, predictions,average='weighted'),4))
print ('Recall:', round(recall_score(y_test,predictions,average='weighted'),4))
print ('Precision:',round(precision_score(y_test,predictions,average='weighted'),4))
print ('clasification report:\n', classification_report(y_test,predictions))
print ('confussion matrix:\n',confusion_matrix(y_test,predictions))