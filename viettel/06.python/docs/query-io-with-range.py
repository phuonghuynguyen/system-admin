from asyncio.windows_events import NULL
import asyncore
from re import I, S, search
import requests
import json
import datetime
import time
import calendar
import re

url = 'http://10.254.139.73:8501/api/v1/series'
url2 = 'http://10.254.139.73:8501/api/v1/query_range'
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }
ins_list=[]
subnet_list=[]
ins_file = open("f:\CPM\CPM\instance.txt", "w",encoding="utf-8") 
iofile = open("io.txt", "w")
metric= "node_boot_time_seconds"
ngay = calendar.timegm(time.gmtime())
payload = {"match[]":metric, "start": ngay-86400 , "end": ngay}
qr_data = requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]
for i in qr_data:
    if "job" in i and  search("linux_sd_agent",i['job']) :
        ins=str(i['instance'])
        ins_list.append(ins)
        sub_net_tmp= ins.split('.')
        sub_net= str(sub_net_tmp[0]) + '.' + str(sub_net_tmp[1]) + '.' + str(sub_net_tmp[2]) + '.*:' + str(sub_net_tmp[3].split(':')[1])       
        if sub_net not in subnet_list:
            subnet_list.append(sub_net)
        job=str(i['job'])
        mor=str(i['monitor'])
        s= ins + '|' + job + '|' + mor + '\n'
        ins_file.write(s)

metric2= "wmi_system_system_up_time"
payload2 = {"match[]":metric2, "start": ngay-86400, "end": ngay}
qr_data2 = requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload2).json()["data"]
for i in qr_data2:
    ins=str(i['instance'])
    ins_list.append(ins)
    sub_net_tmp= ins.split('.')
    sub_net= str(sub_net_tmp[0]) + '.' + str(sub_net_tmp[1]) + '.' + str(sub_net_tmp[2]) + '.*:' + str(sub_net_tmp[3].split(':')[1])
    if sub_net not in subnet_list:
        subnet_list.append(sub_net)
    job=str(i['job'])
    mor=str(i['monitor'])
    s= ins + '|' + job + '|' + mor + '\n'
    ins_file.write(s)
#print (len(subnet_list))
#print(subnet_list)
#ins_file.write(str(subnet_list))

for i in subnet_list:
    if ":20100" in i:
    #ip2=ip.strip()
       io_ql= 'max by(instance, backup, job)(avg_over_time(sd_agent_node_disk_usage_5m{backup!="true", instance=~"' + i +'"}[10m]))*100'
       io_qr = {'query': io_ql, "step": "5m", "start": ngay-86400, "end": ngay}
    #total_ram_qr = {"query":"node_memory_MemTotal_bytes{instance=~%22{}%22}".format(ip)}
       temp_rq = requests.request("GET", url2, headers=headers, auth=(usr, pas), params=io_qr).json()['data']['result']
#       print(json.dumps(temp_rq,indent=4))
       for i in temp_rq:
           ins = i['metric']['instance']
           rs_value= i['values']
           for i in rs_value:
               io_time=i[0]
#               io_humantime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(io_time))
               io_value=i[1]
               s=ins + '_' + io_value + '\n'
               iofile.write(s)
               print(s)
#           io_time= str(i['value'][0])
#           io= str(i['value'][1])
#           s=ins  +'_' + io_time + '_' + io + '\n'
#           print(s)
#           iofile.write(s)
    if ":9182" in i:
    #ip2=ip.strip()
       io_ql= 'max by(instance)(avg_over_time(wmi_io_usage_percent{instance=~"'+ i +'"}[10m]))'
       io_qr = {'query': io_ql, "step": "5m", "start": ngay-86400, "end": ngay}
    #total_ram_qr = {"query":"node_memory_MemTotal_bytes{instance=~%22{}%22}".format(ip)}
       temp_rq = requests.request("GET", url2, headers=headers, auth=(usr, pas), params=io_qr).json()['data']['result']
       for i in temp_rq:
           ins = i['metric']['instance']
           rs_value= i['values']
           for i in rs_value:
               io_time=i[0]
#               io_humantime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(io_time))
               io_value=i[1]
               s=ins + '_' + io_value + '\n'
               iofile.write(s)
               print(s)
#           io_time= str(i['value'][0])
#           io_value=  i['value'][1]
#           s=ins  +'_' + io_time + '_' + io_value + '\n'
           #print(s)
#           iofile.write(s)
#ins_file.write(ins_list)"""
iofile.close()