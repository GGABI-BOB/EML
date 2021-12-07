import os
import numpy as np
from pdf import generate_feature_vector_pdf
#evaluation
import sklearn.metrics as metrics

#model import
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
import joblib
import pickle
from imblearn.over_sampling import SMOTE

def training(X_data,y_data,model):
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=777, stratify=y_data)
    sm = SMOTE()
    X_train, y_train = sm.fit_resample(X_train, y_train)
    model.fit(X_train,y_train)
    joblib.dump(model, '/home/ggabi/sumin/model/pdf/pdf_model.pkl') 
    y_pred = model.predict(X_test)
    acc=metrics.accuracy_score(y_test, y_pred)
    f1=metrics.f1_score(y_test, y_pred)
    precision=metrics.precision_score(y_test, y_pred)
    recall=metrics.recall_score(y_test, y_pred)
    auc=metrics.roc_auc_score(y_test, y_pred)

    return acc,f1,precision,recall,auc

def predict_pdf(file_path,filename):
    model = joblib.load('/home/ggabi/sumin/model/pdf/pdf_model.pkl')
    X_test = np.array([generate_feature_vector_pdf.extract(file_path+filename)])
    return model.predict_proba(X_test)[:,1]

    
    

   

    

