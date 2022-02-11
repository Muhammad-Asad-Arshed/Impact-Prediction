# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 00:51:56 2019

@author: Maharvi
"""
from colorama import Fore, Back, Style 
import pandas as pd
from sklearn.svm import SVC 
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,confusion_matrix, classification_report
from collections import Counter
from imblearn.over_sampling import ADASYN
df = pd.read_excel('SecondaryDataSet_PCA.xlsx',encoding='latin-1')  
df2 = df[['Positive','Negative','Neutral','Status']]
X = df2.drop('Status', axis=1)  
y = df2['Status']
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=88)
#good one is that Sampling should applied after spliting dataset means it applied on training data just 
print("Before Oversampling=",Counter(y_train))
ad = ADASYN(random_state=88)
x_train_res, y_train_res = ad.fit_sample(X_train_raw, y_train)
print("After Oversampling=",Counter(y_train_res))
params_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]},{'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
svm_model = GridSearchCV(SVC(), params_grid, cv=5)
svm_model.fit(x_train_res, y_train_res)
predictions = svm_model.predict(X_test_raw)
ac=accuracy_score(y_test, predictions)
#View the best parameters for the model found using grid search
print('Best C:',svm_model.best_estimator_.C) 
print('Best Kernel:',svm_model.best_estimator_.kernel)
print('Best Gamma:',svm_model.best_estimator_.gamma)
print('Best score for training data:', round(svm_model.best_score_,4) )
print (Fore.WHITE+Style.BRIGHT+Back.BLACK+'**********Best score for test data:', round(accuracy_score(y_test, predictions),4),"**********"+Style.RESET_ALL)
print ('F1 score:', round(f1_score(y_test, predictions,average='weighted'),4))
print ('Recall:', round(recall_score(y_test,predictions,average='weighted'),4))
print ('Precision:', round(precision_score(y_test,predictions,average='weighted'),4))
print ('clasification report:\n', classification_report(y_test,predictions))
print ('confussion matrix:\n',confusion_matrix(y_test,predictions))