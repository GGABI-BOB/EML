import requests
import json
import time
import os

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ModuleNotFoundError as e:
    print (e)
    os.system("pip3 install watchdog")

# ------------------------------------------------
class Handler(FileSystemEventHandler):
    def on_created(self, event): # 파일 생성시
        print (f'event type : {event.event_type}\n'

               f'event src_path : {event.src_path}')
        if event.is_directory:
            print ("디렉토리 생성")
        else: # not event.is_directory
            """
            Fname : 파일 이름
            Extension : 파일 확장자 
            """
            Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
            '''
             1. zip 파일
             2. exe 파일
             3. lnk 파일
             4. json 파일
            '''
            if Extension == '.zip':
                print (".zip 압축 파일 입니다.")
            elif Extension == '.exe':
                print (".exe 실행 파일 입니다.")
                os.remove(Fname + Extension)   # _파일 삭제 event 발생
            elif Extension == '.lnk':
                print (".lnk 링크 파일 입니다.")
            elif Extension == '.json':
                print ("json 파일 입니다.")

    def on_deleted(self, event):
        print ("삭제 이벤트 발생")

    def on_moved(self, event): # 파일 이동시
        print (f'event type : {event.event_type}\n')

class Watcher:
    # 생성자
    def __init__(self, path):
        print ("감시 중 ...")
        self.event_handler = None      # Handler
        self.observer = Observer()     # Observer 객체 생성
        self.target_directory = path   # 감시대상 경로
        self.currentDirectorySetting() # instance method 호출 func(1)

    def currentDirectorySetting(self):
        print ("====================================")
        print ("현재 작업 디렉토리:  ", end=" ")
        os.chdir(self.target_directory)
        print ("{cwd}".format(cwd = os.getcwd()))
        print ("====================================")

    def run(self):
        self.event_handler = Handler() # 이벤트 핸들러 객체 생성
        self.observer.schedule(
            self.event_handler,
            self.target_directory,
            recursive=False
        )

        self.observer.start() # 감시 시작
        try:
            while True: # 무한 루프
                time.sleep(1) # 1초 마다 대상 디렉토리 감시
        except KeyboardInterrupt as e: # 사용자에 의해 "ctrl + z" 발생시
            print ("감시 중지...")
            self.observer.stop() # 감시 중단

myWatcher = Watcher("/home/ggabi/Eml")
myWatcher.run()

# REST_URL = "http://localhost:8090/tasks/create/file"
# SAMPLE_FILE = "./testEMLwithFile2.eml"
# HEADERS = {"Authorization": "Bearer UDlDodxFjmPUblIiV3qVyA"}

# with open(SAMPLE_FILE, "rb") as sample:
#     files = {"file": ("test_file_4", sample)}
#     params = {'timeout': int(20)}
#     r = requests.post(REST_URL, headers=HEADERS, files=files, params=params)

# # Add your code to error checking for r.status_code.

# task_id = r.json()["task_id"]

# print(task_id)

# REST_URL = "http://localhost:8090/tasks/report/47"
# HEADERS = {"Authorization": "Bearer UDlDodxFjmPUblIiV3qVyA"}

# r = requests.get(REST_URL, headers=HEADERS)

# # Add your code to error checking for r.status_code.
# test_result = r.json()

# with open("test_result.json", "w") as json_file:
#     json.dump(test_result, json_file)

# with open("test_result.json") as json_file:
#     info = json.load(json_file)
#     print(info["info"]["score"])

# # Add your code to error checking if task_id is None.