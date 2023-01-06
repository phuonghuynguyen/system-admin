from asyncio.windows_events import NULL
import asyncore
from re import I, S
import requests
import json
import datetime
import time

url = "http://10.254.139.73:8501/api/v1/query_range"
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }

iofile = open("f:\CPM\CPM\io.txt", "w")
ipfile = open("f:\CPM\CPM\ip1.txt", "w+")
for ip in ipfile:
    ip2=ip.strip()
    io_ql= 'max by(instance, backup, job)(avg_over_time(sd_agent_node_disk_usage_5m{backup="false", instance=~"' + ip2 +'"}[10m])*100)'
    payload = {"query":io_ql,"step":"5m", "start":"1671901200.000", "end":"1671987600.000"}
  
    #total_ram_qr = {"query":"node_memory_MemTotal_bytes{instance=~%22{}%22}".format(ip)}
    temp_rq = requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()
    if temp_rq != NULL: 
        rp=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload ).json()['data']['result']
        for i in rp:
            ins = str(i['metric']['instance'])
            rs_value= i['values']
            for i in rs_value:
                io_time=i[0]
                io_humantime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(io_time))
                io_value=i[1]
                s=ins + '_' + str(io_humantime) + '_' + io_value + '\n'
                iofile.write(s)
                print(s)
iofile.close()
