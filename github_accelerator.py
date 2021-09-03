import requests
from bs4 import BeautifulSoup
import os
import subprocess

import platform
from logger import logger


def is_platform() -> str:
    type = platform.system()
    logger.info("the system is {}".format(type))
    return type


class gitip:
    def __init__(self, ip_list):
        super().__init__()
        self.ip_list = ip_list
        self.ip_1 = 'https://github.com.ipaddress.com/' # github.com
        self.ip_2 = 'https://fastly.net.ipaddress.com/github.global.ssl.fastly.net' # github.global.ssl.fastly.net
        self.ip_3 = 'https://github.com.ipaddress.com/assets-cdn.github.com' # assets-cdn.github.com
        self.ip_4 = 'https://githubusercontent.com.ipaddress.com/raw.githubusercontent.com'

    def get_1(self): # github.com
        response = requests.get(self.ip_1)
        soup = BeautifulSoup(response.text, features = 'html.parser')
        self.ip_list.append(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    github.com')
    def get_2(self): # github.global.ssl.fastly.net
        response = requests.get(self.ip_2)
        soup = BeautifulSoup(response.text, features = 'html.parser')
        self.ip_list.append(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    github.global.ssl.fastly.net')
    def get_3(self): # assets-cdn.github.com
        response = requests.get(self.ip_3)
        soup = BeautifulSoup(response.text, features = 'html.parser')
        ips = soup.find_all('li')
        for i in range(4):
            self.ip_list.append(ips[i].text + '    assets-cdn.github.com')
    def get_4(self): # assets-cdn.github.com
        response = requests.get(self.ip_4)
        soup = BeautifulSoup(response.text, features = 'html.parser')
        ips = soup.find_all('li')
        for i in range(4):
            self.ip_list.append(ips[i].text + '    raw.githubusercontent.com')

if __name__ == '__main__':
    ip_list = []
    error = 0
    github = gitip(ip_list)
    try:
        github.get_1()
    except:
        print('github.com 申请出错')
        error+=1
    try:
        github.get_2()
    except:
        print('github.global.ssl.fastly.net 申请出错')
        error+=1
    try:
        github.get_3()
    except:
        print('assets-cdn.github.com 申请出错')
        error+=1
    try:
        github.get_4()
    except:
        print('raw.githubusercontent.com 申请出错')
        error+=1        

    if error == 0:
        print('\n')
        for i in github.ip_list:
            print(i)
        print('\n')

    plat = is_platform()
    
    if plat=="Windows":
        try:
            subprocess.run("explorer.exe %s" % 'C:\Windows\System32\drivers\etc')
        except:
            print('请打开文件路径 C:\Windows\System32\drivers\etc 更改hosts文件')
    if plat=="Darwin":
        try:
            os.system("open /etc")
        except:
            print('请打开文件路径 /etc 更改hosts文件')

    print("按下回车以结束程序...")
    os.system('read')
    
