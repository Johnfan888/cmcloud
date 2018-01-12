#!/usr/bin/env python
# encoding:utf-8
import json,sys,argparse
from zabbix_api import ZabbixAPI
server = "http://192.168.18.25/zabbix"
username = "Admin"
password = "zabbix"
zapi = ZabbixAPI(server=server, path="", log_level=0)
zapi.login(username, password)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="host name")
    parser.add_argument("-t", "--templates", help="template name")
    # 解析所传入的参数
    args = parser.parse_args()
    if not args.host:
        args.host = raw_input(‘host: ‘)
    if not args.templates:
        args.templates = raw_input(‘templates: ‘)
    return args

def get_host_id(host):
    get_host_id = zapi.host.get(
        {
            "output": "hostid",
            "filter": {
                "host":host.split(",")
            }
        }
)
    host_id = []
    host_id.append([I[‘hostid‘] for I in get_host_id])
    return host_id[0]
def get_templates_id(templates):
    templates_id = zapi.template.get(
    {
        "output": "templateid",
        "filter": {
            "host":templates.split(",")
        }
    }
)
    return templates_id
    
def template_massadd(template_id,host_id):
     template_add = zapi.template.massadd(
        {
            "templates": template_id,
            "hosts": host_id
            }
)
     return "host add template success"
     
if __name__ == "__main__":
    args = get_args()
    host_id = get_host_id(args.host)
    template_id = get_templates_id(args.templates)
    if len(host_id) == len(args.host.split(‘,‘)):
        if len(template_id) == len(args.templates.split(‘,‘)):
            print template_massadd(template_id,host_id)
        else:
            print "template not exist"
    else:
        print "host not exist"
