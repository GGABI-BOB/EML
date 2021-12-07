import numpy as np

from hwp import hwp_model, hwp_parsing
from pdf import pdf_model
from docx import docx_model, docx_parser
from xlsx import xlsx_model, xlsx_parser

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB

def pdf_training():
    X_data = np.load('/home/ggabi/sumin/model/pdf/pdf_X_data.npy', allow_pickle=True)
    y_data = np.load('/home/ggabi/sumin/model/pdf/pdf_Y_data.npy', allow_pickle=True)
    best_params , best_f1_score = pdf_model.pdf_model_training(X_data,y_data)
    print('pdf의 GridSearchCV 최적 파라미터 :', best_params)
    print('pdf의 GridSearchCV 최고 f1 score : ' ,best_f1_score)
    return best_params

def xlsx_training():
    ben_files = docx_parser.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/xlsx/ben/")
    mal_files = docx_parser.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/xlsx/mal/")
    X_file_data, y_file_data =xlsx_parser.make_total_file_list(ben_files,mal_files)
    best_params , best_f1_score = xlsx_model.xlsx_model_training(X_file_data,y_file_data)
    print('xlsx의 GridSearchCV 최적 파라미터 :', best_params)
    print('xlsx의 GridSearchCV 최고 f1 score : ' ,best_f1_score)
    return best_params

def docx_training():
    ben_files = docx_parser.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/docx/ben/")
    mal_files = docx_parser.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/docx/mal/")
    X_file_data, y_file_data =docx_parser.make_total_file_list(ben_files,mal_files)
    best_params , best_f1_score = docx_model.docx_model_training(X_file_data,y_file_data)
    print('docx의 GridSearchCV 최적 파라미터 :', best_params)
    print('docx의 GridSearchCV 최고 f1 score : ' ,best_f1_score)
    return best_params

def hwp_training():
    ben_files = hwp_parsing.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/hwp/ben/")
    mal_files = hwp_parsing.get_file_list_from_dir("/home/ggabi/sumin/data_sha256/hwp/mal/")
    X_file_data, y_file_data =hwp_parsing.make_total_file_list(ben_files,mal_files)
    best_params , best_f1_score = hwp_model.hwp_model_training(X_file_data,y_file_data)
    print('hwp의 GridSearchCV 최적 파라미터 :', best_params)
    print('hwp의 GridSearchCV 최고 f1 score : ' ,best_f1_score)
    return best_params


if __name__ == '__main__':
    print("pdf 성능 : ", pdf_training())
    print("docx 성능 : ", docx_training())
    print("hwp 성능 : ", hwp_training())
    print("xlsx 성능 : ", xlsx_training())
