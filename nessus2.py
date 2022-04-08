from datetime import datetime
import sqlite3
import requests
import subprocess
import datetime
import urllib3
import socket
urllib3.disable_warnings()
header={"X-ApiKeys": "accessKey=57f6504f85fa53dd440004e605b3b45db6d99dbca86448d6e147ff13e3f1989b; secretKey= 7f802004872dc1a1216b83c6efb8735af9d90dfcff48873323354917d6820464;"}
cikti=subprocess.check_output("dir",shell=True)
if not "host_discovery.db" in str(cikti):
    print("veritabanı yok ")
    conn= sqlite3.connect('host_discovery.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE hosts (ip text,zaman text)''')
conn=sqlite3.connect('host_discovery.db')
c=conn.cursor()
c.execute('SELECT ip FROM hosts')
ipler=c.fetchall()
ipler_liste=[]
for i in ipler:
    ipler_liste.append(str(i[0]))
conn.close()
url="https://192.168.1.67:8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)
for i in sonuc.json()['scans']:
    if "HD" in i['name'] and "completed" in i['status']:
        url="https://192.168.1.67:8834/scans/"+str(i['id'])
        sonuc=requests.get(url=url,headers=header,verify=False)
        for j in sonuc.json()['hosts']:
            if not j['hostname'] in ipler_liste:
                print("Yeni IP:",j['hostname'])
                conn=sqlite3.connect('host_discovery.db')
                c=conn.cursor()
                c.execute('INSERT INTO hosts VALUES (?,?)',(str(j['hostname']),str(datetime.datetime.now()))) 
                conn.close()
                s=socket.socket()
                s.connect(("192.168.1.14",515))
                log="yeni ip bulundu"+str(j['hostname'])
                s.sendall(str(log).encode())
                s.close()