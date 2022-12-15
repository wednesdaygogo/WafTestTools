import argparse
import re

import requests
from lxml import etree
from openpyxl import Workbook
import time
from tqdm import trange

def get_cve_from_ali(key,pages):
    vul_list = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    keywords = key.split(',')
    if len(keywords) == 1 or len(keywords) == 2:
        for i in trange(1, pages + 1):
            url = 'https://avd.aliyun.com/search?q={}&page={}'.format(keywords[0], i)
            result = requests.get(url=url, headers=header)
            if result.status_code == 200:
                result.encoding = 'utf-8'
                html = result.text
                html_afer_xpath = etree.HTML(html)
                vul_num = len(html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr'))
                for v in range(1, vul_num + 1):
                    vul_dic = {
                        "vul_avd_id": "",
                        "vul_cve_num": "",
                        "vul_name": "",
                        "vul_type": "",
                        "vul_time": "",
                        "vul_status": ""

                    }
                    vul_avd_id = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[1]/a/text()'.format(v))[0].strip()
                    vul_name = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[2]/text()'.format(v))[0]
                    try:
                        vul_type = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[3]/button/@title'.format(v))[0].strip()
                    except Exception as err:
                        vul_type = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[3]/button/text()'.format(v))[0].strip()

                    vul_time = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[4]/text()'.format(v))[0].strip()
                    vul_cve_num = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[5]/button[1]/@title'.format(v))[0]
                    vul_statu = html_afer_xpath.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[{}]/td[5]/button[2]/@title'.format(v))[0]
                    vul_dic['vul_avd_id'] = vul_avd_id
                    vul_dic['vul_name'] = vul_name
                    vul_dic['vul_type'] = vul_type
                    vul_dic['vul_time'] = vul_time
                    vul_dic['vul_cve_num'] = vul_cve_num
                    vul_dic['vul_status'] = vul_statu
                    if len(keywords) == 2:
                        if re.search(keywords[1].encode('unicode-escape').decode(),vul_name) != None:
                            vul_list.append(vul_dic)
                        else:
                            continue
                    else:
                        vul_list.append(vul_dic)

    else:
        print("参数输入错误")
    for vul in vul_list:
        print(vul)
    return vul_list
def geerate_execl(vuls):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "漏洞列表"
    sheet.append(["vul_avd_id", "vul_cve_num","vul_name","vul_type","vul_time","vul_status"])
    for vul in vuls:
        sheet.append(list(vul.values()))
    workbook.save("vul.xlsx")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--regex", help="例：php,代码注入（逗号前为搜索关键字，逗号后为正则表达式（匹配目标为漏洞名称），中文不用转码）")
    parser.add_argument("-p", "--pages", help="例：80，代表爬取阿里云漏洞库80页")
    args = parser.parse_args()
    geerate_execl(get_cve_from_ali(args.regex,int(args.pages)))
    # s = 'php代码注入漏洞'
    # word = "php.*代码".encode('unicode-escape').decode()
    # l = re.search(word,s)
    # print(l)





