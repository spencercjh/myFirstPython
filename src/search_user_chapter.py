import csv
import logging
import time

from const import file_location
from http_request import sc_ftqq_send_message
from judge_free import judge_free

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("search_user_chapter")


def judge_user_translation(entry):
    zh_source_url = entry[5]
    try:
        if None is not zh_source_url and 0 != len(zh_source_url):
            if not judge_free(zh_source_url):
                LOGGER.info("写入" + str(entry))
                id_list.append(entry[0])
            return True
    except Exception as e:
        LOGGER.error(str(entry) + "请求失败:" + str(e))
        return False


def read_csv():
    global id_list
    id_list = []
    error_entry_list = []
    user_translations = open(file_location + 'user_translations.csv', encoding='utf-8')
    csv_reader = csv.reader(user_translations)
    csv_data = list(csv_reader)
    for entry in csv_data:
        if not judge_user_translation(entry):
            error_entry_list.append(entry)
    # 没有请求成功的再试一次
    for entry in error_entry_list:
        if judge_user_translation(entry):
            error_entry_list.remove(entry)
    with open(file_location + 'user_translations_id.txt', 'w', encoding='utf-8') as id_file:
        id_file.write("\n".join(id_list))


if __name__ == '__main__':
    start_time = time.time()
    read_csv()
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
    sc_ftqq_send_message("查找含有收费章节的用户翻译信息id", "耗时" + str(seconds) + "秒")
