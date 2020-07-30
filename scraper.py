import requests
import time
from bs4 import BeautifulSoup

#connection = MongoClient('192.168.0.234', 27017)
#db = connection.reading_list
#articles = db.articles


security_posts = requests.get('https://dev.to/t/security')
linux_posts = requests.get('https://dev.to/t/linux')
daily_swig_posts = requests.get('https://portswigger.net/daily-swig')
soup1 = BeautifulSoup(security_posts.text, "html.parser")
soup2 = BeautifulSoup(linux_posts.text, "html.parser")
soup3 = BeautifulSoup(daily_swig_posts.text, "html.parser")
security_article_data = []
linux_article_data = []
daily_swig_data = []
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


def getFirstThree(article_array, latest):
    for i in range(3):
        latest.append(article_array[i])



#db.articles.delete_many({})

def addToDatabase(latest_list, collection):
    for seg in latest_list:
        post_data = {
                'title': seg[0],
                'url': seg[1],
        }
        new_doc = collection.insert_one(post_data)


findDevLinks(soup1, security_article_data)

findDevLinks(soup2, linux_article_data)

findDailySwigLinks(soup3, daily_swig_data)

print(latest_articles)
