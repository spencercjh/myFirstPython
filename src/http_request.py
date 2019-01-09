import http.client

import requests
from bs4 import BeautifulSoup

from const import server_host, get_all_books_url, get_one_book_all_chapters_url_front, \
    get_one_book_all_chapters_url_end, admin_token, success_code


def get_all_books():
    conn = http.client.HTTPSConnection(server_host)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    conn.request("GET", get_all_books_url, payload, headers)
    return conn.getresponse().read().decode("utf-8")


def get_one_book_all_chapters(book_id):
    conn = http.client.HTTPSConnection(server_host)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    conn.request("GET", get_one_book_all_chapters_url_front + book_id + get_one_book_all_chapters_url_end, payload,
                 headers)
    return conn.getresponse().read().decode("utf-8")


def use_soup(url):
    response_html = requests.request("GET", url).text
    soup = BeautifulSoup(response_html, 'lxml')
    return soup


def delete_one_book_chapter_by_url(url):
    headers = {"token": admin_token}
    response = requests.request(method="DELETE", url=url, headers=headers)
    return response.status_code == success_code, str(response.content)
