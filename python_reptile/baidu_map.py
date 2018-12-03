#!/usr/bin/env python
# encoding: utf-8
"""
爬取百度地图信息##
@author:nikan

@file: baidu_map.py

@time: 04/03/2018 10:22 PM
"""

import requests
import re
import csv
import time

all_page_no = 0


def business_from_baidu_ditu(citycode='287', key_word='珠宝', pageno=0, writer=None):
    parameter = {
    "newmap": "1",
    "reqflag": "pcmap",
    "biz": "1",
    "from": "webmap",
    "da_par": "direct",
    "pcevaname": "pc4.1",
    "qt": "con",
    "c": citycode,        # 城市代码
    "wd": key_word,       # 搜索关键词
    "wd2": "",
    "pn": pageno,         # 页数
    "nn": pageno * 10,
    "db": "0",
    "sug": "0",
    "addr": "0",
    "da_src": "pcmappg.poi.page",
    "on_gel": "1",
    "src": "8",
    "gr": "3",
    "l": "12",
    "tn": "B_NORMAL_MAP",
    # "u_loc": "12621219.536556,2630747.285024",
    "ie": "utf-8",
    # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
    "t": "1468896652886"}
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87Safari/537.36'}
    
    url = 'http://map.baidu.com/'
    htm = requests.get(url, params=parameter, headers=headers)
    htm = htm.text.encode('latin-1').decode('unicode_escape')  # 转码
    pages_pattern = r'"total":([1-9]+)'
    global all_page_no
    if not all_page_no:
        all_page_no = re.findall(pages_pattern, htm)[0]
        print(all_page_no)
    
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    
    htm = re.findall(pattern, htm)  # 按段落匹配
    

    
    for r in htm:
        pattern = r'(?<=\b"\},"name":").+?(?=")'
        name = re.findall(pattern, r)
#if not name:
        pattern = r'(?<=\b,"name":").+?(?=")'
        name = re.findall(pattern, r)

        pattern = r'.+?(?=")'
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        pattern2 = r'(?<="tel":").+?(?=")'
        if not phone:
            phone = re.findall(pattern2, r)
        if phone and phone[0] and '",' != phone[0]:
            phone_list = phone[0].split(sep=',')
            for number in phone_list:
                if re.match('1', number):
                    print('write_{}')
                    print(str(citycode)+name[0]+','+address+','+ str(number))
                    writer.writerow((name[0], address, number))


def main(city_num_list=None, keyworklist=None):
    """
    执行函数， 需要提供city_num_list & keyworklist
    :param city_num_list: 百度地图城市代码列表
    :param keyworklist: 关键词列表
    :return:
    """
    citynumlist = city_num_list if city_num_list else []
    keywordlist = keyworklist if keyworklist else []
    
    start = time.time()
    num = 1
    
    #建立csv文件，保存数据
    csvFile = open(r'%s.csv' % 'CityData','a+', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    writer.writerow(('name', 'address', 'number'))
    
    for citycode in citynumlist:
        for kw in keywordlist:
            for page in range(1):
                business_from_baidu_ditu(citycode=citycode, key_word=kw, pageno=page, writer=writer)
                #防止访问频率太高，避免被百度公司封
                time.sleep(1)
            for page in range(1, int(all_page_no)):
                business_from_baidu_ditu(citycode=citycode, key_word=kw, pageno=page, writer=writer)
                time.sleep(1)
            if num%20 == 0:
                time.sleep(2)
            if num%100== 0:
                time.sleep(3)
            if num%200==0:
                time.sleep(7)
            num = num + 1
    
    end = time.time()
    lasttime = int((end-start))
    print('耗时'+str(lasttime)+'s')

    csvFile.close()


if __name__ == '__main__':
    main([33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,731,770,789,792,1214,1215,1216,1217,1218,1277,1293,1498,1515,1641,1642,1643,1644,1713,2031,2032,2033,2358,2359,2634,2654,2734,2757,2758], ['珠宝'])
