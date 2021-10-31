#!/usr/bin/python3
# encoding:utf-8
import requests
import json
def pushplus(title, content):
    token = "9e0588f54a7645f1aade6f627e9b455e"
    url = 'http://www.pushplus.plus/send'
    data = {
        "token":token,
        "title":title,
        "content":content
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)