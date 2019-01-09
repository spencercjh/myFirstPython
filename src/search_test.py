import logging

from search_vip_resource import traverse_one_book

test_book_id = 'b60b5cb4-9bea-4944-8bc2-1b31ef5f15bd'
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("search_vip")
handler = logging.FileHandler("../log/test_search.log")
LOGGER.addHandler(handler)


def test_search():
    traverse_one_book(test_book_id)


if __name__ == '__main__':
    test_search()
