from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import re
import os
from operator import itemgetter 
import json
import time
from fake_useragent import UserAgent
_url = "https://www.flightclub.com/catalogsearch/result?query="
ua =UserAgent()
chrome_options = Options()
def get_results(query):
	url = "{}{}".format(_url, query)
	products= []
	user_agent = ua.random
	total_pages = -1
	curr_page = 1

	chrome_options.add_argument('user-agent={}'.format(user_agent))  
	#chrome_options.add_argument("--headless") 
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get(url="{}&page={}".format(url, curr_page))
	wait = WebDriverWait(driver, 20)
	time.sleep(5)
	soup = BeautifulSoup(driver.page_source,'lxml')

	if total_pages == -1:
		total_pages = soup.find('ul',{"class":"sc-1jid6c7-2 larejM"})
		temper = total_pages.find('span',{"class","sc-1jid6c7-4 eSjGTy"}).get_text()

	temper = temper.encode('utf-8')
	temper = temper.replace(' ', '')
	temp_list = []
	temp_list = temper.split("of")
	total_pages = int(temp_list[1])

	while curr_page < total_pages:
		chrome_options.add_argument('user-agent={}'.format(user_agent))  
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.get(url="{}&page={}".format(url, curr_page))
		try:
			div = soup.find('div',{"class": "sc-12ddmbl-0 kEGgBM"})
		except Exception as e:
			print e

		for link in div.find_all('a',{"class":"sc-12adlsx-0 hniSJt"}):
			image = link.find('img',{"class": "sc-htpNat ipJcZu"})
			name = link.find('h2',{"class": "bt2tlo-0 sc-13zm8u8-0 cQeHPV"}).get_text()
			price = link.find('div',{"class":"yszfz8-5 lbGKhm"}).get_text()
			name = name.encode('utf-8')
			price = price.encode('utf-8')
			products.append([name, image['src'], price])

		curr_page = curr_page + 1
		driver.close()
	return products

def seller(arr):
	price = [item[2] for item in arr]
	price = [sub.replace('Out of stock', '') for sub in price]
	price = [sub.replace('$', '') for sub in price]
	price = [sub.replace('+', '') for sub in price]
	price = list(filter(None, price))
	price = list(map(int, price))
	avg = sum(price) / len(price)
	return avg

def buyer(arr):
	price = [item[2] for item in arr]
	price = [sub.replace('Out of stock', '') for sub in price]
	price = [sub.replace('$', '') for sub in price]
	price = [sub.replace('+', '') for sub in price]
	price = list(filter(None, price))
	price = list(map(int, price))
	index = price.index(min(price))
	return arr[index]

if __name__ == '__main__':
	results = get_results('shoes')
	print(seller(results))
	print '\n'
	print(buyer(results))







