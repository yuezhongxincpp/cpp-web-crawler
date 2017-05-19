# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from multiprocessing.dummy import Pool
import sqlite3
import time


def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ,
        'Referer': 'http://cn.bing.com/search?q=%E8%B1%86%E7%93%A3%E5%9B%BE%E4%B9%A6250&qs=n&form=QBRE&sp=-1&pq=%E8%B1%86%E7%93%A3%E5%9B%BE%E4%B9%A6250&sc=1-6&sk=&cvid=B55F0187063E418E9494E164500C2C3E'
        }

    r = requests.get(url, headers=header).text

    return r


def parse_html(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    article_list = soup.find('div', attrs={'class': 'article'})

    for i in article_list.find_all('table'):
        list = []
        infor = i.select('td')[1]
        href = infor.find('a')['href']
        name = infor.find('a')['title']

        # 获取作者,译者,价格出版社信息,
        other = infor.find('p').get_text().split('/')

        author = other[0]
        price = other[-1]
        time = other[-2]
        pub = other[-3]
        # 判断是否有翻译人员
        if other[-4] == other[0]:
            trans = 'None'
        else:
            trans = other[-4]

        score = i.find('span', attrs={'class': 'rating_nums'}).get_text()

        comment_num = re.findall(r'\d+', i.find('span', attrs={'class': 'pl'}).get_text())  # 提取评价人数

        list.append(name)
        list.append(author)

        list.append(trans)
        list.append(price)

        list.append(pub)
        list.append(time)
        list.append(score)
        list.append(comment_num[0])
        list.append(href)
        data.append(list)




def get_url():
    url = 'https://book.douban.com/top250'
    soup = BeautifulSoup(get_html(url), 'lxml')
    article = soup.find('div', attrs={'class': 'article'})
    list = article.find('div', attrs={'class': 'paginator'}).find_all('a')
    urls = []
    urls.append(url)
    for i in list:
        href = i['href']
        urls.append(href)
    return urls


if __name__ == '__main__':
    ts = time.time()
    urls = get_url()
    data = []
    cx = sqlite3.connect("test.db")
    cu = cx.cursor()
    cu.execute(
        "create table catalog (name text NULL,author text NULL,trans text NULL,price text NULL,pub text NULL,times text NULL,score text NULL,comment text NULL,href text NULL)")

    p = Pool()
    p.map(parse_html, urls)
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    cx = sqlite3.connect("test.db")
    for  i in data:

        cx.execute("insert into catalog values (?,?,?,?,?,?,?,?,?)", i)
    cx.commit()


    print time.time() - ts