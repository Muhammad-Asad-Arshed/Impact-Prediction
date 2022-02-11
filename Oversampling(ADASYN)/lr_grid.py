# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 09:55:31 2019

@author: Maharvi
"""

from colorama import Fore, Back, Style 
import pandas as pd
from sklearn.svm import SVC 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,confusion_matrix, classification_report
from imblearn.over_sampling import ADASYN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from collections import Counter
df = pd.read_excel('SecondaryDataSet_PCA.xlsx',encoding='latin-1')  
df2 = df[['Positive','Negative','Neutral','Status']]
X = df2.drop('Status', axis=1)  
y = df2['Status'] 
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=88)
print(Counter(y_train))
ad = ADASYN(random_state=88)
x_train_res, y_train_res = ad.fit_sample(X_train_raw, y_train)
print(Counter(y_train_res))
solver_options = ['newton-cg', 'lbfgs', 'sag', 'saga']
multi_class_options = ['multinomial','ovr','auto']
co=[1, 10, 100, 1000]
param_grid = dict(solver = solver_options, multi_class = multi_class_options,C=co)
lr=LogisticRegression();
grid = GridSearchCV(lr, param_grid, cv=5)
grid.fit(x_train_res, y_train_res)
predictions = grid.predict(X_test_raw)    
#View the best parameters for the model found using grid search
print('Best C:',grid.best_estimator_.C) 
print('Best Solver:',grid.best_estimator_.solver)
print('Best multi_class:',grid.best_estimator_.multi_class)
print('Best score for training data:', round(grid.best_score_,4)) 
print (Fore.WHITE+Style.BRIGHT+Back.BLACK+'Best score for test data/Test Accuracy:', round(accuracy_score(y_test, predictions),4)," "+Style.RESET_ALL)
print ('F1 score:', round(f1_score(y_test, predictions,average='weighted'),4))
print ('Recall:', round(recall_score(y_test,predictions,average='weighted'),4))
print ('Precision:',round(precision_score(y_test,predictions,average='weighted'),4))
print ('clasification report:\n', classification_report(y_test,predictions))
print ('confussion matrix:\n',confusion_matrix(y_test,predictions))
