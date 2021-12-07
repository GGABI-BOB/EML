import generate_feature_vector_pdf
import os
import numpy as np
import pandas as pd

def generate_data(mal_dir, ben_dir):
    X_data=[]
    y_data=[]

    mal_files = os.listdir(mal_dir)
    ben_files = os.listdir(ben_dir)
    for file in mal_files:
        X_data.append(generate_feature_vector_pdf.extract(mal_dir+file))
        y_data.append(1)
    for file in ben_files:
        X_data.append(generate_feature_vector_pdf.extract(ben_dir+file))
        y_data.append(0)
    X_data = np.array(X_data)
    y_data = np.array(y_data)

    np.save('pdf_X_data', X_data)
    np.save('pdf_Y_data',y_data)
    


if __name__ == '__main__' :
    generate_data('/home/ggabi/sumin/data_sha256/pdf/mal/','/home/ggabi/sumin/data_sha256/pdf/ben/')

    