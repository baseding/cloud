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
            dstip = json_data["json_data"][0]["dstip"]
            sshhostip = json_data["json_data"][0]["sshhostip"]
            if type == "tcp ping":
                port = json_data["json_data"][0]["port"]
        else:
            logger_msg("Wrong Request Method: GET","error")
            return HttpResponse("Wrong Request Method:'GET'")
            
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger_msg(info)  
    
    
    # Data Check 
    if is_valid_ip(dstip) == False:
        logger_msg("Wrong IP Format: " + dstip,"error")
        return HttpResponse("Wrong IP Format: " + dstip)
    elif is_valid_ip(sshhostip) == False:
        logger_msg("Wrong IP Format: " + sshhostip,"error")
        return HttpResponse("Wrong IP Format: " + sshhostip)

    
    if type == "ping" or type == "tcp ping":
        if type == "tcp ping":
            if is_valid_port(port) == False:
                logger_msg("Wrong Port Format: " + port,"error")
                return HttpResponse("Wrong Port Format: " + port)
    else:
        logger_msg("Wrong Type Format: " + type,"error")
        return HttpResponse("Wrong Type Format: " + type )

    # CMD Call
    if type == "ping":
        cmd_dict = cmd_fping(json_data)
    elif type == "tcp ping":
        cmd_dict = cmd_tcping(json_data)

    # Return Result
    dict = cmd_dict
    dict['dstip'] = dstip
    ##dict['datetime'] = str(time.ctime())
    logger_msg("response:"+ str(dict),"info")
    json = simplejson.dumps(dict)
    return HttpResponse(json)


def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

def is_valid_port(port):
    m = 0 < int(port) < 65535
    return bool(m)

def cmd_fping(json_data):
    cmd_dict = {}
    #Json Data
    type = json_data["json_data"][0]["type"]
    dstip = json_data["json_data"][0]["dstip"]
    srcip = json_data["json_data"][0]["srcip"]
    sshhostip = json_data["json_data"][0]["sshhostip"]

    # CMD
    #cmd = "fping -p 100 -c 5 "+ str(dstip)
    #cmd = "fping -c 5 "+ str(dstip)
    
    if is_valid_ip(srcip):
        cmd =  "ssh " + str(sshhostip) + " ' fping -c 5 " + str(dstip) + " -S " + str(srcip) + " ' "
    else:
        cmd =  "ssh " + str(sshhostip) + " ' fping -c 5 " + str(dstip) + " ' "

    print cmd

    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output, error = p.communicate()

    latency = output.split('\n')
    #print(latency[4])

    # List len will be ping time (5) + 1
    fping_success_num = len(latency)

    # Result
    # avg: get from the last fping success result:
    # loss: get from caculate
    if p.returncode:
        cmd_dict["loss"]= 100
        cmd_dict["avg"]= 0

    elif p.returncode == 0:
        result = re.split("\(|%| ",latency[fping_success_num - 2 ])
        cmd_dict["loss"]= 100 - ((fping_success_num - 1) * 100 / 5 )
        cmd_dict["avg"]= result[8]

    return cmd_dict


def cmd_tcping(json_data):
    cmd_dict = {}
    #Json Data
    dstip = json_data["json_data"][0]["dstip"]
    sshhostip = json_data["json_data"][0]["sshhostip"]
    srcip = json_data["json_data"][0]["srcip"]
    port = json_data["json_data"][0]["port"]

    # CMD /dev/null replace vz
    if is_valid_ip(srcip):
        cmd = "ssh " + str(sshhostip) + " 'ncat -w4 --send-only -s " + str(srcip) + " " + str(dstip) +" "+ str(port) + " </dev/null' "
    else:
        cmd = "ssh " + str(sshhostip) + " 'ncat -w4 --send-only -s " + str(srcip) + " " + str(dstip) +" "+ str(port) + " </dev/null' "

    print cmd

    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output, error = p.communicate()

    if p.returncode:
        cmd_dict["port_status"] = 1
    elif p.returncode == 0:
        cmd_dict["port_status"] = 0

    return cmd_dict


def logger_msg(msg,lvl="info"):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-s %(levelname)-s: %(message)s',
                    #datefmt='%m-%d %H:%M',
                    #filename='/cloud/pings/logs/pings.log-'+time.strftime("%Y-%m-%d"),
                    filemode='a')
 
    # Now, define a couple of other loggers which might represent areas in your
    # application:

    logger1 = logging.getLogger('pings')

    LOG_FILE = '/cloud/pings/logs/pings.log'
    filehandler = logging.handlers.TimedRotatingFileHandler(LOG_FILE,when='midnight',interval=1,backupCount=90)
    formatter = logging.Formatter('%(asctime)s %(name)-s %(levelname)-s: %(message)s')
    filehandler.setFormatter(formatter)
    logger1.addHandler(filehandler)


    if lvl == "error":
        logger1.error(msg)
    else:
        logger1.info(msg)


   
