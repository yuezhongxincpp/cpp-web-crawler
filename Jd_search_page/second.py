# encoding: gbk

from dict_url_name import infor_dict
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    print url
    slist = []
    #print requests.get(url)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # 获取次分类下有多少页商品


    try:
        num = soup.find('span',attrs = {'class':'p-skip'}).find('b').get_text()
        page_num =int(num)+1
        #print page_num

        #获取分类名
        name = soup.find('a',attrs = {'class':'crumbs-link'}).get_text()

        for i in soup.find_all('span',attrs = {'class':'curr'}):
            name = name + ',' + i.get_text()
        slist.append(name.encode('gbk','ignore'))
        slist.append(url)
        slist.append(page_num)
        mlist.append(slist)
        print name
        print len(mlist)
    except:
        print url

if __name__ == '__main__':
    print len(infor_dict)
    mlist = []
    for i in infor_dict.values():
        get_html(i)


    '''
    classfication 为商品分类记录了属于哪一种哪一类 例如(食品饮料,进口商品,饼干蛋糕)
    init_url 为该类别下搜索页url,用于下一步继续构造url进入具体商品
    '''
    with open('url.csv', 'wb') as f:

        title = ['classification','init_url','page_num']
        writer = csv.writer(f)
        writer.writerow(title)
        writer.writerows(mlist)










