import unittest

import requests
from bs4 import BeautifulSoup


# 测试抓取页面内容的判断逻辑
class TestSoup(unittest.TestCase):
    def test_zhuishushenqi_not_free(self):
        url = 'https://www.zhuishushenqi.com/book/53192eaba2534b963b019bb0/129.html'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertTrue(soup.find(attrs={'class': 'is-vip'}) is not None)

    def test_zhuishushenqi_free(self):
        url = 'https://www.zhuishushenqi.com/book/53192eaba2534b963b019bb0/10.html'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertFalse(soup.find(attrs={'class': 'is-vip'}) is not None)

    def test_qidian_not_free(self):
        url = 'https://m.qidian.com/book/1693876/33468532'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertTrue(soup.find(attrs={'class': 'btn-primary read-btn-vip-login jsLoginRss'}) is not None)

    def test_qidian_free(self):
        url = 'https://m.qidian.com/book/1693876/29018852'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertFalse(soup.find(attrs={'class': 'btn-primary read-btn-vip-login jsLoginRss'}) is not None)

    def test_xxsy_not_free(self):
        url = 'https://www.xxsy.net/chapter/8559315.html'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertTrue(soup.find(attrs={'class': 'chapter-main'}) is None)

    def test_xxsy_free(self):
        url = 'https://www.xxsy.net/chapter/8427636.html'
        responseHtml = requests.request("GET", url).text
        soup = BeautifulSoup(responseHtml, 'lxml')
        self.assertFalse(soup.find(attrs={'class': 'chapter-main'}) is None)
