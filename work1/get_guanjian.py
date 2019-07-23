#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime
import re


def getguanjian(url):
    response = requests.get(url)
    html = response.text

    data = {}
    soup = BeautifulSoup(html, 'lxml')
    #获取所有的标题数据
    info = soup.select('h2')
    for i in info:
        title = i.string

        #排除手机端的关键词
        patt = re.compile(r'手机')
        if re.search(patt, str(title)):
            break
        info = i.next_siblings
        g = []
        for i in info:
            for q in i:
                # print(q)
                patt = re.compile(r'.*>(.*?)<.*')
                r = re.findall(patt, str(q))
                if r:
                    g.append(r[0])
        if title:
            data[title] = g
    #判断多少个搜索引擎
    result = {}
    if len(data) == 1:
        for k, v in data.items():
            result[k] = v[:30]
        return result
    elif len(data) == 2:
        for k, v in data.items():
            result[k] = v[:15]
        return result


def insert_xlxs(urls, getguanjian):
    #将网页上获取的内容写入到xlsx表中
    time = datetime.now()
    time = time.strftime('%Y-%m-%d')
    workbook = xlsxwriter.Workbook('%s关键词.xlsx' % time)
    worksheet = workbook.add_worksheet()

    fiel = 0
    for url in urls:
        gdict = getguanjian(url)
        worksheet.write(0, fiel, url)
        count = 1
        for key, vlues in gdict.items():
            for vv in vlues:
                worksheet.write(count, fiel + 1, key)
                worksheet.write(count, fiel, vv)
                count += 1
        fiel += 3
    workbook.close()


if __name__ == '__main__':
    urls = []
    with open('url.txt', 'r') as fobj:
        for url in fobj:
            url = url.strip()
            urls.append(url)
    insert_xlxs(urls, getguanjian)