#-*-coding:utf-8-*-
from django.shortcuts import render
import os, sys, stat
import json
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response
#插入数据表
from . import models
#-----下面是api调用-----
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
import  xdrlib ,sys
sys.path.append('/usr/CMC/zabbix_api/')
import auth
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code
#连接数据库需要
from django.db import connection
import MySQLdb
from django.core import serializers #导入serializers模块
#-----------
import yaml
import commands

#读取yaml
#-----------------------
# Create your views here.
def main(request):
    #os.system("nc -l -p 8899 -k > /etc/zabbix/aa/shiyan.yaml")
    return render(request, 'main/main.html', )

def homepage(request):
    # os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    # host = models.chost.objects.all().values('hostName') #取数据库的数据
    # os.system('python /usr/CMC/zabbix_api/zabbix_getgroup.py')
    # hostgroups = models.chostgroups.objects.all().values('hostgroupsName')  # 取数据库的数据
    # os.system('python /usr/CMC/zabbix_api/zabbix_gettemplate.py')
    # templates = models.ctemplates.objects.all().values('templatesName')
    return render(request, 'main/homepage.html',locals())
    #locals()取所有本地数据

def add(request):
    return render(request, 'main/add.html', )

def add_host(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gettemplate.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_getgroup.py')
    hostgroups = models.chostgroups.objects.all()
    templates = models.ctemplates.objects.all()
    # templates ={'templatesName':templatesName}
    # 点提交进行的步骤
    if request.method == "POST":
        hostName = request.POST.get('hostName')
        hostIp = request.POST.get('hostIp')
        groupId = request.POST.get('hostgroupsId')
        templatesId = request.POST.get('templatesId')
        json_data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host":hostName,
                # "host": "hhh33",
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        # "ip": '192.168.1.100',
                        "ip": hostIp,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        # "groupid": '4'
                        "groupid": groupId,
                    }
                ],
                "templates": [
                    {
                        # "templateid": '10001'
                        "templateid": templatesId
                    }
                ],
                "inventory_mode": 0,
                "inventory": {
                    "macaddress_a": "01234",
                    "macaddress_b": "56768"
                }
            },
            "auth": auth_code,
            "id": 1
        }

        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
        # os.system('python /usr/CMC/zabbix_api/ll.py')
        # os.system('python /usr/CMC/zabbix_api/zabbix_createhost.py')  # 运行脚本
                add_host_data = {'hostName': hostName, 'hostIp': hostIp, 'groupId': groupId, 'templatesId': templatesId}

                return render(request, 'main/add_host.html',locals())
    return render(request,'main/add_host.html',locals())

def add_hostgroups(request):
    # 点提交进行的步骤
    if request.method == "POST":
        hostgroupsName = request.POST.get('hostgroupsName')
        json_data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": hostgroupsName,
            },
            "auth": auth_code,
            "id": 1
        }

        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
                aa = {'b': hostgroupsName}
                return render(request, 'main/add_hostgroups.html', aa)
    return render(request, 'main/add_hostgroups.html')

