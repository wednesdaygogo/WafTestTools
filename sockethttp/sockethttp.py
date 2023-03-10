import socket
import os
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor,as_completed

from openpyxl import load_workbook

black_payload_path ={
    'php_code_injection':'./black_list/phpcodeinject_small_4k_payload/',
    'php_serilize':'./black_list/php_serilize_payload/',
    'xml_injection':'./black_list/xxe_payload/',
    'xray_php_serilize_payload':'./black_list/xray_php_serilize_payload/',
    'aes_payload':'./black_list/aes_lanjie_payload/'
}

white_payload_path = {
    'white_base64':'./white_list/white_payload_base64/',
    'white_picture':'./white_list/white_payload_picture/',
    'white_internet_post':'./white_list/internet_post_payload/',
    'normal_string':'./white_list/normal_string_post_payload/',
}

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
    cmd = 'copy {} {}'.format(src,dst)
    os.system(cmd)
def send(ip,port,content):
    #print(content)
    url = ip
    port = port
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((url,port))
    sock.sendall(content)
    #response = b''
    res = sock.recv(1024)
    # while rec:
    #     response += rec
    #     rec = sock.recv(1024)
    result = res.decode(errors='ignore')
    sock.close()
    return result

def main(url,port,content,file):
    try:
        result  = send(url,port,content)
        #print(result)
    except TimeoutError:
        print(file + ' 连接超时')
        return 2
        #copy_file(file,'.\\outtime\\')
    except ConnectionResetError:
        print(file + ' 已拦截')
        return 1
    except ConnectionAbortedError:
        #print(result)
        if result.find('403') == -1:
            print(file + ' 未拦截')
            return 0
            #copy_file(file,'.\\QMNO\\')
        else:
            print(file + ' 已拦截')
            return 1
            #copy_file(file,'.\\command-wubao\\')


def muti_thread_test(url,port,dir,threads):
    success = 0
    faild = 0
    out_time = 0
    future_list = []
    files = read_dir(dir)
    with ThreadPoolExecutor(threads) as executor:
        for file in files:
            content = read_file(file)
            a = [url,port,content,file]
            future_list.append(executor.submit(lambda p: main(*p),a))
    for future in as_completed(future_list):
        results = future.result()
        print(results)
        if results == 1:
            success = success +1
        elif results == 0:
            faild = faild + 1
        else:
            out_time = out_time + 1
    print("总共检测payload："+str(success+faild+out_time))
    print("拦截数量：" + str(success))
    print("未拦截数量：" + str(faild))
    print("超时数量：" + str(out_time))
    print("检测率："+str(success/success+faild+out_time))

def send_from_xlsx(url,port,path):
    if os.path.splitext(path)[-1] != '.xlsx':
        print('-x 参数需为xlsx后缀文件')
        sys.exit()
    success = 0
    count = 0
    workbook_object = load_workbook(filename=path)
    sheet = workbook_object.worksheets[0]
    max_row_num = sheet.max_row
    for i in range(2, max_row_num + 1):
        try:
            content = sheet[i][0].value.lstrip().encode("utf-8")
        except AttributeError:
            continue
        try:
            count = count + 1
            result = send(url, int(port), content)

            # print(result)
        except TimeoutError:
            print('序号:' + str(count) + ' ' + 'line: '+ str(i) + ' 连接超时')
            # copy_file(file,'.\\outtime\\')
            continue
        except ConnectionResetError:
            print('序号:' + str(count) + ' ' + 'line: '+ str(i) + ' 已拦截')
            success = success + 1
            continue
        except ConnectionAbortedError:
            continue
        # print(result)
        if result.find('403') == -1:
            print('序号:' + str(count) + ' ' + 'line: '+ str(i) + ' 未拦截')
            # copy_file(file,'.\\aes_bypass\\')
        else:
            print('序号:' + str(count) + ' ' + 'line: '+ str(i) + ' 已拦截')
            success = success + 1
            # copy_file(file,'.\\command-wubao\\')
    print("一共发送样本数量：{}".format(max_row_num))
    print("拦截数：{}".format(success))
    print("未拦截数：{}".format(max_row_num - success))
    print("检测率：" + str(success / max_row_num))


def single_thread_test(url,port,file_dir):
    dir = []
    success = 0
    count = 0
    if file_dir == 'white_all':
        for key,value in white_payload_path.items():
            dir += read_dir(value)
    elif file_dir == 'black_all':
        for key,value in black_payload_path.items():
            dir += read_dir(value)
    else:
        if file_dir[-1] != '\\' and file_dir[-1] != '/':
            file_dir = file_dir + '/'
        dir = read_dir(file_dir)
    total = len(dir)
    for file in dir:
        content = read_file(file)
        try:
            count = count + 1
            result  = send(url,int(port),content)

            #print(result)
        except TimeoutError:
            print('序号:'+str(count) + ' ' + file + ' 连接超时')
            #copy_file(file,'.\\outtime\\')
            continue
        except ConnectionResetError:
            print('序号:'+str(count) + ' ' + file + ' 已拦截')
            success = success + 1
            continue
        except ConnectionAbortedError:
            continue
        #print(result)
        if result.find('403') == -1:
            print('序号:'+str(count) + ' ' + file + ' 未拦截')
            #copy_file(file,'.\\aes_bypass\\')
        else:
            print('序号:'+str(count) + ' ' + file + ' 已拦截')
            success = success + 1
            #copy_file(file,'.\\command-wubao\\')
    print("一共发送样本数量：{}".format(total))
    print("拦截数：{}".format(success))
    print("未拦截数：{}".format(total-success))
    print("检测率："+str(success/total))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Target ip;Example:10.88.1.220")
    parser.add_argument("-p", "--port", help="Target port;Example:8001")
    parser.add_argument("-d", "--dir", help="Target file;Example:D:\pythonProject\sockethttp\\text")
    parser.add_argument("-t", "--threads", help="thread number;Example:-t 10代表10个线程")
    parser.add_argument("-w","--white",help="白流量测试；Example: -w white_base64 表示测试white_base64类型白流量，all测试全部类型")
    parser.add_argument("-b", "--black", help="黑流量测试；Example: -b php_serilize 表示测试php_serilize类型黑流量，all测试全部类型")
    parser.add_argument("-x", "--xlsx", help="从xlsx中读取payload测试，要求xlsx文件第一列为payload Example: -x ./xxx.xlsx")
    args = parser.parse_args()
    if args.threads == None:
        if args.white != None:
            if args.white == 'all':
                single_thread_test(args.url,int(args.port),'white_all')
            else:
                single_thread_test(args.url,int(args.port),white_payload_path[args.white])
        if args.black != None:
            if args.black == 'all':
                single_thread_test(args.url,int(args.port),'black_all')
            else:
                single_thread_test(args.url,int(args.port),black_payload_path[args.black])
        if args.dir != None:
            single_thread_test(args.url, int(args.port),args.dir)
        if args.xlsx != None:
            send_from_xlsx(args.url,int(args.port),args.xlsx)


    else:
        muti_thread_test(args.url,int(args.port),args.dir,int(args.threads))

    #muti_thread_test(args.url,int(args.port),args.file,int(args.threads))
    # content = read_file('D:\pythonProject\sockethttp\\bypass\\1147.txt')
    # print(content)
    # result = send('99.99.99.88',80,content)
    # print(result)
