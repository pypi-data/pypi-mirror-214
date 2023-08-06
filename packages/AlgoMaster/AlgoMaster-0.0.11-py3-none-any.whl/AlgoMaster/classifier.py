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
from heapq import nlargest

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

    @staticmethod
    def format_input_data(data):
        if isinstance(data, np.ndarray):
            if data.ndim == 2 and data.shape[0] == 1:
                return data
            else:
                return data.reshape(1, -1)
        else:
            return np.asarray(data).reshape(1, -1)
        
    def model_accuracy(self, y_test_f, y_pred_f, model_name):
        acc = accuracy_score(y_test_f, y_pred_f)
        confusion = confusion_matrix(y_test_f, y_pred_f)
        roc = roc_auc_score(y_test_f, y_pred_f)
        f1 = f1_score(y_test_f, y_pred_f)
        recall = recall_score(y_test_f, y_pred_f)
        precision = precision_score(y_test_f, y_pred_f)
        return {'model name': model_name, 'accuracy': acc, 'confusion': confusion, 'roc': roc, 'f1': f1, 'recall': recall, 'precision': precision}

    def model_training(self):
        model_results = []
        for model, model_name in zip(self.model, self.model_name):
            model.fit(self.X_train, self.Y_train)
            y_pred = model.predict(self.X_test)
            model_result = pd.DataFrame([self.model_accuracy(self.Y_test, y_pred, model_name)])
            model_results.append(model_result)

        self.model_table = pd.concat(model_results, ignore_index=True)
        self.model_table = self.model_table.sort_values('accuracy', ascending=False)
        self.model_table.reset_index(drop=True, inplace=True)
        return self.model_table
    
    def ensemble_prediction(self, count):
        top_models = nlargest(count, self.model_table.iterrows(), key=lambda x: x[1]['accuracy'])
        ensemble_predictions = []
        for _, model_row in top_models:
            model_index = self.model_name.index(model_row['model name'])
            model = self.model[model_index]
            y_pred = model.predict(self.X_test)
            ensemble_predictions.append((model_index, y_pred))
        majority_vote = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=np.array([y_pred for _, y_pred in ensemble_predictions]))
        return self.model_accuracy(self.Y_test, majority_vote, 'Ensemble')
    
    def logistic_test(self, pred):
        pred=self.format_input_data(pred)
        model = LogisticRegression()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'Logistic Regression')
    
    def KNeighbors_test(self, pred):
        pred=self.format_input_data(pred)
        model = KNeighborsClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'KNeighborsClassifier')
        
    def GaussianNB_test(self, pred):
        pred=self.format_input_data(pred)
        model = GaussianNB()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'GaussianNB')
    
    def Bagging_test(self, pred):
        pred=self.format_input_data(pred)
        model = BaggingClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'BaggingClassifier')
        
    def ExtraTrees_test(self,pred):
        pred=self.format_input_data(pred)
        model = ExtraTreesClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'ExtraTreesClassifier')
    
    def Ridge_test(self, pred):
        pred=self.format_input_data(pred)
        model = RidgeClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'RidgeClassifier')
    
    def SGD_test(self,pred):
        pred=self.format_input_data(pred)
        model = SGDClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'SGDClassifier')
    
    def RandomForest_test(self,pred):
        pred=self.format_input_data(pred)
        model = RandomForestClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'RandomForestClassifier')
    
    def XGB_test(self,pred):
        pred=self.format_input_data(pred)
        model = xgb.XGBClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'XGBClassifier')
    
    def AdaBoost_test(self,pred):
        pred=Classifier.format_input_data(pred)
        model = AdaBoostClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'AdaBoostClassifier')
    
    def BernoulliNB_test(self,pred):
        pred=self.format_input_data(pred)
        model = BernoulliNB()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'BernoulliNB')
    
    def GradientBoosting_test(self, pred):
        pred=self.format_input_data(pred)
        model = GradientBoostingClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict=model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'GradientBoostingClassifier')
    
    def DecisionTree_test(self,pred):
        pred=self.format_input_data(pred)
        model = DecisionTreeClassifier()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'DecisionTreeClassifier')

    def SVC_test(self,pred):
        pred=self.format_input_data(pred)
        model = SVC()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(pred)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, 'SVC')
        
    
    
        