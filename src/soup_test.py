import unittest

from http_request import delete_one_book_chapter_by_url
from judge_free import judge_free


class TestSoup(unittest.TestCase):
    # False为收费not free
    def test_zhuishushenqi_not_free(self):
        url = 'https://www.zhuishushenqi.com/book/53192eaba2534b963b019bb0/129.html'
        self.assertFalse(judge_free(url))

    # True为免费free
    def test_zhuishushenqi_free(self):
        url = 'https://www.zhuishushenqi.com/book/53192eaba2534b963b019bb0/10.html'
        self.assertTrue(judge_free(url))

    # False为收费not free
    def test_qidian_not_free(self):
        url = 'https://m.qidian.com/book/1693876/33468532'
        self.assertFalse(judge_free(url))

    # True为免费free
    def test_qidian_free(self):
        url = 'https://m.qidian.com/book/1693876/29018852'
        self.assertTrue(judge_free(url))

    # False为收费not free
    def test_xxsy_not_free(self):
        url = 'https://www.xxsy.net/chapter/8559315.html'
        self.assertFalse(judge_free(url))

    # True为免费free
    def test_xxsy_free(self):
        url = 'https://www.xxsy.net/chapter/8427636.html'
        self.assertTrue(judge_free(url))

    # 不在检测范围中的url
    def test_not_in_range(self):
        url = 'https://www.baidu.com'
        self.assertTrue(judge_free(url))

    # 非法参数
    def test_illegal_parameter(self):
        url = 1
        self.assertTrue(judge_free(url))

    # 从url中取出chapterId
    def test_string(self):
        url = "test-api.lemonovel.com/v1/books/26a5c9ce-f6ae-492c-b1c6-754207738409/chapters/73eb877f-43b7-4727-b05c-0ef31e5b3e8d"
        print(url[url.find("chapters") + 9:])

    # 删除请求测试
    def test_delete(self):
        url = "https://test-api.lemonovel.com:443/v1/books/26a5c9ce-f6ae-492c-b1c6-754207738409/chapters/7261c458-d6e1-4048-813f-ba70464f0141"
        self.assertTrue(delete_one_book_chapter_by_url(url))

    # 测试url截取,去掉读文件时附带的最后一个\n
    def test_url_sub(self):
        url = "https://test-api.lemonovel.com:443/v1/books/26a5c9ce-f6ae-492c-b1c6-754207738409/chapters/7261c458-d6e1-4048-813f-ba70464f0141\n"
        print((url[:-1]))
        url = url.replace("https://test-api.lemonovel.com:443", "http://192.168.0.135")
        print(url)
        url = "api.lemonovel.com/v1/books/34f8f3b6-cc52-4245-929e-4a118c1e1772/chapters/"
        print(url[url.find("books/") + 6:url.find("/chapters/")])
