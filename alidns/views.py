# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ruamel.yaml as yaml
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, DescribeDomainRecordInfoRequest, AddDomainRecordRequest, DescribeDomainsRequest

#
from django.urls import reverse
from django.views import generic

from django.utils import timezone
#



# Create your views here.

# 1. Create AcsClient Instantance
client = AcsClient(
    str("LTAIp8HQFmAC0FIo"),
    str("PwrU39MPMiO6NE4PaznxQ4Zi6CC6E2"),
    str("cn-shanghai"),
);


#
@csrf_exempt
def index(request):
    domain_list = describedomains()
    #return HttpResponse("result: " + result["Domain"][0]["DomainName"])

    context = {'domain_list': domain_list["Domain"]}

    #return HttpResponse(domain_list["Domain"][0])
    return render(request, 'alidns/index.html', context) 

   

def records(request):
    domain_record_list = describedomainrecords()

    context = {
        'domain_record_list': domain_record_list["DomainRecords"]["Record"],
    }


    return render(request, 'alidns/records.html', context)

    #return HttpResponse(domain_record_list["DomainRecords"]["Record"])


def add(request):

    return render(request, 'alidns/add.html')


def describedomains():

    # 2. Create request, with params 
    request = DescribeDomainsRequest.DescribeDomainsRequest()
    request.set_accept_format('json')


    # 3. Send API request,and print response 
    #response = yaml.safe_load(client.do_action_with_exception(request)).get('Domains')
    response = yaml.safe_load(client.do_action_with_exception(request)).get('Domains')

    return(response)



def describedomainrecords(): 
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName("azza.com.cn")
    request.set_accept_format('json')

    # 3. Send API request,and print response 
    #response = client.do_action_with_exception(request)
    #response = json.loads(client.do_action_with_exception(request)).get('Domains').get('DomainId')
    response = yaml.safe_load(client.do_action_with_exception(request))

    return(response)


def adddomainrecord():
    # 2. Create request, with params
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_DomainName('azza.com.cn')
    request.set_RR('test4')
    request.set_Type('A')
    request.set_Value('4.4.4.4')
    #request.set_RecordId('3427090946544640')
    request.set_TTL('600')
    request.set_accept_format('json')


    # 3. Send API request,and print response
    response = yaml.safe_load(client.do_action_with_exception(request))

    return(response)







