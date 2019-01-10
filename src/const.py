import requests

mode = 1  # 1表示生产 0表示测试
env = 0  # 1表示内网服务器 0表示我的电脑
if mode == 0:
    if env == 0:
        server_host = "test-api.lemonovel.com"
    elif env == 1:
        server_host = "192.168.0.135"
    file_location = "../test/"
elif mode == 1:
    if env == 0:
        server_host = "api.lemonovel.com"
    elif env == 1:
        server_host = "192.168.0.136"
    file_location = "../product/"
get_all_books_url = "/v1/books?page=0&pageSize=10000"
get_one_book_all_chapters_url_front = "/v1/books/"
get_one_book_all_chapters_url_end = "/chapters/"
domain_zhuishushenqi = "zhuishushenqi"
domain_qidian = "qidian"
domain_xxsy = "xxsy"
admin_token = "d80f98afa67e107022d8ac48fae7f50e47ee5df4a92706027906c149a8943b81"
success_code = requests.codes.ok
count_process = 10

sc_key = 'SCU37675T0c48d22fd4519a967d9f95767fe450f05c1388b9ee394'
sc_url = 'https://sc.ftqq.com/%s.send' % sc_key
