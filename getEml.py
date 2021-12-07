import psycopg2
import os
import time
import json
import threading

class Databases():
    def __init__(self):
        with open('./properties.json', 'r') as f:
            jsonObject = json.load(f)
        id = jsonObject.get("DB").get("ID")
        pw = jsonObject.get("DB").get("PW")
        self.db = psycopg2.connect(host = '101.101.210.59',
        dbname='james_mail', user=id, password=pw, port=5432)

        self.cursor = self.db.cursor()
    
    def __del__(self):
        self.db.close()
        self.cursor.close()
    
    def execute(self, query, args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchone()
        return row
    
    def commit(self):
        self.cursor.commit()


class Query(Databases):
    def readEml(self, cnt):
        query = "SELECT encode(james_mail.header_bytes, 'hex'), encode(james_mail.mail_bytes, 'hex'), james_mail.mailbox_id, james_mail.mail_uid\
                FROM james_mail\
                JOIN james_mailbox on james_mail.mailbox_id = james_mailbox.mailbox_id\
                WHERE james_mailbox.mailbox_name = 'INBOX'\
                OFFSET " + str(cnt) + " rows\
                FETCH first 1 row only;"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
        except Exception as e :
            result = ("[DB error]",e)
        
        return result


# 이후 
if __name__ == "__main__":
    db = Query()
    i = int(0)
    print('Start!!')
    time.sleep(1)
    while(True):
        try:
            result = list(db.readEml(cnt = i))
        except TypeError as e:
            print("Waiting...")
            time.sleep(1)
            continue


        eml = result[0] + result[1]
        fileName = str(result[2]) + '_' + str(result[3])

        f = open('./sample.hex', 'wb')
        f.write(eml.encode())
        f.close()
        
        '''
        eml filename: index_mailboxID_mailUID
        ex) 0_1501_1 ==> 1501번 메일박스 아이디의 1번 ID eml
        '''
        os.system('xxd -p -r sample.hex ./emlBox2/' + str(i) + '_' + fileName +'.eml')
        os.remove('./sample.hex')
        print(str(i) + '_' + fileName + '.eml extracted!')

        i += 1
        time.sleep(1)