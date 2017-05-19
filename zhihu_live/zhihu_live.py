# encoding=gbk

'''

爬取知乎live信息.输入ongoing 输出将要ongoing live信息  输入ended 输出ended live信息

'''

import requests
import json
import csv
import time

#获取json格式的数据
def get_json(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': '_zap=c977c6e1-accc-4edb-b6b6-fdeb9169df3e; q_c1=e9bdad46b81d4eb1b75e37e51b72997c|1486553772000|1486553772000; l_cap_id="NzRkYmI4ZGZmOTBhNDQ2ZGI3NTU3ZDVlMWY0N2M3YmM=|1486557572|c1e232a6a87c88ee5d164fd1f76ff6b0205c60e1"; cap_id="MThiM2Y4NmU2NzNjNGI1NTg0MzQxMDg2ZTFjYTBiMjQ=|1486557572|eb8949a46003b6f43b5081c696c50091576a15a0"; d_c0="AFBCMceCRwuPTsHi1Sx7AFAgdSygQu2D5cQ=|1486557573"; _zap=16bfe232-7b4c-48a1-89bb-c6f071ae2af7; login="YmRjOWQwZGY1Mzc1NGNmY2JmNWM2YjY5M2JlMTM0OTc=|1486557600|6fb4ed7ef73946ffdc9b614b8778e0636be7b3af"; aliyungf_tc=AQAAABdHuVjdzg4AAaU5OzbVk8BzXZf/; z_c0=Mi4wQUhBQTFkWWt2QW9BVUVJeHg0SkhDeGNBQUFCaEFsVk50NTdDV0FDelg0XzlPQ0JPQUtsZWJiSktycFptZVBrS2NR|1486826798|d70f9fe4161dee6852b3e2d9b8599f0ab7560bd1; nweb_qa=heifetz; __utma=155987696.1166272402.1486826797.1486826797.1486826797.1; __utmb=155987696.0.10.1486826797; __utmc=155987696; __utmz=155987696.1486826797.1.1.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=%E7%9F%A5%E4%B9%8Elive'
    }
    return json.loads(requests.get(url,headers = header).content)

#获取url的list
def get_urls():
    #第一个接口
    zimu = raw_input('entre: [ongoing] view ongoing live ; enter : [ended] view history live]====Please enter: ')
    url = 'https://api.zhihu.com/lives/'+str(zimu)
    json = get_json(url)
    #创建一个空list
    init_list =[]
    init_list.append(url)

    is_end = json['paging']['is_end']  #是否到了下一页,有下一页为false

    while not is_end:
        href = json['paging']['next']  # 下一页的链接


        init_list.append(href)
        is_end = get_json(href)['paging']['is_end']
        json = get_json(href)
    return init_list,zimu

#utc时间转化
def get_time(timestamp):
    timearray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timearray)

#解析json格式数据获取信息
def get_infor(url):
    data = get_json(url)['data']
    mlist = []
    for li in data:
        list=[]

        speaker_name = li['speaker']['member']['name']



        introduct = li['description']

        live_name = li['subject']

        time = get_time(li['starts_at'])

        join= str(li['seats']['taken'])

        fee = str(li['fee']['amount']/100)+ li['fee']['unit']

        href = 'https://www.zhihu.com/lives/'+li['id']

        selfurl= 'https://www.zhihu.com/people/'+li['speaker']['member']['url_token']

        try:
            score = str(li['feedback_score'])
        except:
            score = 'No score now'

        try:
            like_num = str(li['liked_num'])
        except:
            like_num = 'No like_num now'

        try:
            answer_count = str(li['speaker_message_count'])
        except:
            answer_count = 'No answer_account now'


#==============selfurl 用于爬取个人信息=======


        list.append(live_name.encode('gbk','ignore'))
        list.append(speaker_name.encode('gbk','ignore'))
        list.append(href.encode('gbk','ignore'))
        list.append(time.encode('gbk','ignore'))
        list.append(join.encode('gbk','ignore'))
        list.append(introduct.encode('gbk','ignore'))
        list.append(fee.encode('gbk','ignore'))
        list.append(selfurl.encode('gbk','ignore'))
        list.append(score.encode('gbk','ignore'))
        list.append(like_num.encode('gbk','ignore'))
        list .append(answer_count.encode('gbk','ignore'))
        mlist.append(list)


    return mlist


def save_infor(file_name,list,title):
    csvfile = open(file_name, 'w')
    writer = csv.writer(csvfile)
    writer.writerow(title)
    writer.writerows(list)
    csvfile.close()


def main():
    #status_id用于辨别文件
    urls,status_id = get_urls()
    infor_list = []
    for url in urls:

        infor_list.extend(get_infor(url))

    #在title中输入储存数据的标题
    title = ['live名称', '主讲者','链接','开始时间','参加人数','介绍','费用','个人主页链接','live评分','喜欢数','回答数','爬取时间 : '+str(get_time(time.time()))]

    save_infor('live_'+str(status_id)+'.csv',infor_list, title)



#运行主函数
if __name__ == '__main__':
    ts = ts = time.time()
    main()
    print 'use time:', time.time() - ts
