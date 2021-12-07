import os
import numpy as np
import pandas as pd
from hwp_parsing import get_train_vector
from hwp_parsing import get_test_vector
from hwp_parsing import get_file_list_from_dir
from hwp_parsing import make_total_file_list
#evaluation
from sklearn.model_selection import StratifiedKFold
import sklearn.metrics as metrics

#model import
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
import dataframe_image as dfi
from sklearn.model_selection import train_test_split, GridSearchCV

def parameter_tuning(X_file_data,y_file_data,param, model):
    X_file_train, X_file_test, y_file_train, y_file_test = train_test_split(X_file_data,y_file_data, test_size=0.2, random_state=121)
    X_train, y_train, total_feature = get_train_vector(X_file_train,y_file_train)
    X_test, y_test = get_test_vector(X_file_test, y_file_test,total_feature)
    grid_cv = GridSearchCV(model, param_grid=param, cv=5, n_jobs=-1)
    grid_cv.fit(X_train, y_train)
    print("최적의 하이퍼 파라미터: ", grid_cv.best_params_)
    print("최고의 예측 정확도: ", grid_cv.best_score_)
    return grid_cv.best_estimator_

def cross_val_evaluation(X_file_data,y_file_data,model):
    all_acc=[]
    all_f1=[]
    all_precision=[]
    all_recall=[]
    all_auc=[]
    skf = StratifiedKFold(n_splits=5)
    for train_index, test_index in skf.split(X_file_data,y_file_data):
        X_file_train = X_file_data[train_index]
        y_file_train = y_file_data[train_index]  
        X_file_test = X_file_data[test_index]
        y_file_test = y_file_data[test_index]
        X_train, y_train, total_feature = get_train_vector(X_file_train,y_file_train)
        
        X_test, y_test = get_test_vector(X_file_test, y_file_test,total_feature)

        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        
        acc=metrics.accuracy_score(y_test, y_pred)
        all_acc.append(acc)
    
        f1=metrics.f1_score(y_test, y_pred)
        all_f1.append(f1)
    
        precision=metrics.precision_score(y_test, y_pred)
        all_precision.append(precision)
    
        recall=metrics.recall_score(y_test, y_pred)
        all_recall.append(recall)
    
        auc=metrics.roc_auc_score(y_test, y_pred)
        all_auc.append(auc)
        
        #print(confusion_matrix(y_test,y_pred))
    acc_mean = np.mean(np.array(all_acc))
    f1_mean = np.mean(np.array(all_f1))
    precision_mean = np.mean(np.array(all_precision))
    recall_mean = np.mean(np.array(all_recall))
    auc_mean = np.mean(np.array(all_auc))
    return acc_mean,f1_mean,precision_mean,recall_mean,auc_mean

if __name__ == "__main__":
    ben_files = get_file_list_from_dir("/home/ggabi/sumin/data/hwp/ben")
    mal_files = get_file_list_from_dir("/home/ggabi/sumin/data/hwp/mal")
    X_file_data, y_file_data =make_total_file_list(ben_files,mal_files)

    rf_params = {
    'criterion': ["gini", "entropy"],
    'max_depth': [8, 10, 12],
    'max_features': ['auto','sqrt'],
    'min_samples_leaf': [2, 4, 6, 8],
    'min_samples_split': [12, 14, 16],  
    'n_estimators': [100,200]
    }
    rf_best_estimator=parameter_tuning(X_file_data,y_file_data,rf_params, RandomForestClassifier())

    dt_params = {
    'criterion': ["gini", "entropy"],
    'max_depth': [6,8,10],
    "max_features":["auto","log2","sqrt",None],
    "max_leaf_nodes":[None,10,20,30],
    'min_samples_leaf': [4, 6 ,8],
    'min_samples_split': [8,10, 12, 14]
    
    }
    dt_best_estimator=parameter_tuning(X_file_data,y_file_data,dt_params, tree.DecisionTreeClassifier())

    svm_params = [
    {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
    {'C': [1, 10, 100, 1000], 'gamma': [0.1,0.01,0.001], 'kernel': ['rbf']},
    ]
    svm_best_estimator=parameter_tuning(X_file_data,y_file_data,svm_params, svm.SVC(probability=True ))

    nb_params = {
    'var_smoothing': np.logspace(0,-9, num=100)
    }
    nb_best_estimator=parameter_tuning(X_file_data,y_file_data,nb_params, GaussianNB())


    graph={}
    #성능평가
    model_list = [rf_best_estimator,svm_best_estimator,dt_best_estimator,nb_best_estimator]
    model_name =['RandomForestClassifier','svm.SVC','DecisionTreeClassifier','GaussianNB']
    for model,model_name in zip(model_list,model_name):
        graph[model_name] = cross_val_evaluation(X_file_data, y_file_data,model)
    df = pd.DataFrame(data = graph, index=['The average value of accuracy','The average value of f1 score','The average value of precision','The average value of recall','The average value of auc'])
    dfi.export(df, 'hwp_evaluation1.png')

    graph2={}
    vo_clf = VotingClassifier(estimators=[('svm',svm_best_estimator),('dt',dt_best_estimator)], voting='soft')
    bg_100_svm = BaggingClassifier(base_estimator=svm_best_estimator,n_estimators=100,n_jobs=-1,)
    bg_200_svm = BaggingClassifier(base_estimator=svm_best_estimator,n_estimators=200,n_jobs=-1,)
    bg_100_dt = BaggingClassifier(base_estimator=dt_best_estimator,n_estimators=100,n_jobs=-1,)
    bg_200_dt = BaggingClassifier(base_estimator=dt_best_estimator,n_estimators=200,n_jobs=-1,)
    graph2['soft voting(svm,dt)']=cross_val_evaluation(X_file_data, y_file_data,vo_clf)
    graph2['svm_bagging clf(estimators-100)']=cross_val_evaluation(X_file_data, y_file_data,bg_100_svm)
    graph2['dt_bagging clf(estimators-100)']=cross_val_evaluation(X_file_data, y_file_data,bg_100_dt)
    graph2['svm_bagging clf(estimators-200)']=cross_val_evaluation(X_file_data, y_file_data,bg_200_svm)
    graph2['dt_bagging clf(estimators-200)']=cross_val_evaluation(X_file_data, y_file_data,bg_200_dt)


    df = pd.DataFrame(data = graph2, index=['The average value of accuracy','The average value of f1 score','The average value of precision','The average value of recall','The average value of auc'])
    dfi.export(df, 'hwp_evaluation2.png')
    
    



