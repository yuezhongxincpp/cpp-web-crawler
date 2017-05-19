# encoding: utf-8
'''
简陋的小工具
获取有效url 其中把解析方式相同 页面 url放在一起
其中带'cat='的为我们首要需要爬取的
'''
import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://www.jd.com/allSort.aspx').content
soup = BeautifulSoup(r, 'lxml')
r = soup.find('div',attrs = {'class':'category-items clearfix'})
r = r.find_all('div',attrs = {'class':'col'})
infor_dict = {}

for i in r:
    li = i.find_all('dd')
    for m in li:
        ssi =  m.find_all('a',attrs = {'target':'_blank'})
        for k in ssi:
            if re.search(r'cat=', k['href']):

                infor_dict[k.get_text()]='http:'+k['href']

result = 'infor_dict = '+str(infor_dict)

with open('dict_url_name.py','w') as f:
    f.write(result)
