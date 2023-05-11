# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 12:45:24 by rzamolo-          #+#    #+#              #
#    Updated: 2023/04/20 12:57:15 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL to download")
    parser.add_argument("-l", "--length", type=int, default=5, help="the recursion depth")
    parser.add_argument("-r", "--recursive", action="store_true", help="whether to recursively download links")
    parser.add_argument("-p", "--path", default="./data", help="the path to save the file")
    args = parser.parse_args()

    return args


def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None


def find_images(html, base_url, domain):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')

    images = []
    for img_tag in img_tags:
        src = img_tag.get('src')
        if src:
            image_url = urljoin(base_url, src)
            if urlparse(image_url).netloc == domain:
                images.append(image_url)

    print(f"Found {len(images)} images: {images}")  # Add this line for debugging
    return images



def get_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    link_tags = soup.find_all('a')

    links = []
    for link_tag in link_tags:
        href = link_tag.get('href')
        if href:
            link_url = urljoin(base_url, href)
            links.append(link_url)
    return links


def download_images(images, folder_path):
    print(f"Downloading {len(images)} images: {images}")  # Add this line for debugging
    downloaded_images = []
    for image_url in images:
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                file_name = image_url.split("/")[-1]
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                downloaded_images.append(image_url)
                print(f"Downloaded image: {image_url}")  # Add this line for debugging
            else:
                print(f"Error downloading image: {image_url}, status_code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {image_url}, error: {e}")
    return downloaded_images



def save_downloaded_urls(downloaded_images, folder_path):
    file_path = os.path.join(folder_path, "downloaded_images.txt")
    with open(file_path, "w") as f:
        for url in downloaded_images:
            f.write(f"{url}\n")


def main(args):
    base_url = args.url
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc
    folder_path = args.path

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        for file in os.scandir(folder_path):
            if file.is_file():
                os.unlink(file.path)

    html = get_html(base_url)
    if html is None:
        sys.exit(f"Error: Unable to fetch URL: {base_url}")

    print(f"HTML: {html}")
    images = find_images(html, base_url, domain)
    print(f"Found {len(images)} images on the main page: {images}")  # Add this line for debugging
    downloaded_images = download_images(images, folder_path)
    print(f"Downloaded {len(downloaded_images)} images from the main page")

    if args.recursive:
        visited = {base_url}
        to_visit = get_links(html, base_url)

        for _ in range(args.length):
            next_links = []
            for link in to_visit:
                if link not in visited:
                    visited.add(link)
                    if urlparse(link).netloc == domain:
                        html = get_html(link)
                        if html:
                            images = find_images(html, link, domain)
                            print(f"Found {len(images)} images on {link}")
                            new_downloaded_images = download_images(images, folder_path)
                            print(f"Downloaded {len(new_downloaded_images)} images from {link}")
                            downloaded_images.extend(new_downloaded_images)
                            next_links.extend(get_links(html, link))
            to_visit = next_links
        save_downloaded_urls(downloaded_images, folder_path)
        print(f"Saved {len(downloaded_images)} image URLs in downloaded_images.txt")

    else:
        save_downloaded_urls(downloaded_images, folder_path)
        print(f"Saved {len(downloaded_images)} image URLs in downloaded_images.txt")

if __name__ == "__main__":
    args = get_arguments()
    main(args)
