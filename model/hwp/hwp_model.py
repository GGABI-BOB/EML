import numpy as np
import pickle
import joblib
from model.hwp import hwp_parsing
from sklearn.pipeline import Pipeline

#model import
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV


def hwp_model_training(X_file_data,y_file_data):
    X_data, y_data, total_feature = hwp_parsing.get_train_vector(X_file_data,y_file_data)
    with open('/home/ggabi/sumin/model/hwp/hwp_feature.pkl', 'wb') as file:
        pickle.dump(total_feature,file)
    clf1=RandomForestClassifier()
    clf2=tree.DecisionTreeClassifier()
    clf3=svm.SVC(probability=True )
    clf4=GaussianNB()
    param1 = {}
    param1['classifier__n_estimators'] = [100, 200]
    param1['classifier__max_depth'] = [8, 10, 12, 14]
    param1['classifier__min_samples_split'] = [10, 12, 14, 16]
    param1['classifier__min_samples_leaf'] = [2, 4, 6, 8]
    param1['classifier'] = [clf1]

    param2 = {}
    param2['classifier__max_depth'] =  [6,8,10,12]
    param2['classifier__min_samples_split'] = [8,10, 12, 14]
    param2['classifier__min_samples_leaf'] = [4, 6 ,8]
    param2['classifier'] = [clf2]

    param3 = {}
    param3['classifier__C'] = [1, 10, 100, 1000]
    param3['classifier__gamma']=[0.1,0.01,0.001]
    param3['classifier'] = [clf3]

    param4 = {}
    param4['classifier__var_smoothing'] = np.logspace(0,-9, num=100)
    param4['classifier'] = [clf4]
    
    pipeline = Pipeline([('classifier', clf1)])
    params = [param1, param2, param3, param4]
    gs = GridSearchCV(pipeline, params, cv=5, n_jobs=-1, scoring='f1_micro').fit(X_data, y_data)
    joblib.dump(gs, '/home/ggabi/sumin/model/hwp/hwp_model_gs.pkl')

    return gs.best_params_ , gs.best_score_


def hwp_model_predict(file_path,filename):
    model = joblib.load('/home/ggabi/sumin/model/hwp/hwp_model_gs.pkl')
    with open('/home/ggabi/sumin/model/hwp/hwp_feature.pkl', 'rb') as file:
        feature = pickle.load(file)
    X_test = np.array(hwp_parsing.make_feature_vec(file_path, [filename], feature))
    if len(X_test)==0:
        return ['zip 변환 실패']
    return model.predict_proba(X_test)[:,1]


if __name__ == "__main__":
    
    ben_files = hwp_parsing.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/hwp/ben/")
    mal_files = hwp_parsing.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/hwp/mal/")
    X_file_data, y_file_data =hwp_parsing.make_total_file_list(ben_files,mal_files)

    best_params , best_f1_score = hwp_model_training(X_file_data,y_file_data)

    print('GridSearchCV 최적 파라미터 : ', best_params)
    print('GridSearchCV 최고 f1 score : ', best_f1_score)