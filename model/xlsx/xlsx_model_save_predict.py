import os
import numpy as np
from xlsx import xlsx_parser
#evaluation
import sklearn.metrics as metrics

#model import
from sklearn import svm
from sklearn import tree
from sklearn.model_selection import train_test_split
import joblib
import pickle

def training(X_file_data,y_file_data,model):
    X_file_train, X_file_test, y_file_train, y_file_test = train_test_split(X_file_data, y_file_data, test_size=0.2, random_state=777, stratify=y_file_data) 
    X_train, y_train, total_feature = xlsx_parser.get_train_vector(X_file_train,y_file_train)
    X_test, y_test = xlsx_parser.get_test_vector(X_file_test, y_file_test,total_feature)
    X_data = np.concatenate((X_train,X_test), axis=0)
    y_data = np.concatenate((y_train,y_test), axis=0)
    with open('/home/ggabi/sumin/model/xlsx/xlsx_X_data.pkl', 'wb') as file:
        pickle.dump(X_data,file)
    with open('/home/ggabi/sumin/model/xlsx/xlsx_Y_data.pkl', 'wb') as file:
        pickle.dump(y_data,file)
    model.fit(X_train,y_train)
    with open('/home/ggabi/sumin/model/xlsx/xlsx_feature.pkl', 'wb') as file:
        pickle.dump(total_feature,file)
    joblib.dump(model, '/home/ggabi/sumin/model/xlsx/xlsx_model.pkl') 
    y_pred = model.predict(X_test)
    acc=metrics.accuracy_score(y_test, y_pred)
    f1=metrics.f1_score(y_test, y_pred)
    precision=metrics.precision_score(y_test, y_pred)
    recall=metrics.recall_score(y_test, y_pred)
    auc=metrics.roc_auc_score(y_test, y_pred)
    return  acc,f1,precision,recall,auc

def predict_xlsx(file_path,filename):
    model = joblib.load('/home/ggabi/sumin/model/xlsx/xlsx_model.pkl')
    with open('/home/ggabi/sumin/model/xlsx/xlsx_feature.pkl', 'rb') as file:
        feature = pickle.load(file)
    X_test = np.array(xlsx_parser.make_feature_vec(file_path, [filename], feature))
    if len(X_test)==0:
        return ['zip 변환 실패']
    return model.predict_proba(X_test)[:,1]



    

   

    

