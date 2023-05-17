# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 12:45:24 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/17 10:59:34 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
import os
from bs4 import BeautifulSoup
import argparse
import re

extensions =  ["jpg", "jpeg", "png", "gif", "bmp"]

def get_args():
	parser = argparse.ArgumentParser(description="Download images from a given URL, with a given recursion level")
	parser.add_argument("URL",
						help="URL to download images from")

	parser.add_argument("-r", "--recusive",
						dest="recursive",
						action="store_true",
						help="Recursion level")

	parser.add_argument("-l", "--length",
						metavar="[N]",
						dest="length",
						type=int,
						default=5,
						help="Length of recursion (default 5)")

	parser.add_argument("-p", "--path",
						metavar="[PATH]",
						type=str,
						default="./data",
						dest="path",
						help="Path to store images (default ./data)")
	
	return (parser)

# def pull_img(imgs, path):
# 	for url in imgs:
# 		img_url = url
# 		try:
# 			if (len(img_url) > 2):
# 				name = img_url.split("/")
# 				if (len(name[-1]) < 0):
# 					return
# 				ext = name[-1].split(".")
# 				if ext[-1] in extensions:
# 					image_name = path + '/' + name[-1]
# 					respuesta = requests.get(img_url, stream=True)
# 					respuesta.raise_for_status()
# 					with open(image_name, "wb") as archivo:
# 						for chunk in respuesta.iter_content(chunk_size=8192):
# 							archivo.write(chunk)
# 		except:
# 				continue

# args = parser.parse_args()

# def	create_list_img(soup):
# 	imgs = soup.find_all("img")
# 	images = soup.find_all("image")
# 	lst_mg = []
# 	tmp = []
# 	for x in imgs:
# 		lst_mg.append(x.get( 'src' ))
# 	for x in imgs:
# 		e = (x.get( 'srcset' ))
# 		if (e != None):
# 			a = e.split(" ")[0]
# 			lst_mg.append(a)
# 	for x in images:
# 		lst_mg.append(x.get( 'href' ))
# 	lst_mg = list(set(lst_mg))
# 	return (lst_mg)

# def domain(org, new, sub):
# 	if (org in new):
# 		return new
# 	name = sub.split('/')
# 	if not(re.match("^(https?|file):\/\/[^\s\/$.?#].[^\s]*$", new)):
# 		if new[0] == '/':
# 			return (name[0] + "//" + name[2] + new)
# 		else:
# 			return ( name[0] + "//" + name[2] + '/' + new)

# def find_url(soup, org, level, blacklist, path, back):
# 	url = soup.find_all("a")
# 	if (len(url) == 0):
# 		return
# 	imgs = create_list_img(soup)
# 	pull_img(imgs, path)
# 	for link in url:

# 		try:
# 			link_url = (link.get( 'href' ))
# 			link_url = domain(org, link_url, back)

# 			if (org in link_url) and not(link_url in blacklist) and (nivel > 1):
# 				blacklist.append(link_url)
# 				tmp_page = requests.get(link_url)
# 				tmp_soup = BeautifulSoup(tmp_page.content, "html.parser")
# 				find_url(tmp_soup, org, (level - 1), blacklist, path, link_url)
# 		except:
# 			continue

# def level(l, r):
# 	if r:
# 		level = l
# 	else:
# 		level = 1
# 	if level < 0:
# 		level = 1
# 	return level

# if not os.path.exists(args.p):
# 	os.mkdir(args.p)

# blacklist = []

# if args.url.startswith('https://'):
# 	org = args.url
# 	domain = args.url.replace("https://", "")
# elif args.url.startswith('http://'):
# 	org = args.url
# 	domain = args.url.replace("http://", "")
# elif args.url.startswith('file://'):
# 	org = args.url
# 	domain = args.url.replace("file://", "")
# else:
# 	org = "https://" + args.url
# 	domain = args.url

# nivel = level(args.l, args.r)
# try:
# 	page = requests.get(org)
# 	soup = BeautifulSoup(page.content, "html.parser")
# 	blacklist.append(org)
# 	find_url(soup, domain, level, blacklist, args.p, org)
# except:
# 	print("URL Error")


if __name__ == "__main__":
	parser = get_args()
	domain = parser.parse_args().URL.split("/")[2]
	path = parser.parse_args().path
	recursive_flag = parser.parse_args().recursive
	length = parser.parse_args().length
	
	print(parser.parse_args())
	print(domain)
	print(path)
	print(recursive_flag)
	print(length)
	
	