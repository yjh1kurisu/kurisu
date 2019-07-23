#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import pymysql


def getbookinfo():
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safar"}
    response = requests.get(url='https://book.douban.com/')
    html = response.text
    bookinfo = []
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('li .info')
    for i in info:
        link = i.select('.title a')
        if link:
            link = link[0].attrs['href']

        author = i.select('.author')
        if author:
            author = author[0].string.strip()

        bookname = i.select('.more-meta h4')
        if bookname:
            bookname = bookname[0].string.strip()

        time =  i.select('.year')
        if time:
            time = time[0].string.strip()

        press = i.select('.publisher')
        if press:
            press = press[0].string.strip()

        if bookname:
            bookinfo.append(tuple([bookname, author, time, press, link]))

    return bookinfo
    # for i in bookinfo:
    #     print(i)

def insert_data(bookinfo):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123qqq...A',
        db='book',
        charset='utf8'
    )
    cursor = conn.cursor()

    insert = "insert into douban(bookname, author, date, press, link) values(%s, %s, %s, %s, %s)"
    data = bookinfo
    cursor.executemany(insert, data)
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == '__main__':
    bookinfo = getbookinfo()
    insert_data(bookinfo)
