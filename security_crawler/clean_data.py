import os
import csv
os.chdir('E:/Python3_code/done')
a = 0
b=0


for i in os.listdir():

    os.chdir('E:/Python3_code/done/'+str(i))


    with open(str(i) + '_员工信息', 'r',encoding='gbk') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['姓名'],row['执业机构'])
            print(row['照片'])
            a+=1
print(a)














        #print(column)







print(a,b)