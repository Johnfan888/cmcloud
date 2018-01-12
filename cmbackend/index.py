# /usr/bin/env python
# encoding:utf-8
import yaml
from host_info import Host_Action,Get_Group_Id,Get_Template_Id
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    try:
        with open('config.yaml') as f:
            result = yaml.load(f)
        result_zabbix_info = result['Zabbix_Config']
        zabbix_url = result_zabbix_info['zabbix_url']
        zabbix_header = result_zabbix_info['zabbix_header']

        #删除主机
        host = Host_Action(zabbix_url=zabbix_url, zabbix_header=zabbix_header, host_name='192.168.1.84',
                           visible_name='t1')
        host_id = host.Get_Host_Id()
        host.Del_Host(host_id)
        #增加主机不带资产
        host = Host_Action(zabbix_url=zabbix_url, zabbix_header=zabbix_header, host_name='192.168.1.84',visible_name='t1')
        host.Add_Host(host_ip='192.168.1.84')

        #获取指定主机的hostid
        host = Host_Action(zabbix_url=zabbix_url,zabbix_header=zabbix_header,host_name='192.168.1.84')
        host_id = host.Get_Host_Id()
        print '主机192.168.1.84的id是: %s'%host_id

        #获取指定模本的id
        t_id = Get_Template_Id(template_name='Template OS Linux',zabbix_header=zabbix_header,zabbix_url=zabbix_url)
        print "模板Template OS Linux的id是：%s"%t_id

        #获取指定组的id
        Get_Group_Id(group_name='Linux servers',zabbix_header=zabbix_header,zabbix_url=zabbix_url)
        print "组Linux servers的id是：%s" % t_id



        host_inventory = {
            "type": "Linux Server",
            "name": "xxxxxxx",
            "os": "centos7.2",
            "os_full": "RedHat Centos 7.2",
            "os_short": "Centos 7.2",
            "serialno_a": "f729d3fa-fd53-4c5f-8998-67869dad349a",
            "macaddress_a": "00:16:3e:03:af:a0",
            "hardware_full": "cpu: 4c; 内存: 8G; 硬盘: 20G",
            "software_app_a": "docker",
            "software_app_b": "zabbix agent",
            "software_full": "docker zabbix-server ntpd",
            "contact": "xxx",  # 联系人
            "location": "阿里云 华北二",  # 位置
            "vendor": "阿里云",  # 提供者
            "contract_number": "",  # 合同编号
            "installer_name": "xx 手机: xxxxxxxxxx",  # 安装名称
            "deployment_status": "prod",
            "host_networks": "192.168.1.179",
            "host_netmask": "255.255.255.0",
            "host_router": "192.168.1.1",
            "date_hw_purchase": "2016-07-01",  # 硬件购买日期
            "date_hw_install": "2016-07-01",  # 硬件购买日期
            "date_hw_expiry": "0000-00-00",  # 硬件维修过期
            "date_hw_expiry": "0000-00-00",  # 硬件维修过期
            "date_hw_decomm": "0000-00-00",  # 硬件报废时间
            "site_city": "北京",
            "site_state": "北京",
            "site_country": "中国",
            "site_zip": "100000",  # 邮编
            "site_rack": "",  # 机架
        }

        #添加带资产的主机
        host = Host_Action(zabbix_url=zabbix_url, zabbix_header=zabbix_header, host_name='192.168.1.84')
        host_id = host.Get_Host_Id(host_inventory=host_inventory,flag=1)

        # 删除主机
        host = Host_Action(zabbix_url=zabbix_url, zabbix_header=zabbix_header, host_name='192.168.1.84',
                           visible_name='t1')
        host_id = host.Get_Host_Id()
        host.Del_Host(host_id)

    except Exception,e:
        print e
