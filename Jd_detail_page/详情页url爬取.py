# encoding: utf-8
import csv
import requests
from bs4 import BeautifulSoup
import sys
import gevent
from gevent import monkey
monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf-8')


# 下面的这个函数可以用于爬出一个分类 单面里的所有详情页url
def get_url(url):
    header ={
    'Referer':'https://www.jd.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

    r = requests.get(url,headers =header,timeout=5).content
    soup = BeautifulSoup(r, 'html.parser')
    items = soup.find_all('li', attrs={'class': 'gl-item'})
    slist = []
    for i in items:
        url = 'http:'+i.find('a', attrs={'target': '_blank'})['href']
        print url
        slist.append(url)
    with open(keys, 'ab+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(slist)







def gouzzao(a, b, c):
    slist = []
    for i in range(1, b):
        slist.append(a + '&page=' + str(i))
    dict[c] = slist

with open('url.csv', 'rb') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]
    dict = {}
    for i in rows[1:]:
        # 读取出csv文件中的信息,此处i为不同种类的商品搜索页
        name = i[0].decode('gbk')
        url = i[1]
        page_num = i[2]
        gouzzao(url, int(page_num), name)


keylist = dict.keys()

for keys in keylist:
    jobs = [gevent.spawn(get_url, url) for url in dict[keys]]
    gevent.joinall(jobs)





