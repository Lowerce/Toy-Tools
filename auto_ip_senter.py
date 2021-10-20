import json
from urllib.request import urlopen

import os
import time

import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 获取ip地址的网站
ip_url = 'https://api.ipify.org/?format=json'

# 配置文件名
config_file_name = '.global_ip.json'

# 第三方 SMTP 服务
mail_host = "smtp.163.com"       # SMTP服务器
mail_user = " "                  # 用户名(邮箱全名)    --须填写
mail_pass = " "                  # 授权密码，非登录密码 --须填写

sender = ' '    		# 发送邮箱  --须填写
receivers = [' ']       # 接收邮箱  --须填写

title = 'update_addr'  			# 邮件主题
content = ''    				# 邮件内容

# 检查配置文件及其权限
def check_configfile_exist():
    file_exist = os.access(config_file_name, os.F_OK)
    file_read  = os.access(config_file_name, os.R_OK)
    file_write = os.access(config_file_name, os.W_OK)
    return{'file_exist':file_exist,'file_read':file_read,'file_write':file_write}

def generate_configfile(ip_addr):
    config_construct = {
        "ip_addr": ip_addr
    }
    with open(config_file_name, "w", encoding='utf8') as fp:
        fp.write(json.dumps(config_construct,indent=4, ensure_ascii=False))
    fp.close()

def sendEmail():

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)         # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

localtime = time.localtime(time.time()) # 打印本地时间
print("\n" + time.asctime(localtime))

import socket
# 这种获取方式适用于开启VPN的情况 能够获得本机真实IP
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 获取ip地址
my_ip = str(json.load(urlopen(ip_url))['ip'])
self_ip = get_host_ip()

if self_ip!=my_ip:
    ip_addr = self_ip
else:
    ip_addr = my_ip


if(check_configfile_exist()['file_exist'] & check_configfile_exist()['file_write']):
    config_file = open(config_file_name,'r')
    read_context = json.load(config_file)
    old_ip = read_context['ip_addr']
    config_file.close()
    if (old_ip == ip_addr):
        print("ip address is up-to-date")
    else:
        content = "old ip address is : " + old_ip + '\n' + "new ip address is : " + ip_addr
        sendEmail()
        generate_configfile(ip_addr)
else:
    generate_configfile(ip_addr)
    content = "new ip address is : " + ip_addr
    sendEmail()