# #!/usr/bin/env python
# import urllib.request as urllib2
# from bs4 import *
# from urllib.parse import urljoin
#
#
# def crawl(pages, depth=None):
#     indexed_url = set()  # a set for the main and sub-HTML websites in the main website
#     for i in range(depth):
#         for page in pages:
#             if page not in indexed_url:
#                 indexed_url.add(page)
#                 try:
#                     c = urllib2.urlopen(page)
#                 except:
#                     print("Could not open %s" % page)
#                     continue
#                 soup = BeautifulSoup(c.read(), features="html.parser")
#                 links = soup('a')  # finding all the sub_links
#                 for link in links:
#                     if 'href' in dict(link.attrs):
#                         url = urljoin(page, link['href'])
#                         if url.find("'") != -1:
#                             continue
#                         url = url.split('#')[0]
#                         # if url[0:4] == 'http':
#                         #     indexed_url.add(url)
#                         indexed_url.add(url)
#         pages = indexed_url
#     return indexed_url
#
#
# # pagelist = ["https://en.wikipedia.org/wiki/Python_%28programming_language%29"]
# pagelist = ["https://nomadlist.com/"]
# urls = crawl(pagelist, depth=1)
# print(urls)



# import scrapy
#
# class BlogSpider(scrapy.Spider):
#     name = 'blogspider'
#     start_urls = ['https://www.zyte.com/blog/']
#
#     def parse(self, response):
#         for title in response.css('.oxy-post-title'):
#             yield {'title': title.css('::text').get()}
#
#         for next_page in response.css('a.next'):
#             yield response.follow(next_page, self.parse)
#
#
# inst = BlogSpider()
# links = inst.parse()
# print(links)

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json


def getdata(url):
	r = requests.get(url)
	return r.text


# create empty dict
dict_href_links = {}


def get_links(website_link):
	html_data = getdata(website_link)
	soup = BeautifulSoup(html_data, "html.parser")
	list_links = []
	for link in soup.find_all("a", href=True):

		# Append to list if new link contains original link
		if str(link["href"]).startswith((str(website_link))):
			list_links.append(link["href"])

		# Include all href that do not start with website link but with "/"
		if str(link["href"]).startswith("/"):
			if link["href"] not in dict_href_links:
				print(link["href"])
				dict_href_links[link["href"]] = None
				link_with_www = website_link + link["href"][1:]
				print("adjusted link =", link_with_www)
				list_links.append(link_with_www)

	# Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
	dict_links = dict.fromkeys(list_links, "Not-checked")
	return dict_links


def get_subpage_links(l):
	for link in tqdm(l):
		# If not crawled through this page start crawling and get links
		if l[link] == "Not-checked":
			dict_links_subpages = get_links(link)
			# Change the dictionary value of the link to "Checked"
			l[link] = "Checked"
		else:
			# Create an empty dictionary in case every link is checked
			dict_links_subpages = {}
		# Add new dictionary to old dictionary
		l = {**dict_links_subpages, **l}
	return l


# add websuite WITH slash on end
website = "https://nomadlist.com/"
# create dictionary of website
dict_links = {website: "Not-checked"}

counter, counter2 = None, 0
while counter != 0:
	counter2 += 1
	dict_links2 = get_subpage_links(dict_links)
	# Count number of non-values and set counter to 0 if there are no values within the dictionary equal to the string "Not-checked"
	# https://stackoverflow.com/questions/48371856/count-the-number-of-occurrences-of-a-certain-value-in-a-dictionary-in-python
	counter = sum(value == "Not-checked" for value in dict_links2.values())
	# Print some statements
	print("")
	print("THIS IS LOOP ITERATION NUMBER", counter2)
	print("LENGTH OF DICTIONARY WITH LINKS =", len(dict_links2))
	print("NUMBER OF 'Not-checked' LINKS = ", counter)
	print("")
	dict_links = dict_links2
	# Save list in json file
	a_file = open("data_16.json", "w")
	json.dump(dict_links, a_file)
	a_file.close()
