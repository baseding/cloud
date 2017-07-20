# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import ruamel.yaml as yaml
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, DescribeDomainRecordInfoRequest, AddDomainRecordRequest, DescribeDomainsRequest



# Create your views here.

# 1. Create AcsClient Instantance
client = AcsClient(
    str("LTAIp8HQFmAC0FIo"),
    str("PwrU39MPMiO6NE4PaznxQ4Zi6CC6E2"),
    str("cn-shanghai"),
);


#
def index(request):
    result = describedomains()
    return HttpResponse("result: " + result["Domain"][0]["DomainName"])

def records(request):
    result = describedomainrecords()
    print(result["DomainRecords"])
    print(result["DomainRecords"]["Record"][0]["RR"])


    for r in result["DomainRecords"]["Record"]:
        print r["RR"] + r["DomainName"] + r["RecordId"]

    return HttpResponse("result: " + result["DomainRecords"]["Record"][0]["RR"])



def describedomains():

    # 2. Create request, with params 
    request = DescribeDomainsRequest.DescribeDomainsRequest()
    request.set_accept_format('json')


    # 3. Send API request,and print response 
    #response = yaml.safe_load(client.do_action_with_exception(request)).get('Domains')
    response = yaml.safe_load(client.do_action_with_exception(request)).get('Domains')

    print(response)
    return(response)

def describedomainrecords(): 
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName("azza.com.cn")
    request.set_accept_format('json')

    # 3. Send API request,and print response 
    #response = client.do_action_with_exception(request)
    #response = json.loads(client.do_action_with_exception(request)).get('Domains').get('DomainId')
    response = yaml.safe_load(client.do_action_with_exception(request))

    print(response)
    return(response)
