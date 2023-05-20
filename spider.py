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

# Import required libraries
import argparse
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to get command-line arguments
def get_arguments():
    # Create an argument parser object
    parser = argparse.ArgumentParser(description='Web scraping, retrieves ALL images from a website indicating the sublevels')
    
    # Define command-line arguments
    parser.add_argument('url',
                        help='search link')
    parser.add_argument('-r', '--recursive',
                        dest="recursive",
                        action='store_true',
                        help='Number of search sublevels')
    parser.add_argument('-l', '--length',
                        metavar="[N]",
                        dest='length',
                        type=int,
                        default=5,
                        help='Number of search sublevels')
    parser.add_argument('-P', '--PATH',
                        metavar="[PATH]",
                        type=str,
                        default="./data",
                        dest='path',
                        help='Path to save images (default ./Data)')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    return args

# List of image extensions to consider
extensions = ["jpg", "jpeg", "png", "gif", "bmp"]

# Function to download and save images
def pull_img(imgs, path):
    for url in imgs:
        img_url = url
        try:
            if len(img_url) > 2:
                name = img_url.split("/")
                if len(name[-1]) < 0:
                    return
                file_extension = name[-1].split(".")
                if  file_extension[-1] in extensions:
                    image_filename = path + '/' + name[-1]
                    response = requests.get(img_url, stream=True)
                    response.raise_for_status()
                    with open(image_filename, "wb") as archivo:
                        for chunk in response.iter_content(chunk_size=8192):
                            archivo.write(chunk)
        except:
            continue

# Function to create a list of image URLs from the HTML content
# srcset? 
def create_list_img(soup):
    imgs = soup.find_all("img")
    images = soup.find_all("image")
    img_list = []
    for x in imgs:
        img_list.append(x.get('src'))
    for x in imgs:
        e = x.get('srcset')
        if e is not None:
            a = e.split(" ")[0]
            img_list.append(a)
    for x in images:
        img_list.append(x.get('href'))
    img_list = list(set(img_list))
    return img_list

# Function to handle domain checking and URL construction
def is_domain(org, new, sub):
    if org in new:
        return new
    name = sub.split('/')
    if not re.match("^(https?|file):\/\/[^\s\/$.?#].[^\s]*$", new):
        if new[0] == '/':
            return name[0] + "//" + name[2] + new
        else:
            return name[0] + "//" + name[2] + '/' + new

# Recursive function to find and download images from URLs
def find_url(soup, org, level, blacklist, path, back):
    urls = soup.find_all("a")
    if len(urls) == 0:
        return
    imgs = create_list_img(soup)
    pull_img(imgs, path)
    for link in urls:
        try:
            link_url = is_domain(org, link.get('href'), back)
            if org in link_url and link_url not in blacklist and level > 1:
                print(">>", link_url)
                blacklist.append(link_url)
                temporary_page = requests.get(link_url)
                temporary_soup = BeautifulSoup(temporary_page.content, "html.parser")
                find_url(temporary_soup, org, (level - 1), blacklist, path, link_url)
        except:
            continue

# Function to determine the search level based on command-line arguments
def get_level(length, recursive):
    if recursive:
        level = length
    else:
        level = 1
    if level < 0:
        level = 1
    return level

# Function to check the provided URL and initiate the scraping process
def check_url(args):
    blacklist = []
    
    # Create the target directory if it doesn't exist
    if not os.path.exists(args.path):
        os.mkdir(args.path)

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

    level = get_level(args.length, args.recursive)
    try:
        page = requests.get(org)
        soup = BeautifulSoup(page.content, "html.parser")
        blacklist.append(org)
        find_url(soup, domain, level, blacklist, args.path, org)
    except:
        print("ERROR: Broken link")

# Main execution
if __name__ == "__main__":
    args = get_arguments()
    check_url(args)
