import sqlite3

conn = sqlite3.connect("filter.db") 
cur = conn.cursor()

def senderFilter(sender):
    query = "SELECT EXISTS(SELECT ID FROM sender WHERE address = '" + sender + "')"
    cur.execute(query) 
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

def senderDomainFilter(sender_domain):
    query = "SELECT EXISTS(SELECT ID FROM sender_domain WHERE domain = '" + sender_domain + "')"
    cur.execute(query) 
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

def senderIPFilter(sender_ip):
    query = "SELECT EXISTS(SELECT ID FROM sender_ip WHERE IP = '" + sender_ip + "')"
    cur.execute(query) 
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

def contentsURLFilter(contents_url):
    query = "SELECT EXISTS(SELECT ID FROM contents_url WHERE url = '" + contents_url + "')"
    cur.execute(query) 
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False