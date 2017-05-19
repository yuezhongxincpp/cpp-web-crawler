# encoding=gbk

import re
import requests
import sys
import json
from bs4 import BeautifulSoup
import csv
from gevent import monkey;monkey.patch_all()
import gevent


'''
爬取天猫商品信息(商品名称,月销量,商品价格)
'''
reload(sys)
sys.setdefaultencoding('gbk')

def get_html(payload):
    header = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'}
    url = 'https://detail.m.tmall.com/item.htm?'
    r = requests.get(url,headers =header,params =payload)
    if r.status_code == 200:
        return r.text,payload['id']
    else:
        print 'Fail to get page'

def save_infor(id,list):
    with open(str(id)+'.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(list)


def parse_json(payload):
    html,id = get_html(payload)
    list = []
    #获取月销量
    reg = r'var _DATA_Mdskip =\s+(.*?)\s</script>'
    imerge = re.compile(reg)
    jsonlist =json.loads(re.findall(imerge, html)[0])
    month_sellCount = jsonlist['defaultModel']['sellCountDO']['sellCount']
    print month_sellCount

    #商品价格
    reg2 = r'"price":"(.*?)",'
    rep =  re.compile(reg2)
    price = re.findall(rep, html)[-1]
    print price

    # 获取商品名称
    soup = BeautifulSoup(html,'html.parser')
    name = soup.head.find('title').get_text().split('-')[0]
    print name
    list.append(name)
    list.append(price)
    list.append(month_sellCount)
    save_infor(id, list)



def main():
    payloads1 = [{'id':'523754304759','skuId':'3240229360012'},
                {'id':'43752160447','skuId':'3407168583618'},
                {'id':'523754304759','skuId':'3240229360012'},
                {'id':'545450886204'},
                {'id':'37896295920','skuId':' 3170036025206'},
                {'id': '42951581774','skuId':'3417032154410'},
                {'id':'540733153590','skuId':'3283974745299'},
                {'id':'40661379492'},
                {'id':'41551002662'},
                {'id':'541131228599'},
                {'id':'37318466016'},
                {'id':'545280760107'}]

    payloads2 = [{'id':'537521647734','skuId':'3281388624581'},
                {'id': '541258955986','skuId': '3443614118592'},
                {'id': '541212432230','skuId': '3250111501759'}]

    #jobs1 = [gevent.spawn(parse_json,payload) for payload in payloads2]
    #gevent.joinall(jobs1)

    jobs2 = [gevent.spawn(parse_json, payload) for payload in payloads1]
    gevent.joinall(jobs2)

if __name__ == '__main__':
    main()