from datetime import datetime
import sqlite3
import requests
import subprocess
import datetime
import urllib3
import socket
urllib3.disable_warnings()
cikti=subprocess.check_output("dir",shell=True)
if not "port.db" in str(cikti):
    conn = sqlite3.connect('port.db')
    c= conn.cursor()
    c.execute('''CREATE TABLE portlar (port text, ip text, zaman text)''')
    c.close()
header={"X-ApiKeys": "accessKey=; secretKey=;"}#Nessus API Keys
url="https://192.168.1.67:8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)
for i in sonuc.json()['scans']:
    scan_id=i['id']
    url="https://192.168.1.67:8834/scans/"+str(scan_id)
    tarama=requests.get(url=url, headers=header,verify=False)
    for j in tarama.json()['hosts']:
        try: 
            host_id=j['host_id']
            #14272 shows opened ports
            url="https://192.168.1.67:8834/scans/"+str(scan_id)+"/host/"+str(host_id)+"/plugins/11219"
            IP=requests.get(url=url,headers=header,verify=False)
            for k in IP.json()['outputs']:
                port=list(k['ports'].keys())[0]
                IP=j['hostname']
                conn = sqlite3.connect("port.db")
                c=conn.cursor()
                cikti=c.execute('select * from portlar where port=? and ip=?',(port,IP))
                port_sayisi=len(cikti.fetchall())
                conn.close()
                if port_sayisi<1:
                    print("Yeni port:",port,"IP:",IP)
                    conn=sqlite3.connect("port.db")
                    c=conn.cursor()
                    c.execute('INSERT INTO portlar VALUES (?,?,?)',(port,IP,str(datetime.datetime.now())))
                    conn.commit()
                    conn.close()
        except:
            pass