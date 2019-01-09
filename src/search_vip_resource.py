import json
import logging
import os
import time
from multiprocessing import Pool

from const import get_one_book_all_chapters_url_front, server_host, get_one_book_all_chapters_url_end, count_process, \
    file_location
from http_request import get_one_book_all_chapters, get_all_books
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
    # save_delete_url_list.append(url)
    # save_chapter_id_list.append(chapter_id)
    with open(file_location + 'saveUrl.txt', 'a', encoding="utf-8") as save_url_file_inner:
        save_url_file_inner.write(url + "\n")


def traverse_one_book(book_id_inner):
    global one_book_all_chapters_result
    LOGGER.info("开始遍历图书" + book_id_inner)
    try:
        one_book_all_chapters_result = get_one_book_all_chapters(book_id_inner)
    except Exception as e:
        LOGGER.error(e)
        # 某一本书的所有章节请求失败，保存出错的bookId
        LOGGER.error("图书:" + book_id_inner + "章节遍历出错")
        # save_error_book_list.append(
        #     server_host + get_one_book_all_chapters_url_front + book_id_inner + get_one_book_all_chapters_url_end)
        with open(file_location + "saveErrorBook.txt", 'a', encoding="utf-8") as save_error_book_id_file:
            save_error_book_id_file.write(
                server_host + get_one_book_all_chapters_url_front + book_id_inner + get_one_book_all_chapters_url_end +
                "\n")
    one_book_all_chapters_json_result = json.loads(one_book_all_chapters_result)
    one_book_all_chapters = one_book_all_chapters_json_result['data']
    previous = False
    for chapter in one_book_all_chapters:
        zh_source_url = chapter['zhSourceURL']
        chapter_id = chapter['id']
        LOGGER.info("开始遍历图书" + book_id_inner + "的章节" + chapter_id)
        # url判空
        if zh_source_url is None or len(zh_source_url) == 0:
            continue
        # 如果是收费章节，就删除对应的网站资源，如果前一章是收费章节，那当前章节就一定是收费章节
        try:
            if previous:
                save_one_chapter_source(book_id_inner, chapter_id)
            elif judge_free(zh_source_url) is False:
                previous = True
                save_one_chapter_source(book_id_inner, chapter_id)
        except Exception as e:
            LOGGER.error(e)
            # 某一章的页面请求失败，保存出错的bookId和chapterId
            LOGGER.error("图书:" + book_id_inner + "第" + chapter_id + "章节遍历出错")
            # save_error_book_chapter_list.append(
            #     server_host + get_one_book_all_chapters_url_front + book_id_inner +
            #     get_one_book_all_chapters_url_end +
            #     chapter_id)
            with open(file_location + "saveErrorChapter.txt", 'a', encoding="utf-8") as save_error_book_id_file:
                save_error_book_id_file.write(
                    server_host + get_one_book_all_chapters_url_front + book_id_inner +
                    get_one_book_all_chapters_url_end +
                    chapter_id + "\n")


def main():
    start_time = time.time()
    global all_books_http_result
    # global save_delete_url_list, save_chapter_id_list, save_error_book_list, save_error_book_chapter_list
    all_books_http_result = []
    # save_delete_url_list = multiprocessing.Array("save_delete_url_list", list())
    # save_chapter_id_list = multiprocessing.Array("save_chapter_id_list", list())
    # save_error_book_list = multiprocessing.Array("save_error_book_list", list())
    # save_error_book_chapter_list = multiprocessing.Array("save_error_book_chapter_list", list())
    try:
        all_books_http_result = get_all_books()
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error("超时，解决网络问题后再起一次！")
    json_result = json.loads(all_books_http_result)
    all_books = json_result['data']
    LOGGER.info(all_books)
    book_id_list = []
    # 遍历所有书，获取所有的图书id
    for book in all_books:
        book_id_list.append(book['id'])
    # 多进程：一本书即一个进程
    pool = Pool(count_process)
    # 遍历所有的图书id，通过每本书的id去获取该书所有章节
    for book_id in book_id_list:
        # 遍历某一本书的全部章节
        pool.apply_async(traverse_one_book, args=(book_id,))
    pool.close()
    pool.join()
    LOGGER.info("\n\n全部需要删除URL查找成功")
    saveChapterId()
    LOGGER.info("\n\n存储chapterId成功")
    seconds, minutes, hours = int(time.time() - start_time), 0, 0
    LOGGER.info("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))


# def save_file():
#     with open('../saveUrl.txt', 'a', encoding="utf-8") as save_url_file:
#         save_url_file.write("\n".join(save_delete_url_list))
#     with open('../saveChapterId.txt', 'a', encoding="utf-8") as save_chapter_id_file:
#         save_chapter_id_file.write("[")
#         save_chapter_id_file.write(",\n".join(save_chapter_id_list))
#         save_chapter_id_file.write("]")
#     with open("../saveErrorBook.txt", 'a', encoding="utf-8") as save_error_book_id_file:
#         save_error_book_id_file.write("\n".join(save_error_book_list))
#     with open("../saveErrorChapter.txt", 'a', encoding="utf-8") as save_error_book_id_file:
#         save_error_book_id_file.write("\n".join(save_error_book_chapter_list))

def saveChapterId():
    with open(file_location + 'saveChapterId.txt', 'w', encoding="utf-8") as save_chapter_id_file:
        with open(file_location + 'saveUrl.txt', 'r', encoding="utf-8") as save_url_file_inner:
            for url in save_url_file_inner:
                save_chapter_id_file.write(url[url.find("chapters/") + 9:])


if __name__ == '__main__':
    main()
