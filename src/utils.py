from urllib3 import *
from re import *
from ComicGirlPictureSpider import Crawl

http = PoolManager()
disable_warnings()
curPage = 1
END_FALG = False

def changePage(page=None):
    global URL, curPage
    if page == None:
        curPage += 1
        URL = 'https://konachan.net/post?page=' + str(curPage) + '&tags='
        return
    if type(page) == type(1):
        curPage += page
        URL = 'https://konachan.net/post?page=' + str(curPage) + '&tags='


def getList(tag):
    URL = 'https://konachan.net/post?page=' + str(curPage) + '&tags=' + tag
    RES = http.request('GET', URL)
    HTML = RES.data.decode('utf-8')
    URLList = []
    R = search(r'<ul[^>]*post-list-posts[^>]+(?:.|\n)*?</ul>', HTML).group(0)
    RList = findall(r'<a[^>]*thumb.*?>', R)
    begin = len('\<a class=\"thumb\" href=\"')
    end = len('\" \>')
    for r in RList:
        URLList.append('https://konachan.net/' + r[begin:len(r) - end + 1])
    return URLList


def auto_spider(tag):
    URLList = getList(tag)
    for url in URLList:
        if END_FALG:
            print('End Spider')
            return
        if 0 == Crawl(url):
            print('success')
    URLList[:] = []
    changePage()


def run(tag, itor):
    for i in range(itor):
        auto_spider(tag)