def add_templates(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_getgroup.py')
    hostgroups = models.chostgroups.objects.all()
    if request.method == "POST":
        hostgroups = models.chostgroups.objects.all()
        templateName = request.POST.get('templateName')
        hostgroupsId = request.POST.get('hostgroupsId')

        json_data = {
            "jsonrpc": "2.0",
            "method": "template.create",
            "params": {
                "host": templateName,
                "groups": {
                    "groupid": hostgroupsId,
                },
                # "hosts": [
                #     {
                #         "hostid": "10084"
                #     },
                #     {
                #         "hostid": "10090"
                #     }
                # ]
            },
            "auth": auth_code,
            "id": 1
        }
        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
                template_data = {'templateName': templateName, 'hostgroupsId': hostgroupsId}

                return render(request,'main/add_templates.html',locals())



    return render(request, 'main/add_templates.html',locals())

def add_itemgroups(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    host = models.chost.objects.all()
    if request.method == "POST":
        host = models.chost.objects.all()
        itemgroupsName = request.POST.get('itemgroupsName')
        hostId = request.POST.get('hostId')
        json_data = {
            "jsonrpc": "2.0",
            "method": "application.create",
            "params": {
                "name": itemgroupsName,
                "hostid": hostId,
            },
            "auth": auth_code,
            "id": 1
        }
        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
                itemgroups_data = {'itemgroupsName': itemgroupsName, 'hostId': hostId}

                return render(request, 'main/add_itemgroups.html', locals())
    return render(request, 'main/add_itemgroups.html',locals())

def add_items(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_getinterface.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_getitemgroup.py')
    interface = models.cinterface.objects.all()
    host = models.chost.objects.all()
    itemgroup = models.citemgroups.objects.all()
    # itemgroup = models.citemgroups.objects.all().values('itemgroupsName', 'itemgroupsId', 'hostId')
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", itemgroup)
    data1 = json.dumps(data)
    if request.method == "POST":
        host = models.chost.objects.all()#需要再次获取实现刷新
        # itemgroup = models.citemgroups.objects.all()
        itemName = request.POST.get('itemName')
        itemKey = request.POST.get('itemKey')
        hostId = request.POST.get('hostId')
        interfaceId = request.POST.get('interfaceId')
        itemgroups = request.POST.get('itemgroup')
        description = request.POST.get('description')
        valuetype = request.POST.get('valuetype')
        datatype = request.POST.get('datatype')
        #------------------
        json_data = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "name": itemName,
                "key_": itemKey,
                "hostid": hostId,
                "interfaceid": interfaceId,
                "type": 0,  # 0 - Zabbix agent; 1 - SNMPv1 agent;
                "value_type": valuetype,  # 0 - numeric float; 1 - character; 2 - log; 3 - numeric unsigned; 4 - text.
                "data_type": datatype,  # 0 - (default) decimal; 1 - octal; 2 - hexadecimal; 3 - boolean.
                # zai interface biaoli yilaiyu hostid
                "applications": itemgroups,
                "description": description,
                "delay": 30

            },
            "auth": auth_code,
            "id": 1
        }
        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

                all_data = {'itemName':itemName, 'itemKey':itemKey, 'hostId':hostId,
                    'interfaceId':interfaceId, 'itemgroups':itemgroups, 'description':description,
                    'valuetype':valuetype, 'datatype':datatype}
                return render(request,'main/add_items.html',locals() )
    return render(request, 'main/add_items.html',locals())

def add_triggers(request):
    if request.method == "POST":
        triggersname = request.POST.get('triggersname')
        condition = request.POST.get('condition')
        description = request.POST.get('description')
        severity = request.POST.get('severity')
        # request json //create host
        json_data = {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": {
                "description": triggersname,
                "expression": condition,
                "comments": description,
                "priority": severity
            },
            "auth": auth_code,
            "id": 1
        }
        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)

        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
                trigger_data = {'triggersname': triggersname, 'condition': condition, 'description':description,
                                'severity':severity}

                return render(request, 'main/add_triggers.html', locals())

    return render(request, 'main/add_triggers.html',locals())

