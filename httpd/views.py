# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time,datetime
import simplejson
import re
import os
import multiprocessing
import subprocess
import logging
import validators

# Create your views here.

@csrf_exempt
def index(request):
    dict = {}
    info = 'Data log save success'
    # Handle Post Data
    try:
        if request.method == 'POST':
            #json_data = json.loads(request.body.decode("utf-8"))
            json_data = simplejson.loads(request.body)
            logger_msg("request: "+ str(json_data),"info")

            #list
            type = json_data["json_data"][0]["type"]
            domain = json_data["json_data"][0]["domain"]
            path = json_data["json_data"][0]["path"]
            port = json_data["json_data"][0]["port"]
        else:
            logger_msg("Wrong Request Method: GET","error")
            return HttpResponse("Wrong Request Method:'GET'")
            
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger_msg(info)  
    
    
    # Data Check 
    url = "http://" + str(domain) +":" + str(port) + str(path)
    print url

    if is_valid_url(url) == False:
        logger_msg("Wrong Domain or Path Format: " + url, "error")
        return HttpResponse("Wrong IP Format: " + dstip)
    elif is_valid_port(port) == False:
        logger_msg("Wrong Port Format: " + port,"error")
        return HttpResponse("Wrong Port Format: " + port)


    # CMD Call
    if type == "http":
        cmd_dict = cmd_curl_ncat(json_data)


    # Return Result
    dict = cmd_dict
    dict['domain'] = domain
    logger_msg("response:"+ str(dict),"info")
    json = simplejson.dumps(dict)
    return HttpResponse(json)

def is_valid_url(url):
    m = validators.url(url)
    return bool(m)

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

def is_valid_port(port):
    m = 0 < int(port) < 65535
    return bool(m)

def cmd_curl_ncat(json_data):
    cmd_dict = {}
    #Json Data
    domain = json_data["json_data"][0]["domain"]
    path = json_data["json_data"][0]["path"]
    port = json_data["json_data"][0]["port"]


    # CMD
    if str(port) == "443":
        url = "https://" + str(domain) +":" + str(port) + str(path)
    else:
        url = "http://" + str(domain) +":" + str(port) + str(path)

    cmd =  "curl -o /dev/null -s -w %{time_total} " + str(url)

    print cmd

    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output, error = p.communicate()

    print type(output)
    print output

    # output is str , and change to unicode
    latency = output.split('\n')
    print(type(latency[0]))
    print(latency)

    # Result
    # latency: get from result

    if p.returncode == 0:
        cmd_dict["lantency"]= latency[0]

    return cmd_dict


def logger_msg(msg,lvl="info"):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-s %(levelname)-s: %(message)s',
                    #datefmt='%m-%d %H:%M',
                    filename='/cloud/httpd/logs/httpd.log-'+time.strftime("%Y-%m-%d"),
                    filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    #formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    formatter = logging.Formatter('%(asctime)s  %(name)-12s: %(levelname)-8s %(message)s')

    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
 
    # Now, we can log to the root logger, or any other logger. First the root...
    #logging.info(msg)
 
    # Now, define a couple of other loggers which might represent areas in your
    # application:
 
    logger1 = logging.getLogger('httpd')


    if lvl == "error":
        logger1.error(msg)
    else:
        logger1.info(msg)


   
