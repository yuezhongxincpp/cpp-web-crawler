# encoding=gbk

import requests
import sys
import json
import re
from gevent import monkey;monkey.patch_all()
import gevent
import time
import csv
'''
爬取天猫商品信息(评论数量,评论内容)
坑
'''
reload(sys)
sys.setdefaultencoding('gbk')

urls = [('https://rate.tmall.com/list_detail_rate.htm?itemId=45801773272&sellerId=725677994&order=3&append=0&content=0&currentPage=1&pageSize=10&tagId=&_ksTS=1488522497840_605&callback=jsonp606','jsonp606','https://rate.tmall.com/list_detail_rate.htm?itemId=45801773272&sellerId=725677994&order=3&append=0&content=0&pageSize=10&tagId=&_ksTS=1488522497840_605&callback=jsonp606'),
        ('https://rate.tmall.com/list_detail_rate.htm?itemId=43752160447&sellerId=880734502&order=3&append=0&content=0&currentPage=1&pageSize=10&tagId=&_ksTS=1488522569438_568&callback=jsonp569','jsonp569','https://rate.tmall.com/list_detail_rate.htm?itemId=43752160447&sellerId=880734502&order=3&append=0&content=0&pageSize=10&tagId=&_ksTS=1488522569438_568&callback=jsonp569'),
        'https://rate.tmall.com/list_detail_rate.htm?itemId=523754304759&sellerId=619123122&order=3&append=0&content=0&currentPage=4&pageSize=10&tagId=&_ksTS=1488522623938_581&callback=jsonp582',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=545450886204&sellerId=880734502&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522655284_575&callback=jsonp576',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=537521647734&sellerId=268451883&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522690465_1089&callback=jsonp1090',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=541258955986&sellerId=268451883&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522714446_692&callback=jsonp693',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=541212432230&sellerId=1714128138&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522836375_635&callback=jsonp636',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=37896295920&sellerId=1850245428&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522890613_547&callback=jsonp548',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=42951581774&sellerId=2065716479&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522914962_585&callback=jsonp586',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=540733153590&sellerId=3018281978&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522934405_554&callback=jsonp555',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=40661379492&sellerId=832978172&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522971305_473&callback=jsonp474',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=41551002662&sellerId=1049653664&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488522994004_461&callback=jsonp462',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=541131228599&sellerId=2793620632&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488523011569_462&callback=jsonp463',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=37318466016&sellerId=859515618&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488523029737_505&callback=jsonp506',
        'https://rate.tmall.com/list_detail_rate.htm?itemId=545280760107&sellerId=919474917&order=3&append=0&content=0&currentPage=2&pageSize=10&tagId=&_ksTS=1488523057016_530&callback=jsonp531'
]


def get_comment(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'
        ,
        'cookie': '_m_h5_tk=8c49907b9571742e8a3c5479bdd57c3d_1488535672745; _m_h5_tk_enc=f0c7c74a67965c6855170f172cc1d4c7; _m_user_unitinfo_=center; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uss=WvNIxfKKaIWVjPxI06QZjUrGepxof9ipInQL5jTpZh9mZl7BeCjAdJsvcM8%3D; _tb_token_=5eb6765637779; uc3=sg2=WqagDzc4OOZ%2F%2BPA9zWxDuEJyHyPUUAZejIvGPT%2FGp7s%3D&nk2=Csjn%2FgQ8LDLFRpz3Vattng%3D%3D&id2=UUGgpDpyGYriiQ%3D%3D&vt3=F8dARVacW12vJQgbYgI%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; lgc=interesting%5Cu5CB3666; tracknick=interesting%5Cu5CB3666; cookie2=1823e5b240cddd5fd537d9ba9ee2950b; sg=670; cookie1=B0T5agd9hSiL68Hk5c8%2Bvlb6cndkixX7PuRUP2de0NU%3D; unb=2929832227; t=c11f02491016f945f0b34df54e1f1135; _l_g_=Ug%3D%3D; _nk_=interesting%5Cu5CB3666; cookie17=UUGgpDpyGYriiQ%3D%3D; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=VT5L2FSpccDI&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoW%2FVUCaNnQkrw%3D%3D&tag=7&lng=zh_CN; login=true; cna=fWkwEWb8XAcCAS1Mzdb5HzDa; sm4=350200; JSESSIONID=46A141035658447CC017188BDD2804E4; isg=Ar29SzfOuWVROB0ZlDY6UQ4pzBkMaB6BIYQ_eH8D7pRVtt3oRqoBfItoFl0K; l=At3d7BNZ37szGb9aZapR3ekAbbPW7RFa'
    }
    r = requests.get(url[0],headers=header)
    infor = json.loads(re.findall(r'jsonp606\((.*?)\)',r.text.strip())[0])
    pagenum = infor['rateDetail']['paginator']['lastPage']
    totalcount = infor['rateDetail']['rateCount']['total']
    urls = []
    for i in xrange(1,pagenum+1):
        urls.append(url[2]+'&currentPage='+str(i))
    print urls
    print totalcount
    return urls,totalcount

def save(list):
    with open('comment.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(list)
def parse_json(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'
        ,'cookie':'_m_h5_tk=8c49907b9571742e8a3c5479bdd57c3d_1488535672745; _m_h5_tk_enc=f0c7c74a67965c6855170f172cc1d4c7; _m_user_unitinfo_=center; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uss=WvNIxfKKaIWVjPxI06QZjUrGepxof9ipInQL5jTpZh9mZl7BeCjAdJsvcM8%3D; _tb_token_=5eb6765637779; uc3=sg2=WqagDzc4OOZ%2F%2BPA9zWxDuEJyHyPUUAZejIvGPT%2FGp7s%3D&nk2=Csjn%2FgQ8LDLFRpz3Vattng%3D%3D&id2=UUGgpDpyGYriiQ%3D%3D&vt3=F8dARVacW12vJQgbYgI%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; lgc=interesting%5Cu5CB3666; tracknick=interesting%5Cu5CB3666; cookie2=1823e5b240cddd5fd537d9ba9ee2950b; sg=670; cookie1=B0T5agd9hSiL68Hk5c8%2Bvlb6cndkixX7PuRUP2de0NU%3D; unb=2929832227; t=c11f02491016f945f0b34df54e1f1135; _l_g_=Ug%3D%3D; _nk_=interesting%5Cu5CB3666; cookie17=UUGgpDpyGYriiQ%3D%3D; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=VT5L2FSpccDI&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoW%2FVUCaNnQkrw%3D%3D&tag=7&lng=zh_CN; login=true; cna=fWkwEWb8XAcCAS1Mzdb5HzDa; sm4=350200; JSESSIONID=46A141035658447CC017188BDD2804E4; isg=Ar29SzfOuWVROB0ZlDY6UQ4pzBkMaB6BIYQ_eH8D7pRVtt3oRqoBfItoFl0K; l=At3d7BNZ37szGb9aZapR3ekAbbPW7RFa'
    }
    time.sleep(0.5)
    r = requests.get(url, headers=header)
    try:
        json_infor = json.loads(re.findall(r'jsonp606\((.*?)\)',r.text.strip())[0])
        commentlist= json_infor['rateDetail']['rateList']


        comment = []
        for i in commentlist:
            slist = []
            times = i['rateDate']
            content = i['rateContent']
            slist.append(times)
            slist.append(content)
            comment.append(slist)
        save(comment)

    except:
        pass






urls,totalcount = get_comment(urls[0])
with open('comment.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'content'])
jobs = [gevent.spawn(parse_json, url) for url in urls]
gevent.joinall(jobs)
