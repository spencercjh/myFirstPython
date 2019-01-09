import unittest

from search_vip_resource import traverse_one_book, remove_file


class TestSoup(unittest.TestCase):

    def test_search(self):
        test_book_id = 'b60b5cb4-9bea-4944-8bc2-1b31ef5f15bd'
        remove_file()
        self.assertTrue(traverse_one_book(test_book_id))
