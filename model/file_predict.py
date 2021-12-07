import os
from hwp import hwp_model
from pdf import pdf_model
from docx import docx_model
from xlsx import xlsx_model


def predict_file(PATH, file):
    filename, fileExtension = os.path.splitext(file)
    if fileExtension == '.hwp':
        return hwp_model.hwp_model_predict(PATH,file)[0]
    elif fileExtension == '.pdf':
        return pdf_model.pdf_model_predict(PATH,file)[0]
    elif fileExtension == '.docx':
        return docx_model.docx_model_predict(PATH,file)[0]
    elif fileExtension == '.xlsx':
        return xlsx_model.xlsx_model_predict(PATH,file)[0]
    else :
        print("지원하지 않는 확장자")

if __name__ == '__main__':
    PATH = '/home/ggabi/sumin/eml_test/a.eml/'
    list = os.listdir(PATH)
    for file in list:
        print('첨부파일 이름 : '+str(file))
        print('악성 파일 확률 : '+str(predict_file(PATH,file)))
        print("\n")