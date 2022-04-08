from email import header
import requests
import subprocess
import urllib3
urllib3.disable_warnings()
header={"X-ApiKeys": "accessKey=; secretKey=;"}#Nessus API Keys
url="https://192.168.1.67:8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)
for i in sonuc.json()["scans"]:
    scan_id=i["id"]
    url="https://"NessusIP":8834/scans/"+str(i["id"])
    sonuc=requests.get(url=url,headers=header,verify=False)
    for i in sonuc.json()["hosts"]:
        try:
            IP=i['hostname']
            host_id=i['host_id']
            print(IP)
            print(host_id)
            print("================")
            url="https://"NessusIP":8834/scans/"+str(scan_id)+"/hosts/"+str(host_id)+"/plugins/11936"
            zafiyet=requests.get(url=url,headers=header,verify=False)
            plugin_output=zafiyet.json()['outputs'][0]['plugin_output']
            print(plugin_output)
            if "Windows" in plugin_output:
                dizin=subprocess.check_output("dir",shell=True)
                print(dizin)
                if not "windowss.txt" in str(dizin):
                    veri=str(IP)+"\n"
                    dosya=open("windowss.txt","w")
                    dosya.write(veri)
                    dosya.close()
                dosya=open("windowss.txt","r")
                IP_kontrol=dosya.read()
                dosya.close()
                if not str(IP) in IP_kontrol:
                    veri=str(IP)+"\n"
                    dosya=open("windows.txt","a")
                    dosya.write(veri)
                    dosya.close()
        except:
            pass
