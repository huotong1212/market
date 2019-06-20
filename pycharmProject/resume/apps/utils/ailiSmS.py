#!/usr/bin/env python
#coding=utf-8
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from resume import settings

class AliSms(object):
    def __init__(self,accessKey,accessSecret):
        self.client = AcsClient(accessKey, accessSecret)
        self.request = CommonRequest()

    def sendSMS(self,phoneNum,code):
        self.request.set_accept_format('json')
        self.request.set_domain('dysmsapi.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_protocol_type('https') # https | http
        self.request.set_version('2017-05-25')
        self.request.set_action_name('SendSms')

        self.request.add_query_param('PhoneNumbers', phoneNum)
        self.request.add_query_param('SignName', settings.SIGNNAME)
        self.request.add_query_param('TemplateCode', settings.TEMPLATE_CODE)
        print("{\"code\":\"%s\"}"%(code))
        self.request.add_query_param('TemplateParam', "{\"code\":\"%s\"}"%(code))


        response = self.client.do_action_with_exception(self.request)
        # python2:  print(response)
        print(str(response, encoding = 'utf-8'))
        result = str(response, encoding = 'utf-8')
        result = json.loads(result)
        return result
#if __name__ == "__main__":
    # alisms = AliSms(settings.ACCESS_KEYID, settings.ACCESS_KEYID_SECRET)
    # alisms.sendSMS("17761864285","1235")
