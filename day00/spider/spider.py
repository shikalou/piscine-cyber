import sys
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# def check_arg(tab: list) -> str:
#     ret = ""
#     for arg in range(0, len(tab)):
#         if arg.startswith("-"):
#             if ('p' in tab[arg]):
#                 tab[arg+=1]


def main():

    # site = check_arg(sys.argv)
    site = sys.argv[1]
    path = './data/'

# check download path
    if not os.path.exists(path):
        os.makedirs(path)

# DL PHOTO TO PATH
    rep = requests.get(site)
    soup = BeautifulSoup(rep.text, 'html.parser')
    imgs = soup.find_all('img')

    for img in imgs:
        src = img['src']
        if not src.startswith('http'):
            src = urljoin(site, src)
        filename = os.path.join(path, src.split('/')[-1])
        with open(filename, 'wb') as ret:
            res = requests.get(src)
            ret.write(res.content)

if __name__ == "__main__":
    main()


# • Option -r : recursively downloads the images in a URL received as a parameter.
# • Option -r -l [N] : indicates the maximum depth level of the recursive download.
# If not indicated, it will be 5.
# • Option -p [PATH] : indicates the path where the downloaded files will be saved.
# If not specified, ./data/ will be used.
