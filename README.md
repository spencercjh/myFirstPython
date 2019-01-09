# 删掉所有的黄页 VIP 章节脚本

## 文件说明

src #python源代码文件夹

product #生产环境结果信息文件夹

test #测试环境结果信息文件夹

log #日志文件夹

const.py    #环境常量

delete_vip_resource.py  #发起删除请求

http_request.py #所有的网络请求

judge_free.py   #判断章节页面是否有收费元素

re_search_error_url.py  #重新遍历第一次请求时发生错误的图书的章节

search_test.py  #对遍历搜索一本小说所有章节的traverse_one_book函数的单元测试

search_vip_resource.py  #搜索所有图书的所有收费章节

soup_test.py    #对判断章节页面是否有收费元素的judge_free函数的单元测试

## 需求

我们线上系统之前上线了很多书籍的章节数据,因为抓取的是正版来源,
有部分章节是一些VIP章节,需要登录付费后才可以查看,在我们的网页中无法正常使用,所以需要把这些章节下线掉.

主要包括:起点/潇湘书院/追书神器的书籍来源

## 总结 

我发现原来很多书是缺章节的。

所以不能通过简单的免费章节节数+搜索到的收费章节节数=最新章节节数来判断是否正确地搜索了一本书的收费章节；

正确的判断方法是要分别统计免费章节和收费章节，他们的和等不等于获取到的章节JsonArray的length，
等于即表明代码没有问题，执行过程中也没有异常；

若出现了问题，相关信息都在errorTraverseBook.txt中会有记录，
也就是说一发现有这个文件就说明有书出问题了。

上述2个统计结果都在单一进程的单一方法中，不会有多进程通信问题。

程序的性能瓶颈在于网络抓取小说网页，一本小说的免费章节越多，搜索它的进程就越耗时。

判断收费章节的主要方法是judge_free，全覆盖单元测试在soup_test.py中

搜索小说收费章节的主要方法是traverse_one_book，测试在search_test.py中（在网络条件良好的情况下处理异常部分不可能触发，故暂时不能全覆盖单元测试）

测试环境为服务器47.254.22.221 

dependencies:python3.6+,multiprocessing,requests,bs4

运行方法为
```bash
nohup python3 search_vip_resource.py &
```
```bash
nohup python3 delete_vip_resource.py &
```

搜索全部收费章节全程耗时45分钟左右