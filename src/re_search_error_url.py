import logging
import time
from multiprocessing.pool import Pool

from const import file_location, count_process
from http_request import sc_ftqq_send_message
from search_vip_resource import traverse_one_book, save_chapter_id

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("re_search_vip")


def re_search_book():
    pool = Pool(count_process)
    with open(file_location + "saveErrorBook.txt", 'r', encoding="utf-8") as save_error_book_file:
        for url in save_error_book_file:
            url = url[:-1]
            try:
                traverse_one_book_result = pool.apply_async(traverse_one_book, args=(url[url.find("books/") + 6:url.find("/chapters/")],))
                if not traverse_one_book_result.get()[0]:
                    raise RuntimeError("遍历结果不正确" + str(traverse_one_book_result.get()))
            except Exception as e:
                LOGGER.error(e)
    pool.close()
    pool.join()
    save_chapter_id()


if __name__ == '__main__':
    start_time = time.time()
    re_search_book()
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
    sc_ftqq_send_message("再请求成功", "耗时" + str(seconds) + "秒")
