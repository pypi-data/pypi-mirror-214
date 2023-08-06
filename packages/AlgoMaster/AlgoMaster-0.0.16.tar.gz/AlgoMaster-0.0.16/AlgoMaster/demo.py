import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from classifier import Classifier

diabetes_dataset = pd.read_csv('F:\packagesPyPi\AlgoMaster\diabetes.csv')
X = diabetes_dataset.drop(["Pregnancies","BloodPressure","SkinThickness","Outcome"], axis=1)
Y = diabetes_dataset['Outcome']
clg=Classifier(X,Y,0.2,42)
print(clg.model_training())
print(clg.ensemble_prediction(4))

data=(148,0,33.6,0.627,50)
pred, acc=clg.AdaBoost_test(data)
print(pred)
print(acc)

pred,acc =clg.logistic_test(data)
print(pred)
print(acc)

pred,acc =clg.KNeighbors_test(data)
print(pred)
print(acc)

pred,acc =clg.GaussianNB_test(data)
print(pred)
print(acc)

pred,acc =clg.Bagging_test(data)
print(pred)
print(acc)

pred,acc =clg.ExtraTrees_test(data)
print(pred)
print(acc)

pred,acc =clg.Ridge_test(data)
print(pred)
print(acc)

pred,acc =clg.SGD_test(data)
print(pred)
print(acc)

pred,acc =clg.RandomForest_test(data)
print(pred)
print(acc)

pred,acc =clg.XGB_test(data)
print(pred)
print(acc)

pred,acc =clg.GaussianNB_test(data)
print(pred)
print(acc)

pred,acc =clg.GradientBoosting_test(data)
print(pred)
print(acc)

pred,acc =clg.DecisionTree_test(data)
print(pred)
print(acc)

pred,acc =clg.SVC_test(data)
print(pred)
print(acc)