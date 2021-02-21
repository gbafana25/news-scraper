#!/usr/bin/python3

import requests
import time
from bs4 import BeautifulSoup
import subprocess


security_posts = requests.get('https://dev.to/t/security')
linux_posts = requests.get('https://dev.to/t/linux')
ars_posts = requests.get('https://arstechnica.com/gadgets')
daily_swig_posts = requests.get('https://portswigger.net/daily-swig')
soup1 = BeautifulSoup(security_posts.text, "html.parser")
soup2 = BeautifulSoup(linux_posts.text, "html.parser")
soup3 = BeautifulSoup(daily_swig_posts.text, "html.parser")
soup4 = BeautifulSoup(ars_posts.text, "html.parser")
security_article_data = []
linux_article_data = []
daily_swig_data = []
ars_data = []
latest_articles = []

def findDevLinks(soup, article_array):
	for link in soup.findAll('a'):
		if link.has_attr('id') and link.has_attr('data-preload-image'):
			article_name = ""
			if link.string == None:
				article_name = "Article name not found"
			else:
				article_name = link.string
			new_name = article_name.strip()
			article_id = link.get('href')
			full_link = "https://dev.to" + article_id
			article_sep = article_id.split('/', 3)
			fields = [new_name, full_link]
			article_array.append(fields)
	for i in range(3):
		latest_articles.append(article_array[i])

def findDailySwigLinks(soup, article_array):
    for link in soup.findAll('a',{'class': "noscript-post"}):
        element = []
        url = "https://portswigger.net" + link.get('href')
        element.append(url)
        for name in link.findAll('span', {'class': 'main'}):
            element.insert(0, name.string)
        article_array.append(element)
    for i in range(3):
        latest_articles.append(article_array[i])

def findArsLinks(soup, article_array):
	for tag in soup.findAll('h2'):
		for link in tag.findAll('a'):
			if link.has_attr('href'):
				field = [link.string, link.get('href')]
				article_array.append(field)
	for i in range(3):
		latest_articles.append(article_array[i])

def getFirstThree(article_array, latest):
    for i in range(3):
        latest.append(article_array[i])


findDevLinks(soup1, security_article_data)

findDevLinks(soup2, linux_article_data)

findDailySwigLinks(soup3, daily_swig_data)

findArsLinks(soup4, ars_data)

for i in range(len(latest_articles)):
	print(str(i) + ". " + latest_articles[i][0] + "\n")

option = input("Type number of article you want to open: ")
print("You selected option: " + latest_articles[int(option)][0])
subprocess.run(['firefox', latest_articles[int(option)][1]])
