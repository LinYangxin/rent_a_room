import os
import re
import time
import requests
from lxml import etree


def douban_parser(response,pattern_interest,pattern_ban):
	selector = etree.HTML(response.content)
	info = selector.xpath("//tr[@class]")
	for i in info:
		title = i.xpath("td[@class='title']/a/@title")
		website = i.xpath("td[@class='title']/a/@href")
		user = i.xpath("td[@nowrap='nowrap']/a//text()")
		response = i.xpath("td[@nowrap='nowrap']/text()")
		id = re.findall(r'\d+',str(website))

		flag0 = pattern_interest.search(str(title))
		flag1 = pattern_ban.search(str(title))
		flag2 = 1

		try:
			f0 = open('reg.txt', 'r')
		except:
			# os.mknod("reg.txt")
			print('创建文件失败')
			exit()

		if id:
			# to filter the post we have seen
			#print(id)
			if str(id[0]) in f0.read():
				flag2 = 0

			if flag0 and not flag1 and flag2:
				f1 = open("reg.txt",'a')
				try:
					f1.write("{0},{1},{2}\n".format(id[0],title[0],website[0]))
				except:
					print("error0")
					pass
				print(title[0])
				print(website[0])


if __name__ == '__main__':
	#keyword_interest = r'英伦|莱英花园|大冲|龙井|科苑|深大|桂庙|南头|科技园|科兴|豪方'
	#keyword_ban = r'公寓|限女|妹|女生合租|已出租|求|固戍|整租|单间|岗厦|房源|整套|床位'
	keyword_interest = r'英伦|莱英花园|科苑|深大|桂庙|大冲|科技园|科兴|西丽|茶光|龙井|桃源|龙辉花园|珠光|一室一厅|冠铭花园|一房一厅|单室套'
	keyword_ban = r'龙华|龙胜|清湖|固戍|坪洲|男生|龙岗|岗厦|公寓|已出租|求|合租|床位|三室一厅|主卧|次卧|室友'
	header = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
		"Connection": "keep-alive",
		"Host": "www.douban.com",
		"Referer": "https://www.douban.com/group/szsh/discussion?start=0",
		"Upgrade - Insecure - Requests": "1",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	}

	urls = ["https://www.douban.com/group/szsh/","https://www.douban.com/group/106955/","https://www.douban.com/group/nanshanzufang/"
			"https://www.douban.com/group/551176/","https://www.douban.com/group/498004"]

	pattern_interest = re.compile(keyword_interest)
	pattern_ban = re.compile(keyword_ban)

	for url in urls:
		for i in range(0, 700, 25):
			time.sleep(1)
			response = requests.get("{0}/discussion?start={1}".format(url,str(i)),headers=header)
			douban_parser(response,pattern_interest,pattern_ban)
		




