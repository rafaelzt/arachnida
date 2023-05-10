import requests
import os
from bs4 import BeautifulSoup
import argparse
import re

def pull_img(imgs, path):
    for url in imgs:
        img_url = url
        try:
            if len(img_url) > 2:
                name = img_url.split("/")
                if len(name[-1]) < 0:
                    return
                ext = name[-1].split(".")
                if ext[-1] in ["jpg", "jpeg", "png", "gif", "bmp"]:
                    img_name = path + '/' + name[-1]
                    response = requests.get(img_url, stream=True)
                    response.raise_for_status()
                    with open(img_name, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
        except:
            continue

def create_list_img(soup):
    imgs = soup.find_all("img")
    imges = soup.find_all("image")
    lista = []
    for x in imgs:
        lista.append(x.get('src'))
        srcset = x.get('srcset')
        if srcset:
            lista.append(srcset.split(" ")[0])
    for x in imges:
        lista.append(x.get('href'))
    return list(set(lista))

def is_dominio(org, new, sub):
    if org in new:
        return new
    name = sub.split('/')
    if not(re.match("^(https?|file):\/\/[^\s\/$.?#].[^\s]*$", new)):
        if new[0] == '/':
            return (name[0] + "//" + name[2] + new)
        else:
            return (name[0] + "//" + name[2] + '/' + new)

def find_url(soup, org, nivel, blacklist, path, back):
    url = soup.find_all("a")
    if len(url) == 0:
        return
    imgs = create_list_img(soup)
    pull_img(imgs, path)
    for link in url:
        try:
            link_url = link.get('href')
            link_url = is_dominio(org, link_url, back)
            if org in link_url and link_url not in blacklist and nivel > 1:
                blacklist.append(link_url)
                tmp_page = requests.get(link_url)
                tmp_soup = BeautifulSoup(tmp_page.content, "html.parser")
                find_url(tmp_soup, org, (nivel - 1), blacklist, path, link_url)
        except:
            continue

def level(l, r):
    if r:
        nivel = l
    else:
        nivel = 1
    if nivel < 0:
        nivel = 1
    return nivel

parser = argparse.ArgumentParser(description='Web scraping, get ALL photos from a website indicating sublevels')
parser.add_argument('url', help='search link')
parser.add_argument('-r', '--recursive', dest="r", action='store_true', help='Number of search sublevels')
parser.add_argument('-l', '--length', metavar="[N]", dest='l', type=int, default=5, help='Number of search sublevels')
parser.add_argument('-P', '--PATH', metavar="[PATH]", type=str, default="./data", dest='p', help='Path to save images (default ./Data)')
args = parser.parse_args()

if not os.path.exists(args.p):
    os.mkdir(args.p)

blacklist = []

if args.url.startswith('https://'):
    org = args.url
    domain = args.url.replace("https://", "")
elif args.url.startswith('http://'):
    org = args.url
    domain = args.url.replace("http://", "")
elif args.url.startswith('file://'):
    org = args.url
    domain = args.url.replace("file://", "")
else:
    org = "https://" + args.url
    domain = args.url

nivel = level(args.l, args.r)

try:
    page = requests.get(org)
    soup = BeautifulSoup(page.content, "html.parser")
    blacklist.append(org)
    find_url(soup, domain, nivel, blacklist, args.p, org)
except:
    print("ERROR: broken link")

