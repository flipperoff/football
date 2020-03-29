import telebot
import config
from bs4 import BeautifulSoup
import requests as req
from itertools import groupby
from telebot import types
from requests import get

bot = telebot.TeleBot(config.TOKEN)

main_src = ''
main_text =''
main_title =''

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
	for i in range(len(p)):
		p[i]=p[i].text
	if p[0]==title:
		p[0]=''
	text ='\n\n'.join(p)
	return src,text,title,link


def post(src,text,title):
	bot.send_photo(chat_id ='@whoscoredchannel',photo = get(str(src)).content,caption = str(title))
	bot.send_message('@whoscoredchannel',str(text))



@bot.message_handler(commands=['start'])
def welcome(message):
	global main_src
	global main_text
	global main_title
	bot.send_photo(message.chat.id, get("https://news.liga.net/images/general/2019/09/25/thumbnail-tw-20190925111433-3882.jpg").content)

	time,text,links,news_ = get_lastnews()

	markup = types.InlineKeyboardMarkup()
	item1 = types.InlineKeyboardButton("Новости", callback_data = "news")
	markup.add(item1)
	bot.send_message(message.chat.id, "hello",reply_markup = markup)
	main_src,main_text,main_title,link = get_news(links[0])
	post(main_src,main_text,main_title)


@bot.message_handler(commands=['offline'])
def ofline(message):
	global main_src
	global main_text
	global main_title
	bot.send_message(message.chat.id, "Offline mod")
	time,text,links,news_ = get_lastnews()
	main_src,main_text,main_title,link = get_news(links[0])
	post(main_src,main_text,main_title)
	while True:
		time,text,links,news_ = get_lastnews()
		if links[0]!=link:
			main_src,main_text,main_title,link = get_news(links[0])
			post(main_src,main_text,main_title)
		
@bot.message_handler(commands=['stop'])
def stop(message):
	pass

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	global main_src
	global main_text
	global main_title
	if call.data == "news":
		
		time,text,links,news_ = get_lastnews()

		markup = types.InlineKeyboardMarkup(row_width=1)
		item1 = types.InlineKeyboardButton(str(text[0]),callback_data="news.0")
		item2 = types.InlineKeyboardButton(str(text[1]),callback_data = 'news.1')
		item3 = types.InlineKeyboardButton(str(text[2]),callback_data = 'news.2')
		item4 = types.InlineKeyboardButton(str(text[3]),callback_data = 'news.3')
		item5 = types.InlineKeyboardButton("Главная",callback_data = 'main')
		markup.add(item1,item2,item3,item4,item5)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Новости",reply_markup = markup)
	elif call.data == 'news.0':
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Назад",callback_data = "back")
		item2 = types.InlineKeyboardButton("Запостить",callback_data = 'post')
		markup.add(item1,item2)

		time,text,links,news_ = get_lastnews()
		src,text,title,link = get_news(links[0])
		bot.send_photo(call.message.chat.id, get(str(src)).content,caption = str(title))
		bot.send_message(call.message.chat.id, str(text),reply_markup = markup)
		main_src = str(src)
		main_title = str(title)
		main_text = str(text)
	elif call.data == 'news.1':
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Назад",callback_data = "back")
		item2 = types.InlineKeyboardButton("Запостить",callback_data = 'post')
		markup.add(item1,item2)

		time,text,links,news_ = get_lastnews()
		src,text,title,link = get_news(links[1])
		bot.send_photo(call.message.chat.id, get(str(src)).content,caption = str(title))
		bot.send_message(call.message.chat.id, str(text),reply_markup = markup)		
		main_src = str(src)
		main_title = str(title)
		main_text = str(text)
	elif call.data == 'news.2':
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Назад",callback_data = "back")
		item2 = types.InlineKeyboardButton("Запостить",callback_data = 'post')
		markup.add(item1,item2)

		time,text,links,news_ = get_lastnews()
		src,text,title,link = get_news(links[2])
		bot.send_photo(call.message.chat.id, get(str(src)).content,caption = str(title))
		bot.send_message(call.message.chat.id, str(text),reply_markup = markup)
		main_src = str(src)
		main_title = str(title)
		main_text = str(text)
	elif call.data == 'news.3':
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Назад",callback_data = "back")
		item2 = types.InlineKeyboardButton("Запостить",callback_data = 'post')
		markup.add(item1,item2)

		time,text,links,news_ = get_lastnews()
		src,text,title,link = get_news(links[3])
		bot.send_photo(call.message.chat.id, get(str(src)).content,caption = str(title))
		bot.send_message(call.message.chat.id, str(text),reply_markup = markup)
		main_src = str(src)
		main_title = str(title)
		main_text = str(text)
	elif call.data == 'news.4':
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Назад",callback_data = "back")
		item2 = types.InlineKeyboardButton("Запостить",callback_data = 'post')
		markup.add(item1,item2)

		time,text,links,news_ = get_lastnews()
		src,text,title,link = get_news(links[4])
		bot.send_photo(call.message.chat.id, get(str(src)).content,caption = str(title))
		bot.send_message(call.message.chat.id, str(text),reply_markup = markup) 
		main_src = str(src)
		main_title = str(title)
		main_text = str(text)
	elif call.data == "main":
		markup = types.InlineKeyboardMarkup()
		item1 = types.InlineKeyboardButton("Новости", callback_data = "news")
		markup.add(item1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Главная",reply_markup = markup)
	elif call.data == 'back':
		bot.delete_message(call.message.chat.id, call.message.message_id)
	elif call.data == 'post':
		bot.send_photo(chat_id ='@whoscoredchannel',photo = get(str(main_src)).content,caption = str(main_title))
		bot.send_message('@whoscoredchannel',str(main_text))
	else:
		bot.send_message(call.message.chat.id,"not")
	


bot.polling(none_stop=True)