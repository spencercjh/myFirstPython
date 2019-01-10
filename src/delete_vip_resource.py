import logging
import time

from const import file_location
from http_request import delete_one_book_chapter_by_url, sc_ftqq_send_message

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("delete_vip")
handler = logging.FileHandler("../log/delete_vip.log")
LOGGER.addHandler(handler)


# 替换saveUrl.txt中的url主机
def replace_url_front(url):
    if isinstance(url, str):
        new_url = url.replace("api.lemonovel.com", "http://192.168.0.136")
        return new_url


def delete_all_vip_chapters():
    error_url_list = []
    with open(file_location + 'saveUrl.txt', 'r', encoding='utf-8') as save_url_file:
        for url in save_url_file:
            url = url[:-1]
            url = replace_url_front(url)
            try:
                delete_result, content = delete_one_book_chapter_by_url(url)
                logging.info(content)
            except Exception as e:
                LOGGER.error(e)
                delete_result = False
            if delete_result:
                logging.info("请求成功" + url)
            else:
                logging.error("请求失败" + url)
                error_url_list.append(url)
    if error_url_list:
        with open(file_location + 'deleteErrorUrl.txt', 'a', encoding='utf-8') as delete_error_url_file:
            delete_error_url_file.write("\n".join(error_url_list))


if __name__ == '__main__':
    start_time = time.time()
    delete_all_vip_chapters()
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
    sc_ftqq_send_message("删除请求执行完成", "耗时" + str(seconds) + "秒")
