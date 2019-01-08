import http.client
import json
import os
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup


def get_all_books():
    conn = http.client.HTTPSConnection("test-api.lemonovel.com")
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    conn.request("GET", "/v1/books?page=0&pageSize=10000", payload, headers)
    return conn.getresponse().read().decode("utf-8")


def get_one_book_all_chapters(book_id):
    conn = http.client.HTTPSConnection("test-api.lemonovel.com")
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    conn.request("GET", "/v1/books/" + book_id + "/chapters", payload, headers)
    return conn.getresponse().read().decode("utf-8")


# True表示免费，False表示收费
def judge_free(url):
    if isinstance(url, str):
        print("judge page:" + url + "\n")
        if "zhuishushenqi" in url:
            response_html = requests.request("GET", url).text
            soup = BeautifulSoup(response_html, 'lxml')
            if soup.find(attrs={'class': 'is-vip'}) is not None:
                return False
            else:
                return True
        elif "qidian" in url:
            # 起点站的小说如果url里包含vip那就一定是vip章节，就不用抓取页面了
            if "vip" in url:
                return False
            else:
                response_html = requests.request("GET", url).text
                soup = BeautifulSoup(response_html, 'lxml')
                if soup.find(attrs={'class': 'btn-primary read-btn-vip-login jsLoginRss'}) is not None:
                    return False
                else:
                    return True
        elif "xxsy" in url:
            response_html = requests.request("GET", url).text
            soup = BeautifulSoup(response_html, 'lxml')
            if soup.find(attrs={'class': 'chapter-main'}) is None:
                return False
            else:
                return True
        else:
            # 不是潇湘书院、起点、追书神器站点的书，不作检查
            return True
    else:
        # url不是str类型
        return True


def delete_one_chapter_source(book_id_inner, chapter_id):
    print("进程  %s  存储删除URL：id为" % os.getpid() + book_id_inner + "的id为" + chapter_id + "章节" + "\n")
    url = str("https://test-api.lemonovel.com/v1/books/" + book_id_inner + "/chapters/" + chapter_id)
    print(url)
    with open('saveUrl.txt', 'a', encoding="utf-8") as save_url_file:
        save_url_file.write(url + "\n")


def traverse_one_book(book_id_inner):
    print("开始遍历图书" + book_id_inner + "\n")
    try:
        one_book_all_chapters_result = get_one_book_all_chapters(book_id_inner)
    except TimeoutError:
        while one_book_all_chapters_result is None:
            one_book_all_chapters_result = get_one_book_all_chapters(book_id_inner)
    one_book_all_chapters_json_result = json.loads(one_book_all_chapters_result)
    one_book_all_chapters = one_book_all_chapters_json_result['data']
    previous = False
    for chapter in one_book_all_chapters:
        zh_source_url = chapter['zhSourceURL']
        chapter_id = chapter['id']
        print("开始遍历图书" + book_id_inner + "的章节" + chapter_id + "\n")
        # url判空
        if zh_source_url is None or len(zh_source_url) == 0:
            continue
        # 如果是收费章节，就删除对应的网站资源，如果前一章是收费章节，那当前章节就一定是收费章节
        if previous:
            delete_one_chapter_source(book_id_inner, chapter_id)
        elif judge_free(zh_source_url) is False:
            previous = True
            delete_one_chapter_source(book_id_inner, chapter_id)


def main():
    try:
        all_books_http_result = get_all_books()
    except TimeoutError:
        # 超时重试
        while all_books_http_result is None:
            all_books_http_result = get_all_books()
    json_result = json.loads(all_books_http_result)
    all_books = json_result['data']
    print(all_books)
    print("\n")
    book_id_list = []
    # 遍历所有书，获取所有的图书id
    for book in all_books:
        book_id_list.append(book['id'])
        # 遍历所有的图书id，通过每本书的id去获取该书所有章节
    pool = Pool(20)
    for book_id in book_id_list:
        # 遍历某一本书的全部章节
        pool.apply_async(traverse_one_book, args=(book_id,))
    pool.close()
    pool.join()
    print("全部需要删除URL查找成功，请查看saveUrl.txt")


if __name__ == '__main__':
    main()
