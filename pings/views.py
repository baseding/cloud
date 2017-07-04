# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time,datetime
import simplejson

# Create your views here.

@csrf_exempt
def index(request):
    dict = {}
    info = 'Data log save success'
    try:
        if request.method == 'POST':
            #json_data = json.loads(request.body.decode("utf-8"))
            json_data = simplejson.loads(request.body)
            data = json_data["json_data"]

    except KeyError:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    
    dict['json_data'] = data
    dict['message'] = info
    dict['create_at'] = str(time.ctime())
    json = simplejson.dumps(dict)
    return HttpResponse(json)
