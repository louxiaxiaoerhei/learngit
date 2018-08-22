from multiprocessing.pool import Pool

import requests, os, re, time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '__guid=155324093.3079581561575064000.1518236789006.181; monitor_count=80',
    'Host': 'www.mmjpg.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}


def get_page_url(i):
    pass


def parser_page(page_url):
    try:
        page_html = requests.get(page_url, headers=HEADERS)
        if page_html.status_code == 200:
            soup = BeautifulSoup(page_html.content, 'lxml', from_encoding='utf-8')
            mm_urls = soup.select('div.pic > ul > li > a')
            for mm_url in mm_urls:
                yield mm_url['href']
    except RequestException:
        return None


def parser_mmurl(i, mmurl_t):
    return mmurl_t + str(i) + '.jpg'


def get_mmurl_t(mm_url):
    try:
        page_html = requests.get(mm_url, headers=HEADERS)
        if page_html.status_code == 200:
            soup = BeautifulSoup(page_html.content, 'lxml', from_encoding='utf-8')
            mmurl_t = soup.select('#content')[0].a.img['src'][:-5]
            return mmurl_t
    except RequestException:
        return None


def get_mmurl_count(mm_url):
    try:
        page_html = requests.get(mm_url, headers=HEADERS)
        if page_html.status_code == 200:
            soup = BeautifulSoup(page_html.content, 'lxml', from_encoding='utf-8')
            count = int(soup.select('#page')[0].i.next_sibling.get_text())
            return count
    except RequestException:
        return None


def get_mmurl_title(mm_url):
    try:
        page_html = requests.get(mm_url, headers=HEADERS)
        if page_html.status_code == 200:
            soup = BeautifulSoup(page_html.content, 'lxml', from_encoding='utf-8')
            title = soup.select('body > div.main > div.article > h2')[0].get_text()
            return title
    except RequestException:
        return None


def write_img(i, url, path):
    with open(path + '\\' + str(1000 + i) + '.jpg', 'wb') as f:
        f.write(requests.get(url, headers=HEADERS).content)


header2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.mmjpg.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def main(num):
    site = 'http://www.mmjpg.com/mm/'
    mm_url = site + str(num)
    print(mm_url)
    count = get_mmurl_count(mm_url)
    print(count)
    title = get_mmurl_title(mm_url)
    print(title)
    mmurl_t = get_mmurl_t(mm_url)
    # print(mmurl_t)
    path = 'D:\\Python\\爬虫\\图片下载\\' + title
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    for i in range(1, count + 1):
        imgs = mmurl_t + str(i) + '.jpg'
        # print(imgs)
        with open(path + '\\' + str((1000 + i)) + '.jpg', 'wb') as f:
            f.write(requests.get(imgs, headers=header2).content)


if __name__ == '__main__':
    s = time.time()
    # for i in range(1242,1256):
    #     main(i)
    # main(1242,1256)
    pool = Pool()
    pool.map(main, [i for i in range(1242, 1256)])

    e = time.time()
    print(e - s)