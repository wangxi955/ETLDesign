import csv
import os.path

import pandas as pd
from pyecharts.globals import ThemeType
from numpy import around
from pyecharts import options as opts
from pyecharts.charts import Map

class Datadeal():
    def __init__(self):
        self.info = self.getdata()
    def getdata(self):
        with open('data/51job.csv', mode='r', encoding='utf8') as file:
            reader = csv.reader(file)
            return list(reader)

    def show(self):
        for info in self.info:
            print(info[2])

    def filtrate(self):
        infos = []
        for elem in self.info:
            if len(elem[10]) <= 4:
                continue
            f = True
            for i in range(len(elem)):
                if(elem[i]==''):
                    f = False
                    break
            if f:
                if '数据' in elem[0]:
                    infos.append(elem)
                elif '大数据' in elem[10]:
                    infos.append(elem)
        self.info = infos
        self.sava('Demo',self.info)

    def salclean(self):
        self.filtrate()
        for i in range(len(self.info)):
            # 薪资 万/月
            text = self.info[i][2]
            if '万/月' in text or '万以上/月' in text or '万以下/月' in text:
                if '-' in text:
                    x = text.split('万')
                    salaryavr = (float(x[0].split('-')[0])+float(x[0].split('-')[1]))/2*10
                    salaryavr = around(salaryavr,1)
                    self.info[i][2] = str(salaryavr) + '千/月'
                else:
                    x = float(text.split('万')[0])*10
                    self.info[i][2] = str(x) + '千/月'
            elif '万/年' in text or '万以上/年' in text or '万以下/年' in text:
                if '-' in text:
                    x = text.split('万')
                    salaryavr = (float(x[0].split('-')[0])+float(x[0].split('-')[1]))/24*10
                    salaryavr = around(salaryavr,1)
                    self.info[i][2] = str(salaryavr) + '千/月'
                else:
                    x = float(text.split('万')[0])/12*10
                    self.info[i][2] = str(x) + '千/月'
            elif '千/月' in text or '千以上/月' in text or '千以下/月' in text:
                if '-' in text:
                    x = text.split('千')
                    salaryavr = (float(x[0].split('-')[0]) + float(x[0].split('-')[1]))/2
                    salaryavr = around(salaryavr,1)
                    self.info[i][2] = str(salaryavr) + '千/月'
                else:
                    x = float(text.split('千')[0])
                    self.info[i][2] = str(x) + '千/月'
            elif '元/天' in text or '元以上/天' in text or '元以下/天' in text:
                if '-' in text:
                    x = text.split('元')
                    salaryavr = (float(x[0].split('-')[0]) + float(x[0].split('-')[1]))/2*30/1000
                    salaryavr = around(salaryavr,1)
                    self.info[i][2] = str(salaryavr) + '千/月'

                else:
                    x = float(text.split('元')[0])*30/1000
                    self.info[i][2] = str(x) + '千/月'
        self.sava('Demo',self.info)

    # save data
    def sava(self,csvname,content):
        path = os.path.join(os.getcwd(), 'data')
        with open(f'{path}/{csvname}.csv', mode='w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            for rec in content:
                writer.writerow(rec)

if __name__ == '__main__':
    x = Datadeal()
    x.filtrate()
    x.salclean()