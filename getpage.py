#!/usr/bin/python2
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re       
import psycopg2 
import sys
import urllib
import os

def grab_page_info(num,url):
	# get the html page: url
	r    = requests.get(url)  
	data = r.text             

	# soup it 
	soup = BeautifulSoup(data) 

	## grab plane information
	planeid=num
	name=audio=video=AcPower=food=overview=seatmap=seatmapkey=''
	#get plane name
	for pname in soup.find_all('h2',class_='h2-fix') :
		name=pname.string
	#get auidio video acpower food
	i = 0
	for div in soup.find_all('div',id = re.compile('link')) :
		if(i % 4 == 0):
			audio=div.p.string       
		elif ( i % 4 == 1):
			video=div.p.string   
		elif ( i % 4 == 2):
			AcPower = div.p.string    
		elif ( i % 4 == 3):
			food = div.p.string
		i = i + 1
	#get overview
	for div in soup.find_all('div',class_ = 'tips-box') :
		overview = div.p.string
	# get seatmap
	imgpath = 'img'
	if (not os.path.exists(imgpath)):
		print "create dir " + imgpath
		os.mkdir(imgpath)
	else:
		print "dir "+ imgpath +" exists"

	if (not os.path.exists(imgpath + '/' + name )):
		os.mkdir(imgpath + '/' + name)
	else:
		print "dir " + imgpath + '/' + name + " exists"

	seatmap = os.getcwd() + '/' + imgpath + '/' + name + '/seatmap'
	if (os.path.exists(seatmap)):
		print "seatmap for this plane exists"
	else:
		for img in soup.find_all('img',class_="plane"): 
			imgurl = img['src']	
			urllib.urlretrieve(imgurl, imgpath + '/' + name + '/seatmap')

	# get seatmapkey
	seatmapkey = os.getcwd() + '/' + imgpath + '/' + name + '/seatmapkey'
	if (os.path.exists(seatmapkey)):
		print "seatmapkey for this plane exists"
	else:
		for img in soup.find_all('img',class_="legend"): 
			imgurl = img['src']	
			urllib.urlretrieve(imgurl, imgpath + '/' + name + '/seatmapkey')

	print (planeid, name, audio, video, AcPower, food, overview, seatmap, seatmapkey)
	# insert data into database
	try:
		conn=psycopg2.connect("user=postgres password=postgres dbname=test")  
	except:
		print "can't connect to database"
		sys.exit(1)
	cur = conn.cursor()
	try:
		cur.execute("INSERT INTO planes(id, name, audio, video, acpower, food, overview, seatmap, seatmapkey) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);",(planeid,name,audio,video,AcPower,food,overview,seatmap,seatmapkey))
	except Exception, e:
		print "can't insert the above record, the reason is :"
		print e.pgerror
		sys.exit(1)
	cur.close() 
	conn.commit() 
	conn.close() 

	## 提取每个座位的信息
	#  提取出所有name为td且其父亲的父亲的父亲的class属性为'standard'的标签，就是要提取的每种座位的信息
	#  每6个td标签组成一组数据，插入到数据库中的seats表中。
	def td_pppclass_is_standard(tag):
		return tag.name == 'td' and tag.parent.parent.parent['class'] == ['standard']
	i=0
	id=0
	seatnum=cls=seattype=video=acpower=descpt=''
	# 连接数据库
	try:
		conn=psycopg2.connect("user=postgres password=postgres dbname=test")  
	except:
		print "can't connect to database"
		sys.exit(1)
	print '==========extracting-seats============'
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
			acpower = td.string     # 是否有电源
		elif ( i % 6 == 5):
			descpt = td.string      # 其他描述

		i = i + 1
		if(i % 6 == 0):             # 6个td标签组成一组数据，插入到数据库中。
			print (planeid,id,seatnum,cls,seattype,video,acpower,descpt)
			cur = conn.cursor()
			try:
				cur.execute("INSERT INTO seats(planeid, id, seatnum, cls, seattype, video, acpower, descpt) \
						VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",(planeid,id,seatnum,cls,seattype,video,acpower,descpt))
			except Exception, e:
				print "can't insert the above record, the reason is :"
				print e.pgerror
				sys.exit(1)
	
			cur.close() 
			conn.commit() 
			id = id + 1
	conn.close()    # 关闭数据库
	print '================done=================='


	##解析seating detail
	i = 0         
	id = 0
	cls=pitch=width=details=''
	# 连接数据库
	try:
		conn=psycopg2.connect("user=postgres password=postgres dbname=test") 
	except:
		print "can't connect to database"
		sys.exit(1)

	print '======extracting-seating-detail======='
	for td in soup.find_all('td',class_=re.compile('item')) :
		if(td.parent.parent.parent['class'] == ['seat-list']):
			## 提取数据
			if(i % 4 == 0):
				cls=td.string
			elif ( i % 4 == 1):
				for s in td.strings:
					pitch = s
			elif ( i % 4 == 2):
				width = td.string
			elif ( i % 4 == 3):
				details = td.p.span.string

			## 每四个一组，存入数据库中
			i = i + 1
			if(i % 4 == 0):
				print(planeid,id,cls,pitch,width,details) 
				cur = conn.cursor()
				try:
					cur.execute("insert into seating_detail (planeid, id, cls, pitch, width, details) \
							values(%s, %s, %s, %s, %s, %s);",(planeid, id, cls, pitch, width, details))
				except Exception, e:
					print "can't insert the above record, the reason is:"
					print e
					sys.exit(1)
				cur.close() 
				conn.commit() 
				id = id + 1

	conn.close()    # 关闭数据库
	print '===============done==============='
def test():
	grab_page_info(0,'http://www.seatguru.com/airlines/Air_China/Air_China_Airbus_A330-200.php')
	grab_page_info(1,'http://www.seatguru.com/airlines/Air_China/Air_China_Airbus_A330-200_B.php')
	grab_page_info(2,'http://www.seatguru.com/airlines/Air_China/Air_China_Airbus_A330-300_B.php')
	
if __name__ == '__main__':
	test()


# problem
# dir img should be created at first, and later execuation won't check if it exists.
