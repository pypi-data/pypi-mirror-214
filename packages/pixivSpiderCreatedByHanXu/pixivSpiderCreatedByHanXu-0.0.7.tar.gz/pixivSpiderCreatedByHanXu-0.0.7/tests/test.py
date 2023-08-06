import urllib.request
def percentage(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = a * b / c
    if per > 100 :
        per = 100
    print ("{:.2%}".format(per),end=" ")

the_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            "referer": "https://www.pixiv.net/",
        }
test_url="https://i.pximg.net/img-master/img/2019/05/22/00/00/29/74841799_p0_master1200.jpg"


# opener = urllib.request.build_opener()
# opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48'),
#                      ("referer", "https://www.pixiv.net/"),]
# urllib.request.install_opener(opener)
urllib.request.urlretrieve(url=test_url,filename="1.jpg",reporthook=percentage)