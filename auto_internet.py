from bs4 import BeautifulSoup
import requests
import time

while True:
    baidu_request=requests.get("https://www.baidu.com/")
    if(baidu_request.status_code==200):
        baidu_request.encoding = 'utf-8'
        baidu_request_bsObj = BeautifulSoup(baidu_request.text, 'html.parser')
        baidu_input = baidu_request_bsObj.find(value="百度一下")
        if baidu_input==None:
            print("未联网...")
        print("已联网...")
    else:
        print("已联网...")
    
    time.sleep(30)