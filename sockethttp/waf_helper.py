import HackRequests

hack = HackRequests.hackRequests()
raw = '''
GET /?id=select%20name%20from%20users HTTP/1.1
Host: x.hacking8.com
Connection: Keep-Alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
'''
hh = hack.httpraw(raw=raw,real_host="10.51.15.107")
print(hh.text())