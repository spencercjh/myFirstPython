import json
import logging
import os
import time
from multiprocessing import Pool

from const import get_one_book_all_chapters_url_front, server_host, get_one_book_all_chapters_url_end, count_process, \
    file_location
from http_request import get_one_book_all_chapters, get_all_books, sc_ftqq_send_message
from judge_free import judge_free

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
LOGGER = logging.getLogger("search_vip")
handler = logging.FileHandler("../log/search_vip.log")
LOGGER.addHandler(handler)


def save_one_chapter_source(book_id_inner, chapter_id):
    LOGGER.info("进程  %s  存储删除URL：id为" % os.getpid() + book_id_inner + "的id为" + chapter_id + "章节")
    url = str(
        server_host + get_one_book_all_chapters_url_front + book_id_inner + get_one_book_all_chapters_url_end +
        chapter_id)
    with open(file_location + 'saveUrl.txt', 'a', encoding="utf-8") as save_url_file_inner:
        save_url_file_inner.write(url + "\n")


def traverse_one_book(book_id_inner):
    delete_chapter_count = 0
    free_chapter_count = 0
    global one_book_all_chapters_result
    LOGGER.info("开始遍历图书" + book_id_inner)
    try:
        one_book_all_chapters_result = get_one_book_all_chapters(book_id_inner)
    except Exception as e:
        LOGGER.error(e)
        # 某一本书的所有章节请求失败，保存出错的bookId
        LOGGER.error("图书:" + book_id_inner + "章节遍历出错")
        with open(file_location + "saveErrorBook.txt", 'a', encoding="utf-8") as save_error_book_id_file:
            save_error_book_id_file.write(
                server_host + get_one_book_all_chapters_url_front + book_id_inner + get_one_book_all_chapters_url_end + "\n")
    one_book_all_chapters_json_result = json.loads(one_book_all_chapters_result)
    one_book_all_chapters = one_book_all_chapters_json_result['data']
    previous = False
    for chapter in one_book_all_chapters:
        zh_source_url = chapter['zhSourceURL']
        chapter_id = chapter['id']
        chapter_name = chapter['name']
        LOGGER.info("开始遍历图书" + book_id_inner + "的章节" + chapter_id + "章节名:" + chapter_name)
        # url判空
        if None is zh_source_url or 0 == len(zh_source_url):
            free_chapter_count += 1
            continue
        # 如果是收费章节，就删除对应的网站资源，如果前一章是收费章节，那当前章节就一定是收费章节
        try:
            if previous:
                delete_chapter_count += 1
                save_one_chapter_source(book_id_inner, chapter_id)
            elif judge_free(zh_source_url) is False:
                delete_chapter_count += 1
                previous = True
                save_one_chapter_source(book_id_inner, chapter_id)
            else:
                free_chapter_count += 1
        except Exception as e:
            LOGGER.error(e)
            # 某一章的页面请求失败，保存出错的bookId和chapterId
            LOGGER.error("图书:" + book_id_inner + "第" + chapter_id + "章节遍历出错")
            with open(file_location + "saveErrorChapter.txt", 'a', encoding="utf-8") as save_error_book_id_file:
                save_error_book_id_file.write(
                    server_host + get_one_book_all_chapters_url_front + book_id_inner +
                    get_one_book_all_chapters_url_end +
                    chapter_id + "\n")
    return (delete_chapter_count + free_chapter_count) == len(one_book_all_chapters), delete_chapter_count, free_chapter_count, len(
        one_book_all_chapters), book_id_inner


def remove_file():
    try:
        os.remove('../log/search_vip.log')
        os.remove(file_location + 'saveUrl.txt')
        os.remove(file_location + 'saveChapterId.txt')
        os.remove(file_location + "saveErrorChapter.txt")
        os.remove(file_location + "saveErrorBook.txt")
        os.remove(file_location + "errorTraverseBook.txt")
    except Exception as e:
        LOGGER.debug(e)


def search_all_vip_chapter():
    start_time = time.time()
    remove_file()
    global all_books_http_result
    all_books_http_result = []
    try:
        all_books_http_result = get_all_books()
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error("超时，解决网络问题后再起一次！")
    json_result = json.loads(all_books_http_result)
    all_books = json_result['data']
    book_id_list = []
    # 遍历所有书，获取所有的图书id
    for book in all_books:
        book_id_list.append(book['id'])
    # 多进程：一本书一个进程
    pool = Pool(count_process)
    # 遍历所有的图书id，通过每本书的id去获取该书所有章节
    for book_id in book_id_list:
        # 遍历某一本书的全部章节
        traverse_one_book_result = pool.apply_async(traverse_one_book, args=(book_id,))
        if not traverse_one_book_result.get()[0]:
            with open(file_location + "errorTraverseBook.txt", 'a', encoding='utf-8') as error_traverse_book_file:
                error_traverse_book_file.write(str(traverse_one_book_result.get()) + "\n")
            LOGGER.error("遍历结果不正确" + str(traverse_one_book_result.get()))
        else:
            LOGGER.info("图书:" + traverse_one_book_result.get()[4] + "付费章节搜索成功")
    pool.close()
    pool.join()
    LOGGER.info("\n\n全部需要删除URL查找成功")
    save_chapter_id()
    LOGGER.info("\n\n存储chapterId成功")
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
    sc_ftqq_send_message("搜索收费章节完成", "耗时" + str(seconds) + "秒")


def save_chapter_id():
    with open(file_location + 'saveChapterId.txt', 'w', encoding="utf-8") as save_chapter_id_file:
        with open(file_location + 'saveUrl.txt', 'r', encoding="utf-8") as save_url_file_inner:
            for url in save_url_file_inner:
                save_chapter_id_file.write(url[url.find("chapters/") + 9:])


if __name__ == '__main__':
    search_all_vip_chapter()
