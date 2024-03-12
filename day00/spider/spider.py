import sys
import argparse
import os
import shutil
import requests
import string
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = []

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def clean_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename.strip()


def dl_image(args, url: str, depth: int):
    print("URL =", url)
    response = requests.get(url)
    visited.append(url)

    soup = BeautifulSoup(response.text, 'html.parser') # soup obj
    imgs = soup.find_all('img')
    for img in imgs: # dl all imgs in loop
        src = img['src']
        print("SRRRCCCCCC", src)
        if not src.startswith('http'):
            src = urljoin(url, src)
        filename = os.path.join(args.path, clean_filename(os.path.basename(urlparse(src).path)))
        with open(filename, 'wb') as ret:
            print("img =", filename)
            res = requests.get(src)
            ret.write(res.content)

    if (args.recurcive is True):
        print("DEPTH ",depth)
        if depth > 0:
            dom = urlparse(url).netloc
            links = soup.find_all('a', href=True)
            for link in links:
                new_url = link['href']
                print(f"link in {url}", new_url)
                if not new_url.startswith('http'):
                    new_url = urlparse(url).scheme + "://" + urlparse(url).netloc + new_url
                else : new_url = urljoin(url, new_url)
                if new_url in visited:
                    continue
                if urlparse(new_url).netloc == dom:
                    dl_image(args, new_url, depth - 1)
    return


def main():

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url to scrap")
    parser.add_argument("-p", dest="path", type=str, default="./data/", required=False, help="dir where to save imgs")
    parser.add_argument("-r", dest="recurcive", action="store_true", required=False, help="to download imgs recurcively")
    parser.add_argument("-l", dest="depth", type=check_positive, default=5, required=False, help="set recurcive depth")
    args = parser.parse_args()
    print(args.__dict__)

    # check directory path
    if os.path.exists(args.path):
        shutil.rmtree(args.path, ignore_errors=True)
        os.makedirs(args.path)
    else:
        os.makedirs(args.path)

    # run images scrapping
    dl_image(args, args.url, args.depth)


if __name__ == "__main__":
    main()
