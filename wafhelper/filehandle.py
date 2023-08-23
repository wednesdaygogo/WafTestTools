import os
import shutil

import requests


def read_dir(path):
    filelist = []
    files = os.listdir(path)
    for file in files:
        filelist.append(path + file)
    return filelist

def read_file(path):
    with open(path,'rb') as f:
        content = f.read()
    return content

def copy_file(src,dst):
    isexist = os.path.exists(dst)
    if not isexist:
        os.makedirs(dst)
    shutil.copy(src,dst)
def check_eventname_form_waf():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Cookie': 'SID=s%3A2Fj3e5T_De3hzUumnin_wYRlCmCreOzj.p5J90QQ1G2VfJHakEi3T8vuHDMNl2hXkIiHtdBC8%2BMM; VWPHPUSERID=adm',
        'Content-Type':'application/json',
        'Connection':'close',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbSIsImtleSI6IjE2Nzk4ODI2MzMzMzEtMC4wNjI5Nzc4MDUyMTQ3MDE4NyIsImlhdCI6MTY3OTg5Njc0OSwiZXhwIjoxNjc5OTI1NTQ5fQ.08iDyf4cLtqgm8hEYsVhGBrg8L43g67KQpiJ1MC9rAo'
    }
    data = {"page":1,"limit":1,"isEnglish":0,"searchType":"ad","searchstr":"","auditlinkage_dstip":"","auditlinkage_uv":"","auditlinkage_pv":"","auditlinkage_port":0,"auditlinkage_wafip":"10.51.15.186","filters":[],"chk_time":"on","chk_evt_name":"on","chk_evt_group":"on","chk_evt_level":"on","chk_x_forwarded_for":"on","chk_srcip_str":"on","chk_srcport":"on","chk_dstip_str":128,"chk_dstport":"on","chk_action":"on","chk_rawguid":"on"}
    url = "http://10.51.15.186/securityeventmonitoring/eventmonlist"
    # response = requests.post(url=url, json=data,headers=header)
    # result = response.json()
    # return result['data']['rows'][0]['evt_name']
    while True:
        response_1 = requests.post(url=url, json=data,headers=header)
        response_2 = requests.post(url=url, json=data, headers=header)
        result_1 = response_1.json()
        result_2 = response_2.json()
        if result_1['data']['rows'][0]['evt_name'] == result_2['data']['rows'][0]['evt_name']:
            break

    return result_2['data']['rows'][0]['evt_name']


