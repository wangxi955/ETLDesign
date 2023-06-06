import csv
import re
import jieba
import pandas as pd


from numpy import around
from pyecharts import options as opts
from pyecharts.charts import Map, Map3D, Geo, Pie, Line, WordCloud
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType, SymbolType

with open('data/coordinate.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    coord = list(reader)
with open('data/Demo.csv','r',encoding='utf8') as f:
    reader = csv.reader(f)
    info = list(reader)


city = []
for i in info:
    text = i[3].split('-')[0]
    city.append(text)
df = pd.DataFrame(data=city, columns=['城市'])
df.replace('燕郊开发区','三河',inplace=True)
df.replace('湖南省','长沙',inplace=True)
df.replace('陕西省','西安',inplace=True)
df.replace('广东省','广州',inplace=True)
df.replace('浙江省','杭州',inplace=True)
df.replace('江西省','南昌',inplace=True)
df.replace('湖北省','武汉',inplace=True)
df.replace('四川省','成都',inplace=True)
df.replace('陕西省','西安',inplace=True)
df.replace('云南省','昆明',inplace=True)

x = df['城市'].value_counts()
city = x.index.values

numb = list(x.values)

def map_show():

    data = [[i, int(j)] for i, j in zip(city, numb)]
    map = Geo(init_opts=opts.InitOpts(theme='light',
                                      page_title='Visualization-pyecharts'))

    map.add_coordinate('黔南',107.52,106.63)
    map.add_schema(maptype="china-cities")
    map.add(series_name='岗位分布',data_pair=data)
    map.set_series_opts(label_opts=opts.LabelOpts(is_show=False,color='auto'))
    map.set_global_opts(title_opts=opts.TitleOpts(title="Map-中国市级"),
                        visualmap_opts=opts.VisualMapOpts(max_=817,min_=1))
    map.render('html/map.html')
    # ma = max(numb)
    # print(ma)
def map3D_show():
    with open('data/coordinate.csv','r',encoding='utf8') as f:
        reader = csv.reader(f)
        coord = list(reader)

    for i in city:
        f = True
        for j in coord:
            if(i==j[0]):
                f = False
                break
        if f:
            print(i)
    data = []
    for i in range(len(city)):
        for j in range(len(coord)):
            if city[i]==coord[j][0]:
                x = (city[i],[float(coord[j][1]),float(coord[j][2]),int(numb[i])])
                data.append(x)
    # for i in data:
    #     print(i)
    c = (
        Map3D()
            .add_schema(
            maptype='china',
            # ground_color='#CCCCCC',

            itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
            ),
            post_effect_opts=opts.Map3DPostEffectOpts(
                is_color_correction_enable=True,
            ),
            map3d_label=opts.Map3DLabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + " " + data.value[2];}"),
            ),
            emphasis_label_opts=opts.LabelOpts(
                is_show=False,
                color="#fff",
                font_size=10,
                background_color="rgba(0,23,11,0)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                main_shadow_quality="high",
                is_main_shadow=False,
                main_beta=10,
                ambient_intensity=0.3,
            ),
        )
            .add(
            series_name="岗位分布",
            data_pair=data,
            type_=ChartType.BAR3D,
            bar_size=0.8,
            min_height=3,
            shading="lambert",
            stack=True,
            label_opts=opts.LabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-中国市级"),
                                 visualmap_opts=opts.VisualMapOpts(
                                     is_piecewise=True,
                                     pieces=[
                                         {'min': 800, 'label': '>800', 'color': '#CC0033'},
                                         {'min': 500, 'max': 799, 'label': '500-799', 'color': '#CC6666'},
                                         {'min': 200, 'max': 499, 'label': '200-499', 'color': '#FF6600'},
                                         {'min': 100, 'max': 199, 'label': '100-199', 'color': '#FFFF33'},
                                         {'min': 10, 'max': 99, 'label': '10-99', 'color': '#6699CC'},
                                         {'min': 0, 'max': 9, 'label': '0-9', 'color': '#003399'},
                                     ],
                                 )

            )
            .render("html/map3d_with_bar3d.html")
    )


def quality_show():
    x = []
    for i in info:
        x.append(i[4])
    df = pd.DataFrame(data=x,columns=['资质'])
    df = df['资质'].value_counts()
    data = [(i,int(j)) for i,j in zip(df.index.values, list(df.values))]
    c = (
        Pie()
            .add(
            series_name='详情',
            data_pair=data,
            rosetype='radius',
            radius=["35%", "60%"],

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
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-公司资质对比"))
        .render("html/pie_quality.html")
    )


def edu_with_salary_show():
    x = []
    for i in info:
        salary = float(i[2].split('千')[0])
        x.append([salary,i[6]])

    df = pd.DataFrame(data=x,columns=['salary','edu'])
    groups = df.groupby('edu')
    groups = around(groups['salary'].mean(),2)
    groups = groups.sort_values()
    salary = list(groups.values)
    edu = list(groups.index.values)
    c = (
        Line()
            .add_xaxis(edu)
            .add_yaxis(
            "月薪(千)",
            salary,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-学历与薪资关系"))
            .render("html/line_markline.html")
    )


def clound_show():
    stop = open('data/stopwords.txt',encoding='utf8').read()
    eng_data =  []
    cn_data = []
    jieba.load_userdict('data/bigdata.txt')

    for i in info:
        spec_words = re.findall('[-.*:a-zA-Z0-9]+', i[10])
        for x in spec_words:
            if re.search(r'\d', x):
                continue
            if len(x) <=20:
                if x not in stop:
                    eng_data.append(x)

        new_data = re.findall('[\u4e00-\u9fa5]+',i[10],re.S)
        new_data = "".join(new_data)
        new_data = jieba.cut(new_data,cut_all=False)
        for i in new_data:
            if i not in stop:
                cn_data.append(i)

    df = pd.DataFrame(data=cn_data,columns=['word'])
    df = df['word'].value_counts()
    cn_name = list(df.index.values)
    cn_numb= list(df.values)
    cn_tuple = []

    for i in range(len(cn_name)):
        if cn_numb[i]>=250:
            cn_tuple.append((str(cn_name[i]),int(cn_numb[i])))

    df = pd.DataFrame(data=eng_data,columns=['word'])
    df = df['word'].value_counts()
    eng_name = list(df.index.values)
    eng_numb= list(df.values)
    eng_tuple = []

    for i in range(len(eng_name)):
        if eng_numb[i]>=100:
            eng_tuple.append((str(eng_name[i]),int(eng_numb[i])))

    data_tuple = eng_tuple+cn_tuple

    c = (
        WordCloud()
            .add(series_name="词云图",
                 data_pair=data_tuple,
                 word_size_range=[20, 70],
                 shape=SymbolType.DIAMOND,
                 textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"))
            .render("html/wordcloud_image.html")
    )

if __name__ == '__main__':
    map_show()
    map3D_show()
    quality_show()
    edu_with_salary_show()
    clound_show()
