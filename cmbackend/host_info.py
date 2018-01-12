# /usr/bin/env python
# encoding:utf-8
import json
import sys
from auth import Zabbix_Auth_Code,Zabbix_Url_Request
#zabbix_url = "http://192.168.18.25/zabbix/api_jsonrpc.php"
#zabbix_header = {"Content-Type": "application/json"}
class Host_Action(object):
    def __init__(self,zabbix_url,zabbix_header,host_name=None,visible_name=None,*args,**kwargs):
        '''
        实现的功能：获取主机id，增、删主机，更新zabbix主机资产表
        :param zabbix_url: 访问zabbix的URL
        :param zabbix_header:  访问头部
        :param host_name:  hostname
        :param visible_name: 可见的主机名
        :param args:
        :param kwargs:
        '''
        self.zabbix_url = zabbix_url
        self.zabbix_header = zabbix_header
        self.host_name= host_name
        self.visible_name = visible_name
    def Get_Host_Id(self):
        auth_code, auth_id = Zabbix_Auth_Code(zabbix_url=self.zabbix_url,zabbix_header=self.zabbix_header)
        find_info = {}
        find_info['host'] = [self.host_name]
        find_info['name'] = [self.visible_name]
        for k,v in find_info.items():
            if v[0] == None:
                find_info.pop(k)
        get_host_id_data = json.dumps({
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": "extend",
                    "filter": find_info
                },
                "auth": auth_code,
                "id": auth_id
            })
        host_info = Zabbix_Url_Request(zabbix_url=self.zabbix_url,data=get_host_id_data,zabbix_header=self.zabbix_header)
        print host_info
        if len(host_info['result']) != 0:
            hostid = host_info['result'][0]['hostid']
            #print hostid
            return hostid
        else:
            print '没有查询到主机hostids'
            return 0
    def Add_Host(self,host_ip,template_id=10001,group_id=2,type=1,main=1,userip=1,port="10050",dns="",
                 flag=0,host_inventory=None,*args,**kwargs):
        '''

        :param group_id: 主机关联的监控模本id(groupid)
        :param templateid:  主机关联的监控模板id(templateid)
        :param host_ip: 主机ip地址
        :param type:  1 - agent; 2 - SNMP; 3 - IPMI; 4 - JMX
        :param main: 0 - not default; 1 - default
        :param userip: 0 - connect using host DNS name; 1 - connect using host IP address for this host interface.
        :param port: Port number used by the interface
        :param dns:  0 - connect using host DNS name;1 - connect using host IP address for this host interface.
        :param flag:    是否维护主机资产，0 - 表示不录入；1 - 表示录入
        :param host_inventory:  主机资产表
        :param args:
        :param kwargs:
        :return:
        '''
        self.host_ip = host_ip
        self.type = type
        self.main = main
        self.userip = userip
        self.port = port
        self.flag = flag
        self.dns = dns
        self.host_inventory = host_inventory
        host_msg = {}
        if self.host_name == None:
            self.host_name = self.host_ip
        host_template_info =[{"templateid": template_id}]
        host_group_info = [{"groupid": group_id}]
        host_interfaces_info = [{
            "type": self.type,
            "main": self.main,
            "useip": self.userip,
            "ip": self.host_ip,
            "dns": self.dns,
            "port": self.port
        }]
        host_msg['host'] = self.host_name
        host_msg['name'] = self.visible_name
        host_msg['interfaces'] = host_interfaces_info
        host_msg['groups'] = host_group_info
        host_msg['templates'] = host_template_info
        if self.flag == 0:
            host_msg['inventory_mode'] = -1  # -1 - disabled; 0 - (default) manual; 1 - automatic.
        elif self.flag == 1:
            host_msg['inventory_mode'] = 0  # -1 - disabled; 0 - (default) manual; 1 - automatic.
        else:
            sys.exit(1)
        auth_code, auth_id = Zabbix_Auth_Code(zabbix_url=self.zabbix_url,zabbix_header=self.zabbix_header)
        host_info = json.dumps({
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": host_msg,
                "auth": auth_code,
                "id": auth_id
            })
        add_host = Zabbix_Url_Request(zabbix_url=self.zabbix_url,data=host_info,zabbix_header=self.zabbix_header)
        if add_host['result']['hostids']:
            print "增加被监控主机成功，主机id ： %s"%(add_host['result']['hostids'])

    def Del_Host(self,host_id):
        self.host_id = host_id
        auth_code, auth_id = Zabbix_Auth_Code(zabbix_url=self.zabbix_url,zabbix_header=self.zabbix_header)
        del_host_info = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [
                self.host_id,
            ],
            "auth": auth_code,
            "id": auth_id
        })
        host_del = Zabbix_Url_Request(self.zabbix_url,del_host_info,self.zabbix_header)
        print host_del
        #if host_del['error']

        if host_del['result']['hostids'] == self.host_id:
            print 'id为%s主机删除成功!!!'%self.host_id

    def Update_Host_Ienventory(self,host_id,host_inventory,*args,**kwargs):
        self.host_id = host_id
        self.host_inventory = host_inventory
        auth_code, auth_id = Zabbix_Auth_Code(zabbix_url=self.zabbix_url,zabbix_header=self.zabbix_header)
        host_msg = {}
        host_msg['hostid'] = self.host_id
        host_msg['inventory_mode'] = 0
        host_msg['inventory'] = self.host_inventory

        update_msg = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": host_msg,
                "auth": auth_code,
                "id": auth_id
            }
        )
        update_host_ienventory = Zabbix_Url_Request(zabbix_url=self.zabbix_url,data=update_msg,zabbix_header=self.zabbix_header)
        print update_host_ienventory

def Get_Group_Id(group_name,zabbix_url,zabbix_header,*args,**kwargs):
    '''
    通过组名获取组id
    :param group_name:  组名
    :return:
    '''
    auth_code, auth_id = Zabbix_Auth_Code(zabbix_url=zabbix_url,zabbix_header=zabbix_header)
    group_info = json.dumps({
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                   group_name,
                ]
            }
        },
        "auth":auth_code,
        "id": auth_id
    })
    groups_result = Zabbix_Url_Request(zabbix_url=zabbix_url,data=group_info, zabbix_header=zabbix_header)
    #print groups_result['result'][0]['groupid']
    return groups_result['result'][0]['groupid']


def Get_Template_Id(template_name,zabbix_url,zabbix_header,*args,**kwargs):
    '''
    通过模板名获取组id
    :param template_name: 模板名
    :return:
    '''
    auth_code,auth_id = Zabbix_Auth_Code(zabbix_url=zabbix_url,zabbix_header=zabbix_header)
    template_info = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        template_name
                    ]
                }
            },
            "auth": auth_code,
            "id": auth_id
        })
    template_result = Zabbix_Url_Request(zabbix_url=zabbix_url,date=template_info,zabbix_header= zabbix_header)
    #print template_result['result'][0]['templateid']
    return template_result['result'][0]['templateid']
