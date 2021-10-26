

import requests
import os
import re
from bs4 import BeautifulSoup
import datetime

img_name_style = r'{id}by_morisa.jpg'
save_path = r'./save'

headers = {
    'Referer': 'http://konachan.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def CreateDefaultIni():
    global save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)


def CheckUrl(target_url):
    if not target_url or target_url == '':
        return False
    if re.compile(r'^(http://|https://)?konachan\.(com|net)/post/show/\d+').search(target_url) is None:
        return False
    return True


def GetHTMLResponse(target_url):
    try:
        target_html_res = requests.get(target_url, headers=headers)
        if str(target_html_res.status_code) != '200':
            print(target_url + '\nConnect Error, code is : ' + str(target_html_res.status_code))
            return None
    except:
        print(target_url + '\nConnect Error, need VPN')
        return None
    return target_html_res


def GetImageName(soup):
    id_str = soup.find(text=re.compile('^Id: \d+'))
    if id_str is not None:
        name = re.compile('\d+').search(id_str).group()

    else:
        name = datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')
    return img_name_style.format(id=name)


def GetImageHrefAndInfo(soup):
    # tag = soup.find('a', attrs={'class': 'original-file-changed'})
    tag = soup.find(
        lambda m_tag: m_tag.name == 'a' and m_tag.get('class') == ['original-file-changed'] or m_tag.get('class') == [
            'original-file-unchanged'])
    href = None
    info = None
    if tag is not None:
        href = tag['href']
        info = re.compile('\(.+\)').search(tag.text).group()
    return href, info


def Crawl(img_main_url):
    CreateDefaultIni()
    img_main_res = GetHTMLResponse(img_main_url)
    if img_main_res is None:
        return -1
    img_main_soup = BeautifulSoup(img_main_res.text, 'lxml')
    img_name = GetImageName(img_main_soup)
    if os.path.exists(save_path + '/' + img_name):
        print(img_name + ' existed')
        return 1
    img_href, img_info = GetImageHrefAndInfo(img_main_soup)
    if img_info is not None:
        print('Downloading ' + img_name + img_info)
    else:
        print('Downloading ' + img_name)
    if img_href is None:
        print('NOT FOUND')
        return -1
    img_href_res = GetHTMLResponse(img_href)
    if img_href_res is None:
        return -1
    img_file = open(save_path + '/' + img_name, 'wb')
    print(save_path + '/' + img_name)
    img_file.write(img_href_res.content)
    img_file.close()
    return 0

