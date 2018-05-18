#/usr/bin/env python
#coding:utf-8

import json
import urllib2
from urllib2 import URLError
import sys
import xlrd

class ZabbixTools:
    def __init__(self):
        self.url = 'http://21.254.247.73/api_jsonrpc.php'
        self.header = {"Content-Type":"application/json"}



    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": "admin",
                                      "password": "admin@watone.com"
                                      },
                           "id": 0
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, please Check your name and password:", e.code
        else:
            response = json.loads(result.read())
            result.close()
            self.authID = response['result']
            return self.authID

    def host_get(self,hostName):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"host.get",
                           "params":{
                                     "output":["hostid","name"],
                                     "filter":{"host":hostName}
                                     },
                           "auth":self.user_login(),
                           "id":1,
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])


        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            result.close()
            print "Number Of %s: " % hostName, len(response['result'])
            lens=len(response['result'])
            if lens > 0:
                return response['result'][0]['name']
            else:
                return ""


    def hostgroup_get(self, hostgroupName):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"hostgroup.get",
                           "params":{
                                     "output": "extend",
                                     "filter": {
                                                "name": [
                                                         hostgroupName,
                                                         ]
                                                }
                                     },
                           "auth":self.user_login(),
                           "id":1,
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()

            lens=len(response['result'])
            if lens > 0:
                self.hostgroupID = response['result'][0]['groupid']
                return response['result'][0]['groupid']
            else:
                print "no GroupGet result"
                return ""


    def template_get(self, templateName):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method": "template.get",
                           "params": {
                                      "output": "extend",
                                      "filter": {
                                                 "host": [
                                                          templateName,
                                                          ]
                                                 }
                                      },
                           "auth":self.user_login(),
                           "id":1,
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            self.templateID = response['result'][0]['templateid']
            return response['result'][0]['templateid']

    #def host_create(self, hostName,visibleName,hostIp,dnsName,proxyName, hostgroupName, templateName1, templateName2):
    def host_create(self, hostName,visibleName,hostIp,dnsName, hostgroupName, templateName1):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"host.create",
                           "params":{
                                     "host": hostName,
                                     "name": visibleName,
                                    # "proxy_hostid": self.proxy_get(proxyName),
                                     "interfaces": [
                                                        {
                                                            "type": 3,
                                                            #1是agent 2 是snmp
                                                            "main": 1,
                                                            "useip": 1,
                                                            "ip": hostIp,
                                                            "dns": dnsName,
                                                            "port": "623"
                                                        }
                                                    ],
                                    "groups": [
                                                    {
                                                        "groupid": self.hostgroup_get(hostgroupName)
                                                    }
                                               ],
                                   "templates": [
                               #这里定义模板在哪个群组里面，但是只有放到这个组里才能识别，不知道为什么

                                                    {
                                                        "templateid": self.template_get(templateName1)

                                                    },
                                                   # {

                                                    #    "templateid": self.template_get(templateName2)
                                                    #}
                                                  ],
                                     },
                           "auth": self.user_login(),
                           "id":1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "host : %s is created!   id is  %s\n" % (hostip, response['result']['hostids'][0])
            self.hostid = response['result']['hostids']
            return response['result']['hostids']

#    def proxy_get(self, ProxyName):
#        data = json.dumps({
#                           "jsonrpc":"2.0",
#                           "method": "proxy.get",
#                           "params": {
#                                      "output": "extend",
#                                      "selectInterface": "extend",
#                                      "filter": {
#                                          "host": [ ProxyName, ]
#                                      }
#                                      },
#                           "auth":self.user_login(),
#                           "id":1,
#                           })
#
#        request = urllib2.Request(self.url, data)
#        for key in self.header:
#            request.add_header(key, self.header[key])
#
#        try:
##            result = urllib2.urlopen(request)
#        except URLError as e:
#            print "Error as ", e
#        else:
#            response = json.loads(result.read())
#            result.close()
#            self.templateID = response['result'][0]['proxyid']
#            return response['result'][0]['proxyid']





if __name__ == '__main__':

    test = ZabbixTools()

   # workbook = xlrd.open_workbook(sys.argv[1])
    workbook = xlrd.open_workbook('80.xlsx')
    for row in xrange(workbook.sheets()[0].nrows):
        hostname=workbook.sheets()[0].cell(row,0).value
        visible=workbook.sheets()[0].cell(row,1).value
        hostip=workbook.sheets()[0].cell(row,2).value
        dnsname=workbook.sheets()[0].cell(row,3).value
        hostgroup=workbook.sheets()[0].cell(row,4).value
        hosttemp=workbook.sheets()[0].cell(row,5).value
        hostgroup=hostgroup.strip()
        hostnameGet=test.host_get(hostname)
        if hostnameGet.strip()=='':
             test.host_create(hostname,visible,hostip,dnsname,hostgroup,hosttemp)
        else:
            print "%s have exist! Cannot recreate !\n" % hostnameGet
