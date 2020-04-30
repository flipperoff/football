import re
from bs4 import BeautifulSoup
import requests as req
from itertools import groupby

def get_lastnews():
	resp = req.get("https://football24.ua/ru/")
 
	soup = BeautifulSoup(resp.text, 'lxml')

	body = soup.body
	main = body.main
	container = main.find('div',class_="container")
	newsListBlock = container.find('div',id='newsListBlock')
	ul = newsListBlock.find('ul')
	news = ul.find_all('li',class_='news-list-item')
	time = []
	for i in news:
		time.append(i.find('div',class_='time'))
	for i in range(len(time)):
		time[i] = time[i].text 
	a = []
	for i in news:
		a.append(i.find("a"))
	links = []
	for i in a:
		links.append("https://football24.ua/" + str(i.get('href')))
	text = []
	for i in a:
		text.append(''.join(i.find("div",class_="title").text.split('\n')))
	news_ = {}
	for i in range(len(text)):
		news_[text[i]]=links[i]
	return time,text,links,news_
	#links = ([link['href'] for link in news if link.has_attr('href')])
	#text = []
	#for i in a:
	#	text.append(i.text)
	#for i in range(len(text)):
	#	text[i] = ''.join(text[i].split('\n'))
	#news_ = {}
	#for i in range(len(text)):
	#	news_[text[i]]=links[i]


def get_news(link):
	resp = req.get(link)
 
	soup = BeautifulSoup(resp.text, 'lxml')

	body = soup.body
	main = body.main
	container = main.find("div",class_ = 'container')
	div_photo = container.find("div",class_ = 'photo')
	image = div_photo.find("img")
	src1 = image.get("src") #-ссылка на фотографию
	src2 = src1.split("?")
	src = src2[0]
	news_text = container.find("div",class_ = "news-text")
	div_title = news_text.find("div",class_ = "title")
	p_lead = div_title.find("p",class_ = "lead")
	title = p_lead.text #-заголовок новости

	p1 = news_text.find_all("p")
	p_cke_markup = news_text.find_all("p",class_ = 'cke-markup')
	p = [elem for elem in p1 if elem not in p_cke_markup]
	# p_new = []
	# for i in range(len(p)):
	# 	if ('К слову' in p[i].text) or ('Напомним' in p[i].text):
	# 		continue
	# 	p_new.append(p[i].text)
	if p[0]==title:
		p[0]=''
	text ='\n\n'.join(p)
	return src,text,title



if __name__ == "__main__":
	time,text,links,news_ = get_lastnews()
	a,b,c = get_news(links[0])
	print(c,b)


