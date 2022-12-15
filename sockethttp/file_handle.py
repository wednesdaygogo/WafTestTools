import os
import random
import base64
import download_picture

def get_filename(path):
    filelist = os.listdir(path)
    return filelist

def read_file(path):
    with open(path,encoding='utf-8',errors='ignore') as f:
        return f.read()

def write_file(path):
    count = 0
    filenames = get_filename(path)
    for filename in filenames:
        file_path = path + filename
        taget_filename = filename.replace(" ","")
        content = read_file(file_path)
        with open('./black_list/{}'.format(taget_filename),'w',encoding='utf-8') as f:
            f.write(content)
        print('写入成功 文件名:{}'.format(filename))
        count = count + 1
    print('共处理文件名{}个'.format(count))

def generate_random_str(ip,port,length=16,encode=None,filename="N"):
    random_str = ''
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890`~!@#$%^&*()_-+=[{]};:\'\",<.>/?|\\'
    str_len = len(base_str) - 1
    for i in range(length):
        random_str += base_str[random.randint(0,str_len)]
    if encode =="base64":
        random_str = base64_encode(random_str)
        payload = generate_http_payload(ip, port, random_str,filename)
    else:
        payload = generate_http_payload(ip,port,random_str,filename)
    return payload

def generate_internet_str(ip,port,file,encode=None):
    content = read_file("./post_payload/{}".format(file))
    if encode == "base64":
        internet_str = base64_encode(content)
        payload = generate_http_payload(ip,port,internet_str,file)
    else:
        payload = generate_http_payload(ip, port, content, file)
    return payload

def generate_picture(ip,port,keyword=None,pages=10):
    if os.path.exists("picture"):
        pass
    else:
        download_picture.get_images_from_baidu(keyword,pages,"picture")
        filenames = get_filename("picture")
        for filename in filenames:
            generate_http_payload(ip,port,read_file("picture\\"+filename))


def base64_encode(str):
    str_encode = base64.b64encode(str.encode('utf-8'))
    str_encode = str_encode.decode('utf-8')
    return str_encode

def generate_http_payload(ip,port,payload,filename):
    content = read_file('http.txt')
    if port == 80:
        host = ip
    else:
        host = ip+":"+str(port)
    http = content.replace("%ip",host).replace("%length",str(len(payload))).replace("%payload",payload).replace("%file",filename)
    return http

def whitefile_write(ip,port,type,length=16,num=2000,encode=None):
    if type == "random":
        path = './white_list/base64/'
        path = path.strip()
        path = path.rstrip("\\")
        isexist = os.path.exists(path)
        if not isexist:
            os.makedirs(path)
        for i in range(0,num):
            with open(path+str(i)+'.txt','w',encoding='utf-8') as f:
                f.write(generate_random_str(ip,port,length,encode,str(i)))
                print("成功生成文件:{}".format(path+str(i)+'.txt'))
    elif type == "internet":
        path = './white_list/internet_post/'
        path = path.strip()
        path = path.rstrip("\\")
        isexist = os.path.exists(path)
        if not isexist:
            os.makedirs(path)
        dic = get_filename("./post_payload")
        for filename in dic:
            with open(path+filename,'w',encoding='utf-8') as f:
                f.write(generate_internet_str(ip,port,filename,encode))
                print("成功生成文件:{}".format(path+filename))



if __name__ == '__main__':
    whitefile_write("99.99.99.88",80,"random",1000,2000,"base64")
    # x= base64_encode("ss())(Lp;ph88;\\@#$RF>?\":L{PO\$)P{IPK\#\)J\)\$NMM\:Kls")
    # print(x)

    #generate_picture("99.99.99.88",80,"cat")
    #print(get_filename("white_payload"))
    #generate_random_str("99.99.99.88",80,1500,"base64")
    #generate_http_payload("99.99.99.88",800,"abc=name")
    #write_file('./black-list/')
    #whitefile_write(20000)
   # y = base64_encode('sss')
   # print(y)