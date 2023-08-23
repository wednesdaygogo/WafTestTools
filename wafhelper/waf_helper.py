import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Target ip;Example:10.88.1.220")
    parser.add_argument("-p", "--port", help="Target port;Example:8001")
    parser.add_argument("-d", "--dir", help="Target file;Example:D:\pythonProject\sockethttp\\text")
    parser.add_argument("-t", "--threads", help="thread number;Example:-t 10代表10个线程")
    parser.add_argument("-w","--white",help="白流量测试；Example: -w white_base64 表示测试white_base64类型白流量，all测试全部类型")
    parser.add_argument("-b", "--black", help="黑流量测试；Example: -b php_serilize 表示测试php_serilize类型黑流量，all测试全部类型")
    parser.add_argument("-x", "--xlsx", help="从xlsx中读取payload测试，要求xlsx文件第一列为payload Example: -x ./xxx.xlsx")
    parser.add_argument("-xp", "--xlsxplus", help="从xlsx中读取payload测试，用于测试请求体和请求头分别在两列的表，测试完成后在原表的1，2列添加事件名称和测试结果")
    parser.add_argument("-df", "--dstfile", help="xlsxplus测试功能结果生成的目标文件")
    parser.add_argument("-c1", "--column1", help="xlsxplus测试功能参与拼接的列数1(有先后顺序，c1拼接在c2之前,c2不写的话就只读c1)")
    parser.add_argument("-c2", "--column2", help="xlsxplus测试功能参与拼接的列数1(有先后顺序，c1拼接在c2之前，c2不写的话就只读c1)")
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
        if args.xlsxplus != None:
            if args.column2 == None:
                send_from_xlsx_plus(args.url,int(args.port), args.xlsxplus,args.dstfile, int(args.column1))
            else:
                send_from_xlsx_plus(args.url, int(args.port), args.xlsxplus, args.dstfile, int(args.column1),int(args.column2))

    else:
        muti_thread_test(args.url,int(args.port),args.dir,int(args.threads))