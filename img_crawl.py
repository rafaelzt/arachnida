import argparse
import os
import requests
import tldextract
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_links(url, max_depth):
    """
    Retrieves all links from the specified URL and its subdomains up to the
    specified depth.
    """
    print(f"Retrieving links from {url}")
    links = set()
    base_url = urlparse(url)
    visited = set()
    queue = [(url, 0)]

    while queue:
        url, depth = queue.pop(0)
        visited.add(url)

        if depth <= max_depth:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    if href.startswith("/"):
                        href = f"{base_url.scheme}://{base_url.netloc}{href}"
                    elif not href.startswith("http"):
                        href = f"{url}/{href}"

                    # Extract the domain of the link
                    link_domain = tldextract.extract(href).registered_domain

                    # Extract the domain of the base URL
                    base_domain = tldextract.extract(url).registered_domain

                    # Check if the link is in the same domain as the base URL
                    if link_domain == base_domain and href not in visited:
                        links.add(href)
                        queue.append((href, depth + 1))

    return links

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL to download")
    parser.add_argument("-l", "--length", type=int, default=2, help="the recursion depth")
    parser.add_argument("-r", "--recursive", action="store_true", help="whether to recursively download links")
    parser.add_argument("-p", "--path", default="./data", help="the path to save the file")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        os.makedirs(args.path)

    links = get_links(args.url, args.length)
    print(f"Found {len(links)} links on {args.url} and its subdomains up to depth {args.length}:")

    for link in links:
        print(link)