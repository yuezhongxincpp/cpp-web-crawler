import requests
import csv
import json


import csv

def save(list):
    with open('首页信息', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list)

def get_html(url):
    headers  ={'Accept':'application/json',
               'Host':'person.sac.net.cn',
               'Origin':'http://person.sac.net.cn',
               'Referer':'http://person.sac.net.cn/pages/registration/sac-publicity-report.html',
                'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'

               }
    data ={
        'filter_EQS_OTC_ID':'10',
        'ORDERNAME': 'AOI#AOI_NAME',
        'ORDER': 'ASC',
        'sqlkey': 'registration',
        'sqlval': 'SELECT_LINE_PERSON'
    }
    r = requests.post(url,headers=headers,data=data)
    data = []
    for i in json.loads(r.text):
        slist = []
        slist.append(i['AOI_NAME'])
        slist.append(i['AOI_ID'])
        slist.append(i['PR_COUNT_PERSON'])
        slist.append(i['PTI0PERSON'])
        slist.append(i['PTI1PERSON'])
        slist.append(i['PTI2PERSON'])
        slist.append(i['PTI3PERSON'])
        slist.append(i['PTI4PERSON'])
        slist.append(i['PTI5PERSON'])
        slist.append(i['PTI6PERSON'])
        slist.append(i['PTI7PERSON'])
        data.append(slist)
    save(data)

url ='http://person.sac.net.cn/pages/registration/train-line-register!orderSearch.action'
with open('首页信息', 'w', newline='') as csvfile:
    title = ['机构名称','id','从业人员数','一般证券业务','证券投资咨询业务(其他)','证券经纪业务营销','证券经纪人','证券投资咨询业务(分析师)'
     '证券投资咨询业务(投资顾问','保荐代表人','投资主办人'
             ]
    writer = csv.writer(csvfile)
    writer.writerow(title)
get_html(url)