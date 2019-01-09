import unittest

from search_vip_resource import traverse_one_book, remove_file


class TestSoup(unittest.TestCase):

    def test_search(self):
        test_book_id = '8a646ae5-4d11-48cf-b29f-e0575618c641'
        remove_file()
        result = traverse_one_book(test_book_id)
        print(result)
        self.assertTrue(result[0])


if __name__ == '__main__':
    unittest.main()
