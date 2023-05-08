# coding=utf-8
# @Software : PyCharm
# @Time : 2023/4/28 17:50
# @File : get_into.py
# @Python Version : Python3.10
# @Core :

import json
import os


def main():
    data = {
        "0": {
            "url": "https://www.pttime.org/attendance.php",
            "header": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Alt-Used": "www.pttime.org",
                "Connection": "close",
                "Cookie": "你的Cookie",
                "Host": "www.pttime.org",
                "Referer": "你的Referer",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
            }
        },
        "1": {
            "url": "https://www.hddolby.com/attendance.php",
            "header": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Alt-Used": "www.hddolby.com",
                "Connection": "close",
                "Cookie": "你的Cookie",
                "Host": "www.hddolby.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
            }
        },
        "2": {
            "url": "https://hdfans.org/attendance.php",
            "header": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Alt-Used": "hdfans.org",
                "Connection": "close",
                "Cookie": "你的Cookie",
                "Host": "hdfans.org",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "TE": "trailers",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-J7108 Build/MMB29K)"
                              " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108"
                              " UCBrowser/11.9.7.977 Mobile Safari/537.36"
            }
        }
    }

    directory_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(directory_path + '/data'):
        pass
    else:
        os.mkdir(directory_path + '/data')
    filename = directory_path + '/data' + '/data.json'
    content = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
    except IOError:
        pass
    content.update(data)

    with open(filename, 'w', encoding='utf-8') as file:
        # file是指使用括号内参数打开文件作为file变量
        json.dump(content, file, indent=4, ensure_ascii=False)
        file.write('\n')


if __name__ == "__main__":
    main()
