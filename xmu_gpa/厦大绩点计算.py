# encoding=gbk
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np

def get_html():
    name = raw_input('Enter your username : ')
    pasword = raw_input('Enter your password : ')
    data = {'Login.Token1': name, 'Login.Token2': pasword}

    header = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
       }
    s = requests.Session()
    url = 'http://ssfw.xmu.edu.cn/cmstar/userPasswordValidate.portal'
    r = s.post(url, data=data, headers=header)
    infor_content = s.get('http://ssfw.xmu.edu.cn/cmstar/index.portal?.pn=p1201_p3535').content



    return infor_content


def parse_html(html):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.body

    portletContent = body.find('div',attrs = {'class':'portletContent'})
    table = body.find('table',attrs={'class':'xmu_table_class'})
    tlist = table.find_all('tr')
    mlist = []
    for li in tlist[3:]:
        slist = []
        for i in li.find_all('font'):

            slist.append(i.get_text().encode('gbk','ignore'))

        mlist.append(slist)
    return mlist
def save_infor(list):
    csvfile = file('score.csv', 'wb')
    title= ['课程名称', '学分', '类别', '修读性质', '成绩','特殊原因','维度']
    writer = csv.writer(csvfile)
    writer.writerow(title)
    writer.writerows(list)
    csvfile.close()

def get_score():
    csvfile = file('score.csv', 'rb')
    reader = csv.reader(csvfile)
    count = []

    for line in reader:
        list = []
        score = line[4]
        credit = line[1]
        # 判断是否为数字
        print score
        if score.isalnum():

            list.append(score)
            list.append(credit)
            count.append(list)
        else:
            pass

    score_li = []
    credit_li = []
    print count

    for i in count:


        score = i[0]

        if int(score) < 60:
            score = 0
        if 63 >= int(score) >= 60:
            score = 1.0
        if 67 >= int(score) >= 64:
            score = 1.7
        if 71 >= int(score) >= 68:
            score = 2.0
        if 72 >= int(score) >= 74:
            score = 2.3
        if 77 >= int(score) >= 75:
            score = 2.7
        if 80 >= int(score) >= 78:
            score = 3.0
        if 84 >= int(score) >= 81:
            score = 3.3
        if 89 >= int(score) >= 85:
            score = 3.7
        if int(score) >= 90:
            score = 4.0

        score_li.append(score)
        credit_li.append(float(i[1]))

    a = np.array(score_li)
    b = np.array(credit_li)
    print sum(a * b) / sum(b)
    csvfile.close()


html = get_html()
inlist = parse_html(html)
save_infor(inlist)
get_score()