import csv
from msedge.selenium_tools import Edge, EdgeOptions
import requests
import re
import json
from lxml import etree
from fake_useragent import UserAgent
import time
# encoding = 'utf-8-sig'

# 使用Edge驱动，创建实例，并设置内核、执行文件路径、驱动路径
options = EdgeOptions()
options.use_chromium = True
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver = Edge(options=options, executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")


# proxies = {
#            # 'https': '94.240.33.242:3128',
#            #  'http': '42.228.3.155:8080',
#            #  'http': '113.128.16.209:8118',
#             'http': '27.191.60.107:3256',
#             'http': '183.195.106.118:8118'
#            }

ua = UserAgent()
headers = {
    'Cookie': 'guid=23ad5f7d0c759d050753ac1a98dd3af8; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60110200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60110200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%B4%F3%CA%FD%BE%DD%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21',
    'User-Agent': ua.random
    }

detail = ['job_name', 'company_name', 'providesalary_text', 'workarea_text', 'companytype_text', 'companyind_text', 'attribute_text']


def run():
    driver.get('https://www.51job.com/')
    # 点击输入框
    driver.find_element_by_id('kwdselectid').click()
    # 在输入框中输入大数据
    driver.find_element_by_id('kwdselectid').send_keys('大数据')
    # 点击搜索
    driver.find_element_by_xpath("//*/button[text()='搜索']").click()
    # 选择全国范围
    # driver.find_element_by_xpath("//*/span[text()='福州']").click()
    # driver.find_element_by_xpath("//*/span[text()='福建省']").click()
    # 对页面进行遍历,k代表当前为第几页
    k=1
    for page in range(2, 100):
        # l 代表当前第几条数据
        l = 1
        # 获取当前页面url
        currentPageUrl = driver.current_url
        # 发起请求
        response = requests.get(currentPageUrl, headers=headers).text
        # print(response)
        # 正则查找当页的全部职位信息
        r = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', response, re.S)
        # 进行拼接
        string = ''.join(r)
        # 更改数据格式
        infodict = json.loads(string)
        # 通过字典的键获取对应的值
        engine_jds = infodict['engine_jds']
        for i in engine_jds:
            time.sleep(1)
            # 判断需要的键是否存在
            flag = 1
            for j in detail:
                # print(j)
                if j not in i.keys():
                    flag = 0
            if flag == 0:
                continue
            # 岗位信息、招聘公司、薪资、工作地点、工作经验、学历要求、公司资质、职位描述
            job_name = i['job_name']
            company_name = i['company_name']
            providesalary_text = i['providesalary_text']
            workarea_text = i['workarea_text']
            companytype_text = i['companytype_text']
            companyind_text = i['companyind_text']

            # 包含了工作地点、工作经验、学历要求、招聘人数，将其分割开，其中也负责了一部分数据清洗
            attribute_text = i['attribute_text']
            # print(experience_text + " " + requirement_text + " " + recruit_people_text)
            if len(attribute_text) == 4:
                experience_text = attribute_text[1]
                requirement_text = attribute_text[2]
                recruit_people_text = attribute_text[3]
            else:
                experience_text = ''
                requirement_text = ''
                recruit_people_text = ''

            companysize_text = i['companysize_text']
            # 获取子页面url
            job_href = i['job_href']
            # print(job_href)

            # response1 = requests.get(job_href, headers =headers,proxies=proxies,timeout=(3,7))
            response1 = requests.get(job_href, headers=headers)
            response1.encoding = response1.apparent_encoding
            # print(response1.text)

            # job_detail = etree.HTML(response1.text).xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p//text()')
            job_detail = etree.HTML(response1.text).xpath('//*/div[@class = "bmsg job_msg inbox"]//text()')
            # 将列表转化为字符串
            job_detail = ''.join(job_detail)
            # 去除内部空格
            job_detail = ''.join(job_detail.split())
            # print(job_detail)
            print("第"+str(k)+"页"+": 第"+str(l)+"条数据")
            l = l+1
            # 储存到本地文件
            with open('51job.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([job_name, company_name, providesalary_text, workarea_text, companytype_text, experience_text, requirement_text, recruit_people_text, companysize_text, companyind_text, job_detail])
            f = open('51job1（test）.csv', 'a', encoding='utf-8')
            f.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(job_name, company_name, providesalary_text, workarea_text, companytype_text, experience_text, requirement_text, recruit_people_text, companysize_text, companyind_text, job_detail))
            f.close()
        k = k+1
        print("第{}页爬完了".format(page-1))
        # 点击页面
        show_more = driver.find_element_by_xpath("//*/a[contains(text(),'%s')]" % str(page))
        driver.execute_script("arguments[0].click();", show_more)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    run()
