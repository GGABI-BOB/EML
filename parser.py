from ctypes import WinError
import os
import simplejson
import time
import datetime
import extract

# Direct .eml file or directory path
EML_PATH_DIR = './emlBox'
RESULT_DIR = './parsedData' 

###############################################
# @@@ Function @@@
# Total parser 
################################################ 
def parse_eml():
    for root, dir, files in os.walk(EML_PATH_DIR):
        for file in files:
            emlName = file.split(".")[0]
            parsed_path = RESULT_DIR + "\\ '" + emlName + "'"
            try:
                os.makedirs(parsed_path)
            except Exception as err:
                extract.Mbox("ERROR REPORTED!", str(err), 0)    
                print(err)           
                exit(1)
            list_info = {}
            list_Second = {}
            if '_info.json' not in file:
                target = f"{root}\{file}"
                fnm_json = f"{parsed_path}\\{emlName}_info.json" 
                list_Second = extract.extract_info(target)
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
                        fnm_name = [x for x in fnm_name if x]   # init fnm_name
                        list_info['Attachment'] = fnm_name
        
                except Exception as err:
                    extract.Mbox("ERROR REPORTED!", str(err), 0)
                    extract.Result_report(f"Error reported in {root} : {err} ")                
                    pass
                list_info.update(list_Second)
                
                json = simplejson.dumps(list_info, ensure_ascii=False)
                try:
                    o = open(fnm_json, "w", encoding='utf-8')
                except UnicodeEncodeError:
                    o = open(fnm_json, "w", encoding='euc-kr')
                o.write(json)
                o.close()
                extract.Result_report(f"Success! created json file : {file}_info.json")
                extract.Result_report("---------------------------------------")           

            else:
                extract.Result_report(f"Same File Exists! : {fnm_json}")


def main():
    start = time.time()
    parse_eml()
    sec = time.time() - start
    times = str(datetime.timedelta(seconds=sec)).split(".")
    times = times[0]

    extract.Mbox("Parsing Completed!", "Running time : "+times, 0)

if __name__ == "__main__":
    main()