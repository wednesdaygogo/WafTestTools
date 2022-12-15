import requests
import os
import time
import sys
import getopt

def get_filename(path):
    filelist = os.listdir(path)
    return filelist

def read_file(path):
    with open(path,encoding='utf-8',errors='ignore') as f:
        return f.read()

def post_webshell(url,filename,path):
    url = url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Referer':'http://10.5.10.78:8005/Pass-01/index.php',
               'Origin':'http://10.5.10.78:8005',
               'Upgrade-Insecure-Requests':'1',
               'Connection':'close'
               }
    file = {"upload_file":(filename,read_file(path),'image/png'),"submit":(None,'上传')}
    r = requests.post(url,files=file,headers=headers)
    if(r.status_code == 403):
        print('被拦截文件:{}'.format(path))
        return 1
    else:
        print('上传成功文件:{}'.format(path))
        return 0
def post_rce_guess(url,filename):
    payload = {'check_syntax_error':['<?ph p phpinfo();','<?php $1a="sss"','<?php $a=1','<?php echo "hello\'','<?php for($i=0;$i<10;$i++){;','<?php for($i=0;$i<10;i++){ echo $i;};','<?php $a=1;$b=2;$a=$a.....$b;'],
               'check_syntax_right':['<?php phpinfo()']
               }
    url = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Referer': 'http://10.5.10.78:8005/Pass-01/index.php',
               'Origin': 'http://10.5.10.78:8005',
               'Upgrade-Insecure-Requests': '1',
               'Connection': 'close'
               }
    file = {"upload_file":(filename,payload,'image/png')}
    reponse = requests.post(url,files=file,headers=headers)


def scan(url,suffix='png',file_path='../uploadtest/'):
    count_all = 0
    count_success = 0
    count_fail = 0
    webshells = get_filename(file_path)
    for webshell in webshells:
        webshell_path = file_path + webshell
        file_name,file_extension = os.path.splitext(webshell_path)
        upload_name = webshell.replace(file_extension,'.' + suffix)
        result = post_webshell(url,upload_name,webshell_path)
        if result == 1:
            count_all = count_all + 1
            count_fail =count_fail +1
        else:
            count_all = count_all + 1
            count_success =count_success + 1
    print('检测率:{}'.format(count_fail/count_all))
def main(argv):
    dir_path = None
    suffix = None
    try:
        opts,args= getopt.getopt(argv,"hu:p:",["suffix="])
    except getopt.GetoptError:
        print('python testchangt.py -u <url> -p D:\phpcheck/uploadtest/ --suffix=png')
        sys.exit()
    for opt,arg in opts:
        if opt == '-h':
            print('python testchangt.py -u <url> -p D:\phpcheck/uploadtest/ --suffix=png')
            sys.exit()
        elif opt == '-u':
            url = arg
        elif opt == '-p':
            dir_path = arg
        elif opt == '--suffix':
            suffix = arg
    if (dir_path == None and suffix != None):
        scan(url,suffix)
    elif(suffix == None and dir_path == None):
        scan(url)
    else:
        scan(url,suffix,dir_path)



if __name__ == '__main__':
    main(sys.argv[1:])