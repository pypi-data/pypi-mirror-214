import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
import numpy as np

class Classifier:   
    def __init__(self, X, Y, test_size=0.2, random_state=20):
        self.X = X
        self.Y = Y
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=test_size, stratify=Y, random_state=random_state)
        self.model = [
            LogisticRegression(), KNeighborsClassifier(), GaussianNB(),
            BaggingClassifier(), ExtraTreesClassifier(),
            RidgeClassifier(), SGDClassifier(), RandomForestClassifier(),
            xgb.XGBClassifier(), AdaBoostClassifier(), BernoulliNB(),
            GradientBoostingClassifier(), DecisionTreeClassifier(), SVC()
        ]
        self.model_name = [
            'Logistic Regression', 'KNeighborsClassifier', 'GaussianNB',
            'BaggingClassifier', 'ExtraTreesClassifier', 'RidgeClassifier', 'SGDClassifier',
            'RandomForestClassifier', 'XGBClassifier', 'AdaBoostClassifier',
            'BernoulliNB', 'GradientBoostingClassifier', 'DecisionTreeClassifier', 'SVC'
        ]
        self.model_table = pd.DataFrame(columns=['model name', 'accuracy', 'confusion', 'roc', 'f1', 'recall', 'precision'])

    def model_accuracy(self, y_test_f, y_pred_f, model_name):
        acc = accuracy_score(y_test_f, y_pred_f)
        confusion = confusion_matrix(y_test_f, y_pred_f)
        roc = roc_auc_score(y_test_f, y_pred_f)
        f1 = f1_score(y_test_f, y_pred_f)
        recall = recall_score(y_test_f, y_pred_f)
        precision = precision_score(y_test_f, y_pred_f)
        return {'model name': model_name, 'accuracy': acc, 'confusion': confusion, 'roc': roc, 'f1': f1, 'recall': recall, 'precision': precision}

    def model_training(self):
        for model, model_name in zip(self.model, self.model_name):
            model.fit(self.X_train, self.Y_train)
            y_pred = model.predict(self.X_test)
            model_result = self.model_accuracy(self.Y_test, y_pred, model_name)
            self.model_table = self.model_table.append(model_result, ignore_index=True)
        return self.model_table