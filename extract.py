from email.parser import BytesParser
from email import policy
from email.message import EmailMessage
from email.header import decode_header
import ctypes
import email
import re
# Direct .eml file or directory path
EML_PATH_DIR = './emlBox'
RESULT_DIR = './parsedData' 

# Message Box for checking
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

###############################################
# @@@ Input @@@
# date (parsed Date data)
# @@@ Function @@@
# Writes status report 
################################################ 
def Result_report(result):
    with open('Status Report.txt','a',encoding='utf-8') as f:
        f.writelines(f"{result}\n")

def KMP_table(pattern):
    lp = len(pattern)
    tb = [0 for _ in range(lp)]
    
    pidx = 0
    for idx in range(1, lp):
        while pidx > 0 and pattern[idx] != pattern[pidx]:
            pidx = tb[pidx-1]
        
        if pattern[idx] == pattern[pidx] :
            pidx += 1
            tb[idx] = pidx
    
    return tb

def KMP(word, pattern):
    table = KMP_table(pattern)

    # results = [] 
    pidx = 0
    
    for idx in range(len(word)):
        while pidx > 0 and word[idx] != pattern[pidx] :
            pidx = table[pidx-1]
        if word[idx] == pattern[pidx]:
            if pidx == len(pattern)-1 :
                # results.append(idx-len(pattern)+2)
                # pidx = table[pidx]
                return 1
            else:
                pidx += 1
    
    return 0


###############################################
# @@@ Input @@@
# msg: EmailMessgae (msg of eml)
# @@@ Function @@@
# Get file name of Attachments
################################################ 
def get_part_filename(msg: EmailMessage):
    try:
        filename =  msg.get_filename()
    
        if decode_header(filename)[0][1] is not None:
            filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
            
        return filename    
    
    except:
        return 'File Error'   


################################################
# @@@ Input @@@
# date (parsed Date data)
# @@@ Function @@@
# Convert date 
################################################ 
def convert_date(date):
    total = []
    
    con_date = date.split(' ')
    
    Month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    
    for i,month in enumerate(Month_list):        
        if con_date[2] == month:
            
            Con_month = str(i+1)   
            temp = f"{con_date[3]}-{Con_month}-{con_date[1]} {con_date[4]}"
            return temp        
  

################################################
# @@@ Input @@@
# data (body of eml)
# @@@ Function @@@
# Delete something useless except contents fo email
################################################ 
def HtmltoText(data):
    data = re.sub(r'&nbsp;','',data)
    data = re.sub(r'</.*?>','\n',data)
    data = re.sub(r'<.*?>', '', data)
    data = re.sub(r'&lt;', '<', data)
    data = re.sub(r'&gt;', '>', data)
    data = re.sub(r'p{.*}', '', data)
    return data


################################################
# @@@ Input @@@
# target_eml (name of target eml file)
# @@@ Function @@@
# Extracts url from body
################################################
def extractURL(ms, data):
    urlList = []
    httpURL = re.findall('(https?://[\w\/\$\-\_\.\+\!\*\'\(\)]+[/A-Za-z0-9- =+~\?&;:_%\.#\*@!\(\)]+)', data)
    urlList = httpURL
    return urlList


################################################
# @@@ Input @@@
# target_eml (name of target eml file)
# @@@ Function @@@
# Extracts core information from eml
################################################
def extract_info(target_eml):
    with open(target_eml, 'rb') as fp:
        urlList = []
        try:
            ms = email.message_from_file(open(target_eml,encoding='utf-8'))
        except UnicodeDecodeError:
            ms = email.message_from_file(open(target_eml,encoding='euc-kr'))
        msg = BytesParser(policy=policy.default).parse(fp)

        # URL = [x for x in URL if x]
        # Data['URLS'] = URL
        RECEIVER = str(msg['To']).split(',')
        RECEIVER = [x for x in RECEIVER if x]
        SENDER = str(msg['From'])
        SUBJECT = str(msg['Subject'])
        DATE = str(msg['Date'])

        if msg['Date'] is not None:
            DATE = convert_date(DATE)

        Data = {
        "Title": [SUBJECT],
        "Date": [DATE],
        "Receiver": [RECEIVER],
        "Num_of_Receiver": [len(RECEIVER)],
        "Sender": [SENDER]
        }

        if KMP(SUBJECT, '(광고)'):
            Data['AdFlag'] = ['yes']

        if msg['X-Original-SENDERIP'] is not None:
            SENDER_IP = str(msg['X-Original-SENDERIP'])
            Data['X-Original-SendIP'] = [SENDER_IP]
        

        if msg['X-Originating-IP'] is not None:
            SENDER_IP2 = str(msg['X-Originating-IP'])
            Data['X-Originating-IP'] = [SENDER_IP2]          
                     
        
        if msg['X-Original-SENDERCOUNTRY'] is not None:
            SENDER_COUNTRY = str(msg['X-Original-SENDERCOUNTRY'])
            Data['X-Original-SendCOUNTRY'] = [SENDER_COUNTRY]  
           
        try:
            # walks through message
            for part in msg.walk():                            
                type = part.get_content_type()
                if type == 'text/html':
                    EML_BODY = str(msg.get_body(preferencelist=('html')).get_content())                    
                    URL = extractURL(ms, EML_BODY)
                    # EML_BODY = str(msg.get_body(preferencelist=('html')).get_content())
                    EML_BODY = HtmltoText(EML_BODY)
                elif type == 'text/plain':
                    EML_BODY = str(msg.get_body(preferencelist=('plain')).get_content())
                    
        except Exception as Error:
            Mbox("ERROR REPORTED!", str(Error), 0)
            # print(Error)
            pass

        URL = [x for x in URL if x]
        Data['URLS'] = URL
        Data['Contents'] = [EML_BODY]
        
    return Data 

################################################
# @@@ Input @@@
# Path (Path where u want to drop files)  |  target_eml (name of target eml file)
# @@@ Function @@@
# Extract files from eml and write
################################################
def extract_attachments(Path,target_eml):
    try:
        msg = email.message_from_file(open(target_eml,encoding='utf-8'))
    except UnicodeDecodeError:
        msg = email.message_from_file(open(target_eml,encoding='euc-kr'))      
    attachments=msg.get_payload() 
    
    # FileName List
    fnam_list = []      
    
    if msg.is_multipart() is True:
        for attachment in attachments[1:]:
            if get_part_filename(attachment) == 'File Error':
                return 'File Error'
            else:
                fnam = get_part_filename(attachment)
                
                fnam_list.append(fnam)
                attach_file = f"{Path}\{fnam}"
                
                # Take payload and Write File 
                with open(attach_file, 'wb') as f:
                    f.write(attachment.get_payload(decode=True))
                    Result_report(f"Success! File successfully extracted from {target_eml}")
                    Result_report(f"Success! Extracted attachment : {fnam}")
    elif msg.is_multipart() is False:
        return 'No File'       
    else:
        return 'File Error'

    return fnam_list


