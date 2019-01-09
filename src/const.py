mode = 0
if mode == 0:
    server_host = "test-api.lemonovel.com"
    file_location = "../test/"
elif mode == 1:
    server_host = "api.lemonovel.com"
    file_location = "../product/"
get_all_books_url = "/v1/books?page=0&pageSize=10000"
get_one_book_all_chapters_url_front = "/v1/books/"
get_one_book_all_chapters_url_end = "/chapters/"
domain_zhuishushenqi = "zhuishushenqi"
domain_qidian = "qidian"
domain_xxsy = "xxsy"
admin_token = "d80f98afa67e107022d8ac48fae7f50e47ee5df4a92706027906c149a8943b81"
success_code = 200
count_process = 20
