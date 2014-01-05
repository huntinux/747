#!/usr/bin/python2
# -*- coding: utf-8 -*-

# 引入相应的模块
import requests
from bs4 import BeautifulSoup
import re       # 使用正则表达式
import psycopg2 # 操作数据库postgreSQL

# 获取网页
url  = 'http://www.seatguru.com/airlines/Air_China/Air_China_Boeing_747-400.php'
r    = requests.get(url)  # 发出request 得到 response
data = r.text             # r.text为response的正文，也就是html文件的内容。

# 解析网页
soup = BeautifulSoup(data)  # 用BS解析此html

## 提取每个座位的信息
#  提取出所有name为td且其父亲的父亲的父亲的class属性为'standard'的标签，就是要提取的每种座位的信息
#  每6个td标签组成一组数据，插入到数据库中的seats表中。
def td_pppclass_is_standard(tag):
    return tag.name == 'td' and tag.parent.parent.parent['class'] == ['standard']
i=0
c_id=0
seatnum=''
cls=''
seattype=''
video=''
power=''
desct=''
planetype='Boeing 747-400'
print '==========extracting-seats============'
conn=psycopg2.connect("user=postgres password=postgres dbname=test")  # 连接数据库
for td in soup.find_all(td_pppclass_is_standard) :
    if(i % 6 == 0):
        seatnum=td.string       # 座位编号
    elif ( i % 6 == 1):
        cls=td.string           # 座位类别
    elif ( i % 6 == 2):
        seattype = td.string    # 座位描述
    elif ( i % 6 == 3):
        video = td.string       # 是否有TV
    elif ( i % 6 == 4):
        power = td.string       # 是否有电源
    elif ( i % 6 == 5):
        desct = td.string       # 其他描述

    i = i + 1
    if(i % 6 == 0):         # 6个td标签组成一组数据，插入到数据库中。
        print (c_id,seatnum,cls,seattype,video,power,desct,planetype)
        # 存入数据库
        #conn=psycopg2.connect("user=postgres password=postgres dbname=test") 
        cur = conn.cursor()
        cur.execute("INSERT INTO seats(id, seatnum, cls, seattype, video, power, desct, planetype) \
                values(%s, %s, %s, %s, %s, %s, %s, %s);",(c_id,seatnum,cls,seattype,video,power,desct,planetype))
        cur.close() 
        conn.commit() 
        #conn.close() 

        c_id = c_id + 1
conn.close()    # 关闭数据库
print '================done=================='


##解析seating detail
i=0             # 每四个数据一组
c_class=''      # 座位类型，对应数据库表seat_detail 中的 c_class 
c_pitch=''      # 
c_width=''      # 
c_details=''    #
c_id=0          # ID
print '======extracting-seating-detail======='
conn=psycopg2.connect("user=postgres password=postgres dbname=test") # 连接数据库
for td in soup.find_all('td',class_=re.compile('item')) :
    if(td.parent.parent.parent['class'] == ['seat-list']):
        ## 提取数据
        if(i % 4 == 0):
            c_class=td.string
        elif ( i % 4 == 1):
            for s in td.strings:
                c_pitch = s
        elif ( i % 4 == 2):
            c_width = td.string
        elif ( i % 4 == 3):
            c_details = td.p.span.string

        ## 每四个一组，存入数据库中
        i = i + 1
        if(i % 4 == 0):
            print(c_id,c_class,c_pitch,c_width,c_details,planetype) 
            cur = conn.cursor()
            cur.execute("insert into seating_detail (c_id, c_class, c_pitch, c_width, c_details, planetype) \
                            values(%s, %s, %s, %s, %s, %s);",(c_id,c_class,c_pitch,c_width,c_details,planetype))
            cur.close() 
            conn.commit() 
            c_id = c_id + 1

conn.close()    # 关闭数据库
print '===============done==============='
