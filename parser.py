import os
import simplejson
import time
import datetime
import extract

from model.hwp import hwp_model
from model.pdf import pdf_model
from model.xlsx import xlsx_model
from model.docx import docx_model


# Direct .eml file or directory path
EML_PATH_DIR = './emlBox2'
RESULT_DIR = './parsedData' 


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


###############################################
# @@@ Function @@@
# Total parser 
################################################ 
def parse_eml():
    for root, dir, files in os.walk(EML_PATH_DIR):
        for file in files:
            print(file + ' analyzing start!!...')
            time.sleep(1)

            emlName = file.split(".")[0]
            parsed_path = RESULT_DIR + "/" + emlName 
            try:
                os.makedirs(parsed_path)
            except Exception as err:
                print("ERROR REPORTED: " + err)    
                print(err)           
                exit(1)
            list_info = {}
            list_Second = {}
            if '_info.json' not in file:
                target = f"{root}/{file}"
                fnm_json = f"{parsed_path}/{emlName}_info.json" 
                list_Second = extract.extract_info(target)
                if list_Second == 'Skip':
                    os.rmdir(parsed_path)
                    print('Skipped!...')
                    time.sleep(1)
                    continue

                list_info['emlName'] = [file]
                try:
                    fnm_name = extract.extract_attachments(parsed_path,target)
                    if fnm_name == 'No File':
                        list_info['Attachment'] = [' ']
                        extract.Result_report(f"{file}  : No such File exists")
                    elif fnm_name == 'File Error':
                        list_info['Attachment'] = ['FILE_FORMAT_ERROR']   
                        extract.Result_report(f"{file}  :   File Format Error")
                    else:
                        fnm_name = [x for x in fnm_name if x]  
                        list_info['Attachment'] = fnm_name
        
                except Exception as err:
                    print("ERROR REPORTED: " + err)
                    extract.Result_report(f"Error reported in {root} : {err} ")                
                    pass
                list_info.update(list_Second)
                
                ##### add static analysis #####
                for path, dirs, atts in os.walk(parsed_path):
                    parsed_path = parsed_path + '/'
                    print(parsed_path)
                    for att in atts:
                        print('Attachment FileName : '+str(att))
                        print('Malicious percentage : '+str(predict_file(parsed_path,att)))
                        print("\n")

                print(file + ' finished!...')     
                time.sleep(1)      

            else:
                extract.Result_report(f"Same File Exists! : {fnm_json}")


def main():
    start = time.time()
    parse_eml()
    sec = time.time() - start
    times = str(datetime.timedelta(seconds=sec)).split(".")
    times = times[0]
    
    print("Parsing Completed! Running time : " + times)

if __name__ == "__main__":
    main()