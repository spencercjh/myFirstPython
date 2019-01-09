import logging
import time

from const import file_location
from http_request import delete_one_book_chapter_by_url

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("delete_vip")


def delete_all_vip_chapters():
    error_url_list = []
    with open(file_location + 'saveUrl.txt', 'r', encoding='utf-8') as save_url_file:
        for url in save_url_file:
            url = url[:-1]
            delete_result = delete_one_book_chapter_by_url(url)
            if delete_result:
                logging.info("请求成功" + url)
            else:
                logging.error("请求失败" + url)
                error_url_list.append(url)
    with open(file_location + 'deleteErrorUrl.txt', 'a', encoding='utf-8') as delete_error_url_file:
        delete_error_url_file.write("\n".join(error_url_list))


if __name__ == '__main__':
    start_time = time.time()
    delete_all_vip_chapters()
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
