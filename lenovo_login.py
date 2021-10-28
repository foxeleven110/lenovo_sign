#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cookielib
from pathlib import Path
import ast
#初始化 
_session = requests.session()
_session.cookies = cookielib.LWPCookieJar()
header1 = {
    "Host": "mclub.lenovo.com.cn",
    "Origin": "https://mclub.lenovo.com.cn",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://club.lenovo.com.cn/sign",
    "User-Agent": "Chrome/95.0.4638.54 Safari/537.36 Mozilla/5.0 ",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
####读取文件路的Cookies#######
def read_cook():
    print("读取存放文件中的COOKIES")
    with open('cookies.txt', 'r') as f:
        cook_r = str(f.read())
    return cook_r
####定义头部函数####
def init_header(host, origin, refer, cook):
    header = {
     	"Host": host,
    	"origin": origin,
    	"Cookie": cook,
    	"Connection": "keep-alive",
    	"Accept-Encoding": "gzip, deflate, br",
    	"Accept-Language": 'zh-CN,zh;q=0.9',
    	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    	'Connection': 'keep-alive',
    	"referer": refer,
    	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    	"Accept": "text/html,application/xml;q=0.9, text/javascript, */*; q=0.01",
    }
    return header




############登录加载############
header = {
        "Host": "reg.lenovo.com.cn",
        "origin": "https://reg.lenovo.com.cn",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'Cookie': 'sce=1; leid=1.xRPvBztGrts; LA_F_T_10000001=1634986394958; LA_C_Id=_ck21102318531419623772717075232; LA_R_T_10000001=1634986394958; LA_V_T_10000001=1634986394958; LA_M_W_10000001=_ck21102318531419623772717075232%7C10000001%7C%7C%7C; LA_C_C_Id=_sk202110231853160.62828300.9085; _ga=GA1.3.1325283140.1634986395; _gid=GA1.3.1891062882.1634986395; JSESSIONID=F4E731F857E83F5BAABD844714406BEC; qrtoken=l1984-6902c4c5-415f-4717-97af-d8771cdc1db0',
        "referer": "https://reg.lenovo.com.cn/auth/v1/login",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01","Host": "reg.lenovo.com.cn",
        "Connection": "keep-alive",
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': ": Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Accept": "text/html,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

def login():
    login_url = "https://reg.lenovo.com.cn/auth/v2/doLogin"
    
    
    post_data = {
    	"account": '用户名', #修改成自己的
    	"password": '密码密文',#修改成自己的
    	"ps": "1",
    	'codeid': None,
        'code': None,
    	"ticket": "e40e7004-4c8a-4963-8564-31271a8337d8",
    	"slide": "v2",
    	"t": "1634970353204"
    }
    ##以用户名登录按钮##
    
    rep = _session.post(login_url, headers=header, data=post_data)
    cook1 = requests.utils.dict_from_cookiejar(_session.cookies)
    #print(rep.content.decode())
    if rep.json()["msg"] == "success" :
    	print("登录成功")
    else:
    	print("登录失败")
    return cook1
    rep.close()	

####加载签到URL进行签到##一定要放在sign_list()前面否则会tr循环调用错误
def sign(token):
    print("进入签到程序")
    #定义签到URL#
    sign_url = "https://mclub.lenovo.com.cn/signadd"

    header_sign = {
        "Host": "mclub.lenovo.com.cn",
        "Origin": "https://mclub.lenovo.com.cn",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://club.lenovo.com.cn/sign",
        "User-Agent": "Chrome/95.0.4638.54 Safari/537.36 Mozilla/5.0 ",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        #'Cookie': cook_init
    }
    sign_data = {
        "_token": token,
        "memberSource": "0"
    }
    repon = _session.post(url="https://mclub.lenovo.com.cn/signadd", headers=header_sign, data=sign_data)
    print(repon.json())
    repon.close()
    cook_r = read_cook()
    sign_list(cook_r)

def sign_list(cook_fir):
    list_url = "https://mclub.lenovo.com.cn/signlist"
    header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/    avif,image    /webp,image/apng,*/*;q=0.8,application/    signed-exchange;v=b3;q=0.9",    
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            "referer": "https://mclub.lenovo.com.cn/sign",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (    KHTML,     like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        
        }

    cook_fir = ast.literal_eval(cook_fir)#字符串转换成字典
    rep = _session.get(url=list_url, headers=header, cookies=cook_fir)
    tt = rep.text
    rep.close()
    num = tt.find("CONFIG.token")
    n1 = num+16
    n2 = n1+40

    token = tt[n1:n2]
    print(token)
    print(len(token))
    #sign_data = {
    #    "_token": token,
    #    "memberSource": "0"
    #}
    
    
    if "立即签到" in tt:
        print("可以签到")
        sign(token)
    else:
        if "签到成功" in tt:
            print("已经签到")
        else:
            print("未登录,尝试重新登录")
            return "1"
            

######登录并记录COOKIES######
def record_cook():
    cook_w = login()
    with open('cookies.txt', 'w') as f:
        f.write(str(cook_w))
        print("Cookies写入文件")
    main()

##############主函数#########
def main():
    myfile = Path("cookies.txt")
    if myfile.is_file():
        cook_r = read_cook()
        print("加载签到页面...")
        if sign_list(cook_fir=cook_r) == "1":
            record_cook()
            print("cookies过期,尝试更新")
            
    else:
        record_cook()

if __name__ == '__main__':
    main()
