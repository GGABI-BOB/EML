import os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import *

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
import dataframe_image as dfi
from sklearn.model_selection import train_test_split, GridSearchCV

def parameter_tuning(X_data,y_data,param, model):
    grid_cv = GridSearchCV(model, param_grid=param, cv=5, n_jobs=-1,verbose=2,scoring='f1_micro')
    grid_cv.fit(X_data, y_data)
    print("최적의 하이퍼 파라미터: ", grid_cv.best_params_)
    print("최고의 예측 정확도: ", grid_cv.best_score_)
    return grid_cv.best_estimator_

def cross_val_evaluation(X_data,y_data,model):
    all_acc=[]
    all_f1=[]
    all_precision=[]
    all_recall=[]
    all_auc=[]
    skf = StratifiedKFold(n_splits=5)
    for train_index, test_index in skf.split(X_data,y_data):
        sm = SMOTE()
        X_train = X_data[train_index]
        y_train = y_data[train_index]
        X_train, y_train = sm.fit_resample(X_train, y_train)
        X_test = X_data[test_index]
        y_test = y_data[test_index]
    

        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        
        acc=accuracy_score(y_test, y_pred)
        all_acc.append(acc)
    
        f1=f1_score(y_test, y_pred)
        all_f1.append(f1)
    
        precision=precision_score(y_test, y_pred)
        all_precision.append(precision)
    
        recall=recall_score(y_test, y_pred)
        all_recall.append(recall)
    
        auc=roc_auc_score(y_test, y_pred)
        all_auc.append(auc)
        
    acc_mean = np.mean(np.array(all_acc))
    f1_mean = np.mean(np.array(all_f1))
    precision_mean = np.mean(np.array(all_precision))
    recall_mean = np.mean(np.array(all_recall))
    auc_mean = np.mean(np.array(all_auc))
    return [acc_mean,f1_mean,precision_mean,recall_mean,auc_mean]



if __name__ == "__main__":
   
    X_data = np.load('/home/ggabi/sumin/model/pdf/pdf_X_data.npy', allow_pickle=True)
    y_data = np.load('/home/ggabi/sumin/model/pdf/pdf_Y_data.npy', allow_pickle=True)



    # print("Test Precision:",precision_score(gs.predict(X_test), y_test))
    # print("Test Recall:",recall_score(gs.predict(X_test), y_test))
    # print("Test ROC AUC Score:",roc_auc_score(gs.predict(X_test), y_test))


    # graph={}
    # model_list = [rf_best_estimator,svm_best_estimator,dt_best_estimator,nb_best_estimator]
    # model_list = [RandomForestClassifier(),tree.DecisionTreeClassifier(),svm.SVC(probability=True ),GaussianNB()]
    # model_name =['RandomForestClassifier','svm.SVC','DecisionTreeClassifier','GaussianNB']
    # for model,model_name in zip(model_list,model_name):
    #     graph[model_name] = cross_val_evaluation(X_data, y_data,model)
    # df = pd.DataFrame(data = graph, index=['The average value of accuracy','The average value of f1 score','The average value of precision','The average value of recall','The average value of auc'])
    # dfi.export(df, 'pdf_evaluation1.png')

    # graph2={}

    # vo_clf = VotingClassifier(estimators=[('svm',svm_best_estimator),('dt',dt_best_estimator)], voting='soft')
    # bg_100_svm = BaggingClassifier(base_estimator=svm_best_estimator,n_estimators=100,n_jobs=-1,)
    # bg_200_svm = BaggingClassifier(base_estimator=svm_best_estimator,n_estimators=200,n_jobs=-1,)
    # bg_100_dt = BaggingClassifier(base_estimator=dt_best_estimator,n_estimators=100,n_jobs=-1,)
    # bg_200_dt = BaggingClassifier(base_estimator=dt_best_estimator,n_estimators=200,n_jobs=-1,)
    # graph2['soft voting(svm,dt)']=cross_val_evaluation(X_data, y_data,vo_clf)
    # graph2['svm_bagging clf(estimators-100)']=cross_val_evaluation(X_data, y_data,bg_100_svm)
    # graph2['dt_bagging clf(estimators-100)']=cross_val_evaluation(X_data, y_data,bg_100_dt)
    # graph2['svm_bagging clf(estimators-200)']=cross_val_evaluation(X_data, y_data,bg_200_svm)
    # graph2['dt_bagging clf(estimators-200)']=cross_val_evaluation(X_data, y_data,bg_200_dt)


    # df = pd.DataFrame(data = graph2, index=['The average value of accuracy','The average value of f1 score','The average value of precision','The average value of recall','The average value of auc'])
    # dfi.export(df, 'pdf_evaluation2.png')


