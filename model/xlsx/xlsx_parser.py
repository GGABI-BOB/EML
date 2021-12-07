import os
import zipfile
import numpy as np
import re
import pandas as pd

ben_file_path = "/home/ggabi/sumin/data_sha256/xlsx/ben"
mal_file_path = "/home/ggabi/sumin/data_sha256/xlsx/mal"

def make_file_list(file_path): #파일 리스트 생성
    file_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_list.append(file)
    return file_list

def make_feature(file_path, file_list):
    features = []
    for i in range(len(file_list)):
        try:
            # document will be the filetype zipfile.ZipFile
            document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
            f = document.namelist()
            features.append(f)
            
        except zipfile.BadZipfile:
            continue
    #print("개수 : " + str(len(features)))
    tmp= [y for x in features for y in x] #2차원배열로 존재 -> 1차원리스트
    tmp = remove_duplicate(tmp)
    feature_set = set(tmp)

    return feature_set

def remove_duplicate(ord_features):
    tmp = []
    for s in ord_features:
        s=s.replace("\\",'/')
        tmp.append(re.sub(r"([0-9]+)[.]", '.', s))
    return tmp

def make_feature_vec(file_path, file_list, total_feature):
        total_feature_val = []
        for i in range(len(file_list)):
            result = dict(zip(total_feature, [0 for i in range(len(total_feature))]))
            try:
                # document will be the filetype zipfile.ZipFile
                document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
                feature = document.namelist()
                feature = remove_duplicate(list(feature))
                #print(feature)
                feature_dict = dict(zip(feature, [1 for i in range(len(feature))]))
                                        
                for k1 in result:
                    for k2 in feature_dict:
                        if (k1 == k2):
                            result[k1] = 1

                feature_val = list(result.values())
                # if len(list(feature_dict.values()))!=feature_val.count(1):
                #     print("error")
                total_feature_val.append(feature_val)

            except zipfile.BadZipfile:
                continue

        return total_feature_val


def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    data_files = list(all_files)
    return data_files

def make_total_file_list(ben_files, mal_files):
    X_data=[]
    y_data=[]
    for file in ben_files:
        X_data.append(file)
        y_data.append(0)
    for file in mal_files:
        X_data.append(file)
        y_data.append(1)
    X_data = np.array(X_data)
    y_data = np.array(y_data)
    y_data=y_data.reshape(len(y_data),1)
    
    return X_data, y_data


def get_train_vector(X_file_data,y_file_data):
    ben_file_list = [X_file_data[i] for i in range(len(X_file_data)) if y_file_data[i]==0]
    mal_file_list = [X_file_data[i] for i in range(len(X_file_data)) if y_file_data[i]==1]
    mal_feature = make_feature(mal_file_path, mal_file_list)
    ben_feature = make_feature(ben_file_path, ben_file_list)
    
    total_feature = list(mal_feature | ben_feature)
    
    mal_feature_vector = np.array(make_feature_vec(mal_file_path, mal_file_list, total_feature))
    ben_feature_vector = np.array(make_feature_vec(ben_file_path, ben_file_list, total_feature))

    X_data = np.concatenate((ben_feature_vector,mal_feature_vector),axis=0)
    y_data = np.concatenate([np.zeros(len(ben_feature_vector)),np.ones(len(mal_feature_vector))])

    return X_data, y_data, total_feature

def get_test_vector(X_file_data, y_file_data, feature):
    ben_file_list = [X_file_data[i] for i in range(len(X_file_data)) if y_file_data[i]==0]
    mal_file_list = [X_file_data[i] for i in range(len(X_file_data)) if y_file_data[i]==1]
    mal_feature_vector = np.array(make_feature_vec(mal_file_path, mal_file_list, feature))
    ben_feature_vector = np.array(make_feature_vec(ben_file_path, ben_file_list, feature))

    X_data = np.concatenate((ben_feature_vector,mal_feature_vector),axis=0)
    y_data = np.concatenate([np.zeros(len(ben_feature_vector)),np.ones(len(mal_feature_vector))])

    return X_data, y_data