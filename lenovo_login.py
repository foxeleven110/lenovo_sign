#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cookielib
from pathlib import Path
import ast
from lib import sendmsg
#初始化 
_session = requests.session()
_session.cookies = cookielib.LWPCookieJar()
####读取文件路的Cookies#######
def read_cook():
    print("读取存放文件中的COOKIES")
    with open('cookies.txt', 'r') as f:
        cook_r = str(f.read())
    return cook_r

############登录加载############


def login():
    login_url = "https://reg.lenovo.com.cn/auth/v2/doLogin"
    header = {
        "Host": "reg.lenovo.com.cn",
        "origin": "https://reg.lenovo.com.cn",
        "Connection": "keep-alive",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "referer": "https://reg.lenovo.com.cn/auth/v1/login",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        'Cookie': 'leid=自己的ID;  qrtoken=自己的token',
    }
    
    post_data = {
    	"account": '自己的用户名',
    	"password": '自己的用户密码',
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
####显示签到结果####
def msg(header, tt):

    _day = tt.find("continuity_day")
    _da1 = _day+18
    _da2 = _da1+3
    msg_days = tt[_da1:_da2]
    if '"'  in msg_days:
        _da2 = _da1+2
        msg_days = tt[_da1:_da2]
    ######以上加载签到连续天数#######

    repon = _session.get(url="https://mclub.lenovo.com.cn/signuserinfo", headers=header)
    value = {
        "ledou": repon.json()["ledou"],
        "coin": repon.json()["userCoins"],
        "days": msg_days
    } 
    repon.close()
    title = "联想延保签到结果"
    content = '''    你已经连续签到%(days)s天
    当前你的乐豆 %(ledou)s 
    当前你的积分 %(coin)s
    
    ¯¯¯¯¯¯¯¯¯^-^¯¯¯¯¯¯¯¯¯
    ''' 
    
    content = (content % value)
    print(content)
    #sendmsg.pushplus(title, content)
###************####
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
    #print("token:",token)
    
    if "立即签到" in tt:
        print("可以签到")
        sign(token)
    else:
        if "签到成功" in tt:
            print("  你的签到结果为:")
            msg(header,tt)
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
