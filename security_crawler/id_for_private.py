#encoding=utf-8
from multiprocessing.dummy import Pool
import requests
import json
import csv
import os



class Zhenguan(object):

    def __init__(self,name,id):
        self.name = name
        self.id = id

    def create_csv(self):
        with open(self.name, 'w', newline='') as csvfile:
            title = ['RPI_NAME','idnum']
            writer = csv.writer(csvfile)
            writer.writerow(title)

    def write(self,info):
        with open(self.name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(info)

    def get_html(self):

        url = 'http://person.sac.net.cn/pages/registration/train-line-register!search.action'

        headers ={
        'Host':'person.sac.net.cn',
        'Origin':'http://person.sac.net.cn',
        'Referer':'http://person.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId='+str(id),
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
        'X-Requested-With':'XMLHttpRequest'
        }
        data = {'filter_LES_ROWNUM':'10000',
        'filter_GTS_RNUM':'0',
        'filter_EQS_PTI_ID':'',
        'filter_EQS_AOI_ID':str(self.id),
        'ORDERNAME':'PP#PTI_ID,PP#PPP_NAME',
        'ORDER':'ASC',
        'sqlkey':'registration',
        'sqlval':'SEARCH_FINISH_PUBLICITY'}

        r = requests.post(url,headers =headers,data=data)
        print(r)

        json_info= json.loads(r.text)
        data = []
        print(len(json_info))
        for i in json_info:
            slist = []
            #编码问题巨坑
            slist.append(i['RPI_NAME'].encode('gbk','ignore').decode('gbk'))
            slist.append(i['PPP_ID'])

            data.append(slist)

        self.create_csv()
        self.write(data)


class Get_url(object):
    def __init__(self,company_name):
        self.company_name = company_name

    def get_urlid(self,id):
        url = 'http://person.sac.net.cn/pages/registration/train-line-register!search.action'
        headers = {
            'Accept':'application/json',
               'Origin':'http://person.sac.net.cn',
               'Referer':'http://person.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk='+str(id),
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'X-Requested-With':'XMLHttpRequest'
 }
        data = {'filter_EQS_PPP_ID':str(id),
            'sqlkey':'registration',
            'sqlval':'SD_A02Leiirkmuexe_b9ID'


    }

        r = requests.post(url,headers = headers,data=data)
        json_info = eval(r.text)[0]
        id = json_info['RPI_ID']
        return id

        #except:
        #    print('fail',id)
         #   return

    def parse(self,i):
        try:

            slist = []
            slist.append(i[0])
            slist.append(i[1])
            slist.append(self.get_urlid(i[1]))
            print(i,'success')
            self.write_csv(slist)
        except:
            slist = []
            slist.append(i[0])
            slist.append(i[1])
            slist.append(None)
            self.write_csv(slist)

    def run(self):
        with open(self.company_name, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader][1:]
            #print(rows)

        p = Pool()
        p.map(self.parse, rows)
        p.close()
        p.join()

    def write_csv(self,list):
        with open(self.company_name+'_url', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list)



with open('E:/Python3_code/证券人员2/首页','r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

#com = ['国联证券股份有限公司', '华泰证券股份有限公司', '国金证券股份有限公司', '国元证券股份有限公司', '海际证券有限责任公司', '国海证券股份有限公司', '海通证券股份有限公司','华安证券股份有限公司','兴证证券资产管理有限公司']
os.chdir('E:/Python3_code/证券人员2')
for i in rows:
    print(i)
    os.chdir('E:/Python3_code/证券人员2')
    os.mkdir(str(i[0]))

    os.chdir('E:/Python3_code/证券人员2/'+str(i[0]))
    a = Zhenguan(i[0],i[1])
    a.get_html()
    c = Get_url(i[0])
    c.run()




