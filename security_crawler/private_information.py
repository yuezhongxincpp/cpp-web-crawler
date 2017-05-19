#encoding=gbk
from multiprocessing.dummy import Pool
import requests
import json
import csv
import os
import random


class Info(object):

    def __init__(self,name,rows):
        self.name = name
        self.rows = rows



    def get_info(self,id):
        USER_AGENT_LIST = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',

            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',

        ]
        cookies = ['_trs_uv=jybt_373_j1euzxg1; BIGipServerperson=1934665920.20480.0000; JSESSIONID=VvGpZBJFy5xBP0hvNJPX4NQTGwkgJND1yGxTjPJtkCb1RXhQsBVJ!-895601900',
                   '_trs_uv=jybt_373_j1euzxg1; BIGipServerperson=1934665920.20480.0000; JSESSIONID=VvGpZBJFy5xBP0hvNJPX4NQTGwkgJND1yGxTjPJtkCb1RXhQsBVJ!-895601900',
                   '_trs_uv=jybt_373_j1euzxg1; JSESSIONID=c8nGZB5LJpgkQQjM1GM7vh3v1XK1XfbRyrvNl2y0GPB9h4qlhzT3!-895601900; BIGipServerperson=1934665920.20480.0000']
        print(id,'start')
        id =id[2]
        url = 'http://person.sac.net.cn/pages/registration/train-line-register!search.action'
        headers = {
            'Connection':'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': random.choice(cookies),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': '.sac.net.cn',
            'Origin': 'http://person.sac.net.cn',
            'User-Agent': random.choice(USER_AGENT_LIST),
            'X-Requested-With': 'XMLHttpRequest'
        }
        data1 = {
            'sqlkey': 'registration',
            'sqlval':'SELECT_PERSON_INFO',
            'filter_EQS_RPI_ID':str(id)
        }
        data2={
            'sqlkey': 'registration',
            'sqlval': 'SEARCH_LIST_BY_PERSON',
            'filter_EQS_RH#RPI_ID':str(id)

        }
        data = []
        s =requests.session()
        r1 = s.post(url,headers =headers,data=data1,timeout=10)
        print(r1)
        json1 = r1.text
        str1_standard1 = json1.replace('(', '[').replace(')', ']').replace('\'', '"')

        str1_json = json.loads(str1_standard1)[0]
        print(str1_json)
        try:
            img_url = 'http://photo.sac.net.cn/sacmp/images/'+str1_json['RPI_PHOTO_PATH']
            name = str1_json['RPI_NAME']
            sex = str1_json['SCO_NAME']
            eco=str1_json['ECO_NAME']
            company = str1_json['AOI_NAME']
            cer = str1_json['CER_NUM']
            start = str1_json['OBTAIN_DATE']
            end = str1_json['ARRIVE_DATE']
            work =str1_json['PTI_NAME']
            data.append(name)
            data.append(id)
            data.append(sex)
            data.append(company)
            data.append(cer)
            data.append(work)
            data.append(eco)
            data.append(start)
            data.append(end)
            data.append(img_url)
        except:
            pass


        try:
            r2 = s.post(url,headers =headers,data=data2,timeout=10)
            print(r2)
            json2 = r2.text
            str1_standard2 = json2.replace('(', '[').replace(')', ']').replace('\'', '"')
            str1_json2 = json.loads(str1_standard2)
            for i in str1_json2:
                data.append(i['CER_NUM'])
                data.append(i['OBTAIN_DATE'])
                data.append(i['AOI_NAME'])
                data.append(i['PTI_NAME'])
                data.append(i['CERTC_NAME'])

            self.write(data)
            print('保存成功',name,company)
        except:
            pass


    def create(self):
        with open(self.name+'_员工信息', 'w', newline='') as csvfile:
            title = ['姓名','性别','执业机构','证书编号','执业岗位','学历','证书取得日期','证书有效截止日期','照片','证书编号1','取得日期1','执业机构1','执业岗位1','证书状态1','证书编号2','取得日期2','执业机构2','执业岗位2','证书状态2','证书编号3','取得日期3','执业机构3','执业岗位3','证书状态3','证书编号4','取得日期4','执业机构4','执业岗位4','证书状态4','证书编号5','取得日期5','执业机构5','执业岗位5','证书状态5','证书编号6','取得日期6','执业机构6','执业岗位6','证书状态6','证书编号7','取得日期7','执业机构7','执业岗位7','证书状态7','证书编号8','取得日期8','执业机构8','执业岗位8','证书状态8'
                     ]
            writer = csv.writer(csvfile)
            writer.writerow(title)

    def write(self,info):
        with open(self.name+'_员工信息', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info)

    def rewrite(self,info):
        with open(self.name+'re', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(info)


    def run(self):
        #self.create()

        for i in range(0,len(self.rows),10):
            try:
                b = self.rows[i:i+10]
                p = Pool()
                p.map(self.get_info,b)
                p.close()
                p.join()

            except:
                pass




os.chdir('E:/Python3_code/证券人员')
for i in os.listdir():
    print(i)
    os.chdir('E:/Python3_code/证券人员/'+str(i))
    with open(str(i)+ '_url', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    c =Info(str(i),rows)
    c.run()