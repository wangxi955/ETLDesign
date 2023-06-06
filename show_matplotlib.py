import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from pyecharts.charts import Pie
from pyecharts import options as opts


with open('data/Demo.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    info = list(reader)

def get_data():
    #获取数据并转化为自定义列名的DataFrame
    columns_name = ['job_name', 'company_name', 'providesalary_text', 'workarea_text', 'companytype_text', 'experience_text',
                           'education_text', 'recruit_people_text', 'companysize_text', 'companyind_text', 'job_detail']
    with open('data/Demo.csv', mode='r', encoding='utf8') as file:
        reader = csv.reader(file)
        reader = list(reader)
    data = pd.DataFrame(data=reader, columns=columns_name)
    return data


# 使用算法分隔比较小的数据
def divide_ser(ser):
    # 获取Series的长度和索引
    length = len(ser.values)
    indexs = [str(x) for x in ser.index]
    # 合并成元组存入列表
    for i, j in zip(range(0, length, 2), range(length -1, 0, -2)):
        if j <= i:
            break
        ser.iloc[i], ser.iloc[j] = ser.iloc[j], ser.iloc[i]
        indexs[i], indexs[j] = indexs[j], indexs[i]
        ser = pd.Series(ser.values, index=indexs)
    return ser


def show_edu(data):
    # 统计不同学历要求的个数并提取其标签
    b = pd.DataFrame(data['education_text'].value_counts())
    labels = b.index
    b = b['education_text']
    # 提取数据
    x = b.values.tolist()
    # 将数据转换为所占总数百分比
    sum_x = sum(x)
    # print(sum_x)
    for i in range(len(x)):
        x[i] = x[i]/sum_x
    plt.axes(aspect='equal')
    ser1 = pd.Series(x, labels)
    ser1 = divide_ser(ser1)
    print(ser1)
    # 解决乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = [20, 6.5]
    patches, l_text, p_text = plt.pie(x=ser1.values, labels=ser1.index, autopct='%1.1f%%', pctdistance=0.9, radius=1.2)
    for t in p_text:
        t.set_size(6)

    for t in l_text:
        t.set_size(7)
    plt.legend(loc='best', bbox_to_anchor=(1, 1))
    plt.show()

def education_show():
    x = []
    for i in info:
        x.append(i[6])

    df = pd.DataFrame(data=x,columns=['education_text'])
    df = df['education_text'].value_counts()
    # print(df)
    # print(x)
    data = [(i,int(j)) for i,j in zip(df.index.values, list(df.values))]
    c = (
        Pie()
            .add(
            series_name='详情',
            data_pair=data,
            rosetype='radius',
            radius=["35%", "60%"],
            center=['50%', '50%'],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-学历要求展示"))
        .render("html/pie_education.html")
    )


def show_exp(data):
    # 统计不同经验要求的个数并提取其标签
    b = pd.DataFrame(data['experience_text'].value_counts())
    labels = b.index
    b = b['experience_text']
    x = b.values.tolist()
    # 将数据转换为所占总数百分比
    sum_x = sum(x)
    for i in range(len(x)):
        x[i] = x[i]/sum_x

    plt.axes(aspect='equal')
    ser2 = pd.Series(x, labels)
    print(ser2)
    ser2 = divide_ser(ser2)

    # 解决乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # plt.figure(figsize=(8, 6))
    plt.rcParams['figure.figsize'] = [20, 15]
    patches, l_text, p_text = plt.pie(x=ser2.values, labels=ser2.index, autopct='%1.1f%%', pctdistance=0.9, radius=1.2)
    for t in p_text:
        t.set_size(9)

    for t in l_text:
        t.set_size(9)
    plt.legend(loc='best', bbox_to_anchor=(1, 1))
    plt.show()

def experience_show():
    x = []
    for i in info:
        x.append(i[5])
    df = pd.DataFrame(data=x,columns=['experience_text'])
    df = df['experience_text'].value_counts()
    data = [(i,int(j)) for i,j in zip(df.index.values, list(df.values))]
    c = (
        Pie()
            .add(
            series_name='详情',
            data_pair=data,
            rosetype='radius',
            radius=["35%", "60%"],
            center=['50%', '50%'],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-工作经验要求展示"))
        .render("html/pie_experience.html")
    )

def show_salary(data):
    b = pd.DataFrame(data['providesalary_text'])
    # 统计个数
    b = b['providesalary_text']

    c = []
    for i in b:
        i = re.findall(r"\d+\.?\d*", i)
        i = ''.join(i)
        i = float(i)
        if i != 400.0:
            c.append(i)

    # 对数据进行切片,并展示
    # 设置横纵坐标的刻度
    y_values = list(range(0, 3000, 100))
    x_values = list(range(2, 70, 2))
    bins = np.linspace(min(c), max(c), 50)
    plt.xticks(x_values)
    plt.yticks(y_values)
    plt.hist(c, bins,range=[0,62])
    plt.rcParams['figure.figsize'] = [8, 8]
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.ylabel("频数")
    plt.xlabel("薪资(千/月)")
    plt.show()


if __name__ == '__main__':
    data = get_data()
    show_edu(data)
    education_show()
    show_exp(data)
    experience_show()
    show_salary(data)
