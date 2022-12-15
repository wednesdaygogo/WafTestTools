import socket
import os
import argparse

import threading
from concurrent.futures import ThreadPoolExecutor,as_completed


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
            #copy_file(file,'.\\text\\')


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

def single_thread_test(url,port,file_dir):

    success = 0

    dir = read_dir(file_dir)
    total = len(dir)
    for file in dir:
        content = read_file(file)
        try:
            result  = send(url,int(port),content)
            #print(result)
        except TimeoutError:
            print(file + ' 连接超时')
            #copy_file(file,'.\\outtime\\')
            continue
        except ConnectionResetError:
            print(file + ' 已拦截')
            success = success + 1
            continue
        except ConnectionAbortedError:
            continue
        #print(result)
        if result.find('403') == -1:
            print(file + ' 未拦截')
            #copy_file(file,'.\\beforechange\\')
        else:
            print(file + ' 已拦截')
            success = success + 1
            #copy_file(file,'.\\QMYES\\')
    print("一共发送样本数量：{}".format(total))
    print("拦截数：{}".format(success))
    print("未拦截数：{}".format(total-success))
    print("检测率："+str(success/total))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Target ip;Example:10.88.1.220")
    parser.add_argument("-p", "--port", help="Target port;Example:8001")
    parser.add_argument("-f", "--file", help="Target file;Example:D:\pythonProject\sockethttp\\text")
    parser.add_argument("-t", "--threads", help="thread number;Example:-t 10代表10个线程")
    args = parser.parse_args()
    if args.threads == None:
        single_thread_test(args.url,int(args.port),args.file)
    else:
        muti_thread_test(args.url,int(args.port),args.file,int(args.threads))

    #muti_thread_test(args.url,int(args.port),args.file,int(args.threads))
    # content = read_file('D:\pythonProject\sockethttp\\bypass\\1147.txt')
    # print(content)
    # result = send('99.99.99.88',80,content)
    # print(result)
