# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import random
import json
import csv
import re


class Jd_scraper(object):
    def __init__(self,url,sort):
        #1为销量排序，0为综合排序
        self.sort_dict ={0:'',1:'1'}
        self.sort = sort

        self.url = url
        self.search_list_url = 'https://so.m.jd.com/ware/searchList.action'

        self.categoryId = re.findall(r'-(\d+).html',url)[0]
        self.c1 = url.split('-')[0].split('/')[-1]
        self.c2 = url.split('-')[-2]

        #self.page_num =self.get_page_num()
        #文件名为url里的参数和爬取时间
        self.date = '%s-%s-%s'%time.localtime(time.time())[0:3]
        self.time = '%s-%s-%s'%time.localtime(time.time())[3:6]

        self.save_name = 'jd_'+self.date+'_'+self.time+'_'+self.c1+'_'+self.c2+'_'+self.categoryId+'_'+str(self.sort)

    def get_comment_info(self,id):
        url ='http://club.jd.com/comment/productCommentSummaries.action?'
        headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
                   'Host':'club.jd.com',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        payload = {'referenceIds':id}
        try:
            r = requests.get(url,headers =headers,params = payload)
            json_info = json.loads(r.text)['CommentsCount'][0]
            return json_info
        except:
            return None





    def get_html(self,page_num=1):
        #sort1表示按销量顺序
        data={'_format_':'json',
              'categoryId': self.categoryId,
              'c1': self.c1,
              'c2': self.c2,
              'sort': self.sort_dict[self.sort],
              'page':str(page_num)}
        headers = {'authority':'so.m.jd.com',
        'method':'POST',
        'path':'/ware/searchList.action',
        'scheme':'https',
        'accept':'application/json',
        'referer':self.url,
        'user-agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
        'x-requested-with':'XMLHttpRequest'}
        time.sleep(random.randint(1,3))
        r = requests.post(self.search_list_url,headers=headers,data=data)
        if r.status_code == 200:
            print('Success to get html')
            return r.text
        else:
            print('Fail to get html')
            return None

    #获取总面数
    def get_page_num(self):
        html = self.get_html()
        try:
            pagenum = int(json.loads((json.loads(html)['value']))['wareList']['wareCount'])//10
            print('Success to get page_num:',pagenum)
            return pagenum

        except KeyError:
            print('Fail to get page_num')
            return None

    def parse(self,pagenum):
        r = self.get_html(page_num=pagenum)
        ware_list = json.loads((json.loads(r)['value']))['wareList']['wareList']
        wholeinfo =[]
        for index,i in enumerate(ware_list):
            info=[]
            #表示在第几页第几个 如1-2表示第一页第二个

            info.append(i['wname'])
            info.append(i['wareId'])
            info.append(i['jdPrice'])
            info.append(i['totalCount'])
            comment_info = self.get_comment_info(i['wareId'])
            info.append(comment_info['AverageScore'])
            info.append(comment_info['GoodRate'])
            info.append(comment_info['GeneralRate'])
            info.append(comment_info['PoorRate'])
            info.append(self.date)
            info.append(self.time)
            info.append(str(pagenum) + '-' + str(index + 1))
            info.append(self.categoryId)
            info.append(self.sort)
            #print(info)

            wholeinfo.append(info)
        self.save_csv(wholeinfo)

    def create_csv(self):
        titles=['goodsName','ID','price','commentsNum','averageScore','goodrate','generalRate','poorRate','date','time','page','cate','sort']
        with open(self.save_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(titles)


    def save_csv(self,infolist):
        with open(self.save_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(infolist)

    def run(self):
        self.create_csv()
        jobs=[]
        for i in range(10):
            self.parse(i+1)
            #jobs.append(gevent.spawn(self.parse,i+1))
        #gevent.joinall(jobs)


#！！！！！！！修改这里的url即可改变抓取的物品！！！！！！！
url='https://so.m.jd.com/products/1318-12099-9755.html'


#综合排序
c =Jd_scraper(url,0)
c.run()

#销量排序
m =Jd_scraper(url,1)
m.run()