def add_action(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    host = models.chost.objects.all()
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    item = models.citem.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", item)
    data1 = json.dumps(data)
    os.system('python /usr/CMC/zabbix_api/zabbix_gettrigger.py')
    trigger = models.ctrigger.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data2 = serializers.serialize("json",trigger)
    data3 = json.dumps(data2)
    if request.method == "POST":
        actionName = request.POST.get('actionName')
        hostId = request.POST.get('hostId')
        itemId = request.POST.get('itemId')
        osc = request.POST.get('osc')
        triggerId =request.POST.get('triggerId')
        # ---------------------------------------------取list-----------------------------
        from1 = request.POST.getlist('from1')
        from1=from1[1:]#--因为前段有一个空值需要去除第一个
        to1 = request.POST.getlist('to1')
        to1 = to1[1:]
        OpcommandhostId1 = request.POST.getlist('OpcommandhostId1')
        OpcommandhostId1 = OpcommandhostId1[1:]
        commands1 = request.POST.getlist('Commands1')
        commands1 = commands1[1:]
        stepduration1 = request.POST.getlist('stepduration1')
        stepduration1 = stepduration1[1:]
        #-----------------------------上为命令下为邮件-------------------------------------
        stepduration2= request.POST.getlist('stepduration2')
        stepduration2=stepduration2[1:]
        from2 = request.POST.getlist('from2')
        from2 = from2[1:]
        to2 = request.POST.getlist('to2')
        to2 = to2[1:]
        mediatype2 = request.POST.getlist('mediatype2')
        mediatype2 = mediatype2[1:]
        # ----------------------------对list进行填充进json-----------------------------
        # ---------执行命令------------
        json_command = []
        n = len(from1)
        for m in range(n):
            json_command1 = {
                "operationtype": 1,
                ##Possible values: 0 - send message; 1 - remote command; 2 - add host; 3 - remove host; 4 - add to host group; 5 - remove from host group;
                # 6 - link to template; 7 - unlink from template; 8 - enable host; 9 - disable host; 10 - set host inventory mode.
                "esc_period": stepduration1[m],
                # Duration of an escalation step in seconds. Must be greater than 60 seconds. If set to 0, the default action escalation period will be used.

                # Default: 0.
                "esc_step_from": from1[m],
                "esc_step_to": to1[m],
                "evaltype": 0,
                "opconditions": [
                    {
                        "conditiontype": 14,  # Type of condition. Possible values: 14 - event acknowledged.
                        "operator": 0,  #
                        "value": "0"
                    }
                ],
                # "opcommand_grp": [
                #   {
                #      "groupid": "2"#Host groups to run remote commands on.
                # }
                # ],
                "opcommand_hst": [
                    {
                        "hostid": OpcommandhostId1[m],
                        # Host to run remote commands on. ID of the host; if set to 0 the command will be run on the current host.
                    }
                ],
                "opcommand": {
                    "type": 0,  # Possible values: 0 - custom script; 1 - IPMI; 2 - SSH; 3 - Telnet; 4 - global script.
                    "command": commands1[m],  # Command to run.
                    "execute_on": 0,  # Possible values: 0 - Zabbix agent; 1 - Zabbix server.

                }
            }
            json_command.append(json_command1)  # 加入[]
        # json_command = ','.join(str(l) for l in json_command)  # 将数组的[]去掉
        # ----------发邮件------------
        json_mail = []
        i = len(from2)
        for j in range(i):
            json_mail1 = {
                "operationtype": 0,
                "esc_period": stepduration2[j],
                "esc_step_from": from2[j],
                "esc_step_to": to2[j],
                "evaltype": 0,
                "opmessage_grp": [
                    {
                        "usrgrpid": "7"
                    }
                ],
                "opmessage": {
                    "default_msg": 1,
                    "mediatypeid": mediatype2[j],
                }
            }

            json_mail.append(json_mail1)  # 加入[]
        # json_mail=','.join(str(k) for k in json_mail)#将数组的[]去掉
        # --------------------拼接直接相加list------

        json_html = json_command + json_mail
        # 类型list三者均是
        # print type(json_command)
        # print type(json_mail)
        # print type(json_html)
        # print json_html
        #     #request json //create host

        json_data = {
            "jsonrpc": "2.0",
            "method": "action.create",
            "params": {
                "name": actionName,  # action名字
                "eventsource": 0,  # 0 - event created by a trigger;
                # 1 - event created by a discovery rule;
                # 2 - event created by active agent auto-registration;
                # 3 - internal event.
                "status": 0,  # Whether the action is enabled or disabled.  0 - (default) enabled; 1 - disabled.
                "esc_period": osc,
                "def_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
                "def_longdata":"{\r\n\"Trigger status\": \"{TRIGGER.STATUS}\",\r\n\"Trigger name\": \"{TRIGGER.NAME}\",\r\n\"Trigger severity\": \"{TRIGGER.SEVERITY}\",\r\n\"Action name\": \"{ACTION.NAME}\",\r\n\"Event ID\": \"{EVENT.ID}\",\r\n\"Event value\": \"{EVENT.VALUE}\",\r\n\"Event status\": \"{EVENT.STATUS}\", \r\n\"Event time\": \"{EVENT.TIME}\",\r\n\"Event date\": \"{EVENT.DATE}\",\r\n\"Event age\": \"{EVENT.AGE}\",\r\n\"Event acknowledgement\": \"{EVENT.ACK.STATUS}\",\r\n\"Event acknowledgement history\": \"{EVENT.ACK.HISTORY}\",\r\n\"Item values\": \"{ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}\",\r\n\"Original event ID\": \"{EVENT.ID}\"\r\n}",
                "recovery_msg": 1,
                "r_longdata": "{\r\n\"Trigger status\": \"{TRIGGER.STATUS}\",\r\n\"Trigger name\": \"{TRIGGER.NAME}\",\r\n\"Trigger severity\": \"{TRIGGER.SEVERITY}\",\r\n\"Action name\": \"{ACTION.NAME}\",\r\n\"Event ID\": \"{EVENT.ID}\",\r\n\"Event value\": \"{EVENT.VALUE}\",\r\n\"Event status\": \"{EVENT.STATUS}\", \r\n\"Event time\": \"{EVENT.TIME}\",\r\n\"Event date\": \"{EVENT.DATE}\",\r\n\"Event age\": \"{EVENT.AGE}\",\r\n\"Event acknowledgement\": \"{EVENT.ACK.STATUS}\",\r\n\"Event acknowledgement history\": \"{EVENT.ACK.HISTORY}\",\r\n\"Item values\": \"{ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}\",\r\n\"Original event ID\": \"{EVENT.ID}\"\r\n}",
                "r_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
                "filter": {
                    "evaltype": 0,  # 0 - and/or; 1 - and; 2 - or; 3 - custom expression.
                    "conditions": [
                        {
                            "conditiontype": 2,
                            # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
                            # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
                            "operator": 0,
                            # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
                            "value": triggerId  # triggerid
                        },
                        # {
                        # "conditiontype": 1,
                        # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
                        # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
                        # "operator": 0,
                        # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
                        # "value": "10124"  # hostid
                        # },
                    ],

                },
                "operations": json_html,
                "recovery_operations": json_html,

            },
            "auth": auth_code,
            "id": 1
        }

        # print type(json_data)
        # print json_data
        #
        # 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response
                action_data={"actionName":actionName}
                return render(request, 'main/add_action.html',locals())
    return render(request, 'main/add_action.html',locals())

def add_action_child(request):
    if request.method == "POST":
        text1 = request.POST.get('text1')
        stepname=request.POST.get('sname1')
        text2 = request.POST.get('text2')
        fp = open("/etc/zabbix/aa/%s.py" %(stepname),'w+')
        fp.write(text1)
        fp.close()
        os.chmod("/etc/zabbix/aa/%s.py" %(stepname), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # mode:777
        os.chown("/etc/zabbix/aa/%s.py" %(stepname), 988, 983);#uid=988(zabbix) gid=983(zabbix) 组=983(zabbix)
        fp2 = open("/etc/zabbix/aa/%s.sh" %(stepname), 'w+')
        fp2.write(text2)
        fp2.close()
        os.chmod("/etc/zabbix/aa/%s.sh" %(stepname), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # mode:777
        os.chown("/etc/zabbix/aa/%s.sh" %(stepname), 988, 983);#uid=988(zabbix) gid=983(zabbix) 组=983(zabbix
        os.system("scp -p /etc/zabbix/aa/%s.py 192.168.1.90:/etc/zabbix/aa/%s.py" %(stepname,stepname))
        os.system("scp -p /etc/zabbix/aa/%s.sh 192.168.1.90:/etc/zabbix/aa/%s.sh" % (stepname,stepname))
        return render(request, 'main/add_action_child.html', locals())
    return render(request,'main/add_action_child.html',locals())
#-----------------------------------------------------------#


def monitoring(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    host = models.chost.objects.all()
    item = models.citem.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", item)
    data1 = json.dumps(data)
    os.system('python /usr/CMC/zabbix_api/zabbix_gettemplate.py')
    templates = models.ctemplates.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data2 = serializers.serialize("json", templates)
    data3 = json.dumps(data2)
    # if request.method == "POST":
    #
    #         chostId = request.POST.get('hostId')
    #         # 连接数据库按条件查询
    #         from django.db import connection
    #         cursor = connection.cursor()
    #         # 连接数据库
    #         cursor.execute("SELECT * FROM `main_citem` WHERE hostId=%s",[chostId])
    #         # item = cursor.fetchone()      #只有数据没有名字
    #         #取数据将列名带上
    #         index = cursor.description
    #         item = []
    #         for res in cursor.fetchall():
    #             row = {}
    #             for i in range(len(index) - 1):
    #                 row[index[i][0]] = res[i]
    #             item.append(row)
    #         # connect.close()
    #         # return result
    #         # 获取前端选中的hostname并返回

            # return render(request,'main/monitoring.html', locals())

    return render(request, 'main/monitoring.html',locals())

def diagnosis(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_gettrigger.py')
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    host = models.chost.objects.all()
    trigger = models.ctrigger.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", trigger)
    data1 = json.dumps(data)
    item = models.citem.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data2 = serializers.serialize("json", item)
    data3 = json.dumps(data2)
    # if request.method == "POST":
    #
    #         chostId = request.POST.get('hostId')
    #         # chostName =request.POST.get('hostName')
    #         # 连接数据库按条件查询
    #         from django.db import connection
    #         cursor = connection.cursor()
    #         # 连接数据库
    #         cursor.execute("SELECT itemId FROM `main_citem` WHERE hostId=%s",[chostId])
    #         itemId = cursor.fetchall()      #只有数据没有名字
    #         cursor.execute("SELECT * FROM `main_ctrigger` WHERE itemId in %s", [itemId])
    #         #取数据将列名带上
    #         index = cursor.description
    #         trigger = []
    #         for res in cursor.fetchall():
    #             row = {}
    #             for i in range(len(index) - 1):
    #                 row[index[i][0]] = res[i]
    #             trigger.append(row)
            # connect.close()
            # return result



            # return render(request,'main/diagnosis.html', locals())



    return render(request, 'main/diagnosis.html',locals())

def recovery(request):
    recovery = models.crecovery.objects.all().order_by("-eventId")#按照id倒叙取出
         #客户端发来的数据
    if 'actionName' in request.GET:  # 必须有if
        actionName = request.GET['actionName']
        fr = open('/etc/zabbix/aa/shiyan.yaml', "r")
        aa = yaml.load(fr)
        bb = []
        for i in aa:
            if '%s'%(actionName) in i:
                cc = {'actionStepName': i, 'returnValue': aa[i]['value']}
                bb.append(cc)
        bb=str(bb)
        cursor = connection.cursor()
        # 连接数据库
        cursor.execute("SELECT eventId from main_crecovery WHERE returnValue is NULL AND actionName=%s",[actionName])
        eventId = cursor.fetchone()      #取到eventId,
        cursor.execute("UPDATE main_crecovery set returnValue=%s where eventId=%s",[bb,eventId])
        cursor.close()
        return HttpResponse(json.dumps(actionName), content_type='application/json')
    return render(request,'main/recovery.html',locals())

def add_triggers_child(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    host = models.chost.objects.all()
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    item = models.citem.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", item)
    data1 = json.dumps(data)
    return render(request,'main/add_triggers_child.html',locals())
#----------------------------------------------------#


def view_hostgroups(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_getgroup.py')
    hostgroups = models.chostgroups.objects.all()  # 取数据库的数据
    # 下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", hostgroups)
    data1 = json.dumps(data)
    if 'hostgroupsId' in request.GET:#必须有if
        hostgroupsId = request.GET['hostgroupsId']
        json_data = {

                "jsonrpc": "2.0",
                "method": "hostgroup.delete",
                "params": [
                    hostgroupsId

                ],
                "auth": auth_code,
                "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(hostgroupsId), content_type='application/json')

    return render(request, 'main/view_hostgroups.html', locals())

def view_templates(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gettemplate.py')
    templates = models.ctemplates.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", templates)
    data1 = json.dumps(data)
    #接收ajax发送的值


    if 'triggerId' in request.GET:#必须有if
        triggerId = request.GET['triggerId']

        # 连接数据库按条件删除
        # from django.db import connection
        # cursor = connection.cursor()
        # cursor.execute("DELETE FROM `main_ctemplates` WHERE `templatesName` = %s", [namev])
        json_data ={

                "jsonrpc": "2.0",
                "method": "template.delete",
                "params": [
                    triggerId

                ],
                "auth": auth_code,
                "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(triggerId), content_type='application/json')
    return render(request, 'main/view_templates.html', locals())

def view_host(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gethost.py')
    host = models.chost.objects.all() #取数据库的数据
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", host)
    data1 = json.dumps(data)
    os.system('python /usr/CMC/zabbix_api/zabbix_getinterface.py')
    interface = models.cinterface.objects.all() #取数据库的数据
    #下面两步将数据库获得的queryset格式转换为json格式
    data2 = serializers.serialize("json", interface)
    data3 = json.dumps(data2)

    os.system('python /usr/CMC/zabbix_api/zabbix_getitemgroup.py')
    itemgroup = models.citemgroups.objects.all()
    # itemgroup = models.citemgroups.objects.all().values('itemgroupsName', 'itemgroupsId', 'hostId')
    #下面两步将数据库获得的queryset格式转换为json格式
    data4 = serializers.serialize("json", itemgroup)
    data5 = json.dumps(data4)
    if 'hostId' in request.GET:  # 必须有if
        hostId = request.GET['hostId']
        json_data = {

            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [
                hostId

            ],
            "auth": auth_code,
            "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(hostId), content_type='application/json')
    if 'UhostId' in request.GET:  # 必须有if
        hostId = request.GET['UhostId']
        hostStatus = request.GET['UhostStatus']
        json_data = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {
                        "hostid": hostId,
                        "status": hostStatus,
                    },
                    "auth": auth_code,
                    "id": 1

        }
        if len(auth_code) == 0:
                sys.exit(1)
        if len(auth_code) != 0:
                host_create_data = json.dumps(json_data)

                # create request object
                request2 = urllib2.Request(zabbix_url, host_create_data)
                for key in zabbix_header:
                    request2.add_header(key, zabbix_header[key])

                # get host list
                try:
                    result = urllib2.urlopen(request2)
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
                    # print response
        return HttpResponse(json.dumps(hostId), content_type='application/json')
    return render(request, 'main/view_host.html', locals())

def view_action(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_getaction.py')
    action = models.caction.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", action)
    data1 = json.dumps(data)
    if 'actionId' in request.GET:#必须有if
        actionId = request.GET['actionId']
        json_data={

                "jsonrpc": "2.0",
                "method": "action.delete",
                "params": [
                    actionId
                ],
                "auth": auth_code,
                "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(actionId), content_type='application/json')


    return render(request, 'main/view_action.html', locals())
def view_itemgroups(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_getitemgroup.py')
    itemgroups = models.citemgroups.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json", itemgroups)
    data1 = json.dumps(data)
    if 'itemgroupsId' in request.GET:  # 必须有if
        itemgroupsId = request.GET['itemgroupsId']
        json_data = {

            "jsonrpc": "2.0",
            "method": "application.delete",
            "params": [
                itemgroupsId

            ],
            "auth": auth_code,
            "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(itemgroupsId), content_type='application/json')

    return render(request, 'main/view_itemgroups.html', locals())

def view_items(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    item = models.citem.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json",item)
    data1 = json.dumps(data)
    if 'itemId' in request.GET:  # 必须有if
        itemId = request.GET['itemId']
        json_data = {

            "jsonrpc": "2.0",
            "method": "item.delete",
            "params": [
                itemId

            ],
            "auth": auth_code,
            "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(itemId), content_type='application/json')
    return render(request, 'main/view_items.html', locals())

def view_triggers(request):
    os.system('python /usr/CMC/zabbix_api/zabbix_gettrigger.py')
    trigger = models.ctrigger.objects.all()
    #下面两步将数据库获得的queryset格式转换为json格式
    data = serializers.serialize("json",trigger)
    data1 = json.dumps(data)
    os.system('python /usr/CMC/zabbix_api/zabbix_getitem.py')
    item = models.citem.objects.all()
    # 下面两步将数据库获得的queryset格式转换为json格式
    data2 = serializers.serialize("json", item)
    data3 = json.dumps(data2)
    if 'triggerId' in request.GET:  # 必须有if
        triggerId = request.GET['triggerId']
        json_data = {

            "jsonrpc": "2.0",
            "method": "trigger.delete",
            "params": [
                triggerId

            ],
            "auth": auth_code,
            "id": 1

        }
        if len(auth_code) == 0:
            sys.exit(1)
        if len(auth_code) != 0:
            host_create_data = json.dumps(json_data)

            # create request object
            request2 = urllib2.Request(zabbix_url, host_create_data)
            for key in zabbix_header:
                request2.add_header(key, zabbix_header[key])

            # get host list
            try:
                result = urllib2.urlopen(request2)
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
                # print response

        return HttpResponse(json.dumps(triggerId), content_type='application/json')

    return render(request, 'main/view_triggers.html', locals())
