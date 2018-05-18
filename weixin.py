#!/usr/bin/env python
#coding=utf-8
import urllib2
import json,sys
reload(sys)
sys.setdefaultencoding('utf8')

request = urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx02a1e9f68b56d66d&secret=2714c5a9c16a9ceb8ebdc92172b601c0')
response = request.read()
dict=json.loads(response)
token=dict["access_token"]

def main():
#        person_list=["o55ZfuM715QeUNyRR9JN0tEc_SlM","o55ZfuM715QeUNyRR9JN0tEc_SlM"]
#        num=0
#        for i in person_list:
	data = {"touser":sys.argv[1],"msgtype":"text", "text":{"content":(sys.argv[2])}}
        send_message(data)


def send_message(data):
        headers = {'Content-Type': 'application/json'}
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % token
        request = urllib2.Request(url=url, headers=headers, data=json.dumps(data,ensure_ascii=False))
        response = urllib2.urlopen(request)


#发送消息

if __name__ == "__main__":
        main()

