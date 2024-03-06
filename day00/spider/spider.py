import sys
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Arg():
    def __init__(self) -> None:
        self.p = "./data/"
        self.l = 5
        self.l_b = False
        self.r = False
        self.site = ""
        self.visited = []


    def init_arg(self, tab: list):
        try:
            for i in range(0, len(tab)):
                if tab[i].startswith("-"):
                    if ('p' in tab[i]):
                        self.p = tab[i+1]
                    elif ('r' in tab[i]):
                        self.r = True
                    elif ('l' in tab[i]):
                        self.l_b = True
                        self.l = int(tab[i+1])
                if tab[i].startswith("http"):
                    self.site = tab[i]
            if self.l_b is True and self.r is False:
                raise Exception("cant initiat -l without -r")
            if self.site == "":
                raise Exception("wrong website url")
        except Exception as msg:
            print(msg)
            sys.exit()


def dl_image(arg: Arg, site: str, depth: int=0):
    rep = requests.get(site)
    arg.visited.append(site)
    soup = BeautifulSoup(rep.text, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        src = img['src']
        if not src.startswith('http'):
            src = urljoin(site, src)
        filename = os.path.join(arg.p, src.split('/')[-1])
        with open(filename, 'wb') as ret:
            res = requests.get(src)
            ret.write(res.content)
    if (arg.r is True):
        if (depth < arg.l):
            links = soup.find_all('a', href=True)
            for link in links:
                url = link['href']
                print(url)
        else:
            print("max l reached")
            return

def main():
    arg = Arg()
    try:
        arg.init_arg(sys.argv)
    except Exception as msg:
        print(msg)
        sys.exit()
    # print(arg.__dict__)
    
    try:# check download path
        if not os.path.exists(arg.p):
            os.makedirs(arg.p)
        dl_image(arg, arg.site)# DL PHOTO TO PATH
    except:
        print("Error")
if __name__ == "__main__":
    main()

# python spider.py [URL]
# python spider.py -r [URL]
# python spider.py -r -l 6 [URL]
# python spider.py -p [PATH] [URL]

# • Option -r : recursively downloads the images in a URL received as a parameter.
# • Option -r -l [N] : indicates the maximum depth level of the recursive download.
# If not indicated, it will be 5.
# • Option -p [PATH] : indicates the path where the downloaded files will be saved.
# If not specified, ./data/ will be used.
