import logging
import os

from const import domain_zhuishushenqi, domain_qidian, domain_xxsy
from http_request import use_soup

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger("judge_free")


# True为免费，False为收费
def judge_free(url):
    if not isinstance(url, str):
        return True
    LOGGER.info("进程 %s 正在judge page:" % os.getpid() + url)
    if domain_zhuishushenqi in url:
        return judge_zhuishushenqi(url)
    elif domain_qidian in url:
        return judge_qidian(url)
    elif domain_xxsy in url:
        return judge_xxsy(url)
    else:
        # 不是潇湘书院、起点、追书神器站点的书，不作检查
        return True


# True为免费，False为收费
def judge_zhuishushenqi(url):
    # 包含该class就是收费章节

    return None is use_soup(url).find(attrs={'class': 'is-vip'})


# True为免费，False为收费
def judge_qidian(url):
    # 起点站的小说如果url里包含vip那就一定是vip章节，就不用抓取页面了
    if "vip" in url:
        return False
    else:
        # 包含该class就是收费章节
        return None is use_soup(url).find(attrs={'class': 'btn-primary read-btn-vip-login jsLoginRss'})


# True为免费，False为收费
def judge_xxsy(url):
    # 不包含该class就是收费章节
    return None is not use_soup(url).find(attrs={'class': 'chapter-main'})
