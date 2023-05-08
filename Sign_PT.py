# coding=utf-8
# @Software : PyCharm
# @Time : 2023/4/28 15:21
# @File : Sign_PT.py
# @Python Version : Python3.10
# @Core : 已有的三个PT站只要访问attendance.php页面即视为签到成功，之后可以保存签到页面内容并发送通知.使用前请先运行get_into.py

import datetime
import json
import os
import re

import requests
from bs4 import BeautifulSoup

raw = None
code = None


def log(data, path):
    # 获取简易日志
    directory_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(directory_path + '/log'):
        pass
    else:
        os.mkdir(directory_path + '/log')
    filename = directory_path + '/log' + '/' + path
    renew = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            renew = json.load(file)
    except IOError:
        # 假如json文件不存在则报错.
        pass
    renew.update(data)
    with open(filename, 'w', encoding='utf-8') as file:
        # file是指使用括号内参数打开文件作为file变量
        json.dump(renew, file, indent=4, ensure_ascii=False)
        # 缩进，不默认使用ascii码
        file.write('\n')


def sign_pt(url, headers):
    global raw
    global code
    for i in range(1, 10):
        try:
            r = requests.Session().get(url, headers=headers, timeout=300)
            code = r.status_code
            raw = r.text
        except requests.exceptions.ConnectTimeout:
            return False
            pass
        try:
            if code == 200:
                return True
        except code != 200:
            return False
            pass


def re_HDFans(cont):
    soup = BeautifulSoup(cont, 'html.parser')
    data = str(soup.select('td.bottom:nth-child(1) > span:nth-child(1)'))
    data_sp = data.strip().split(']')
    # 魔力值
    magicpower_raw = data_sp[4].strip().split('<a')
    magicpower = magicpower_raw[0].strip().split(' ')[1]
    # 获得数
    gain = re.search(r'签到已得\d+', data_sp[4]).group(0)
    # 分享率
    ratio_raw = data_sp[7].strip().split('</font> ')
    ratio = ratio_raw[1].strip().split(' ')[0]
    # 上传量
    uploads = ratio_raw[2].strip().split(' ')[0] + ratio_raw[2].strip().split(' ')[1]
    # 下载量
    downloads = ratio_raw[3].strip().split(' ')[0] + ratio_raw[3].strip().split(' ')[1]

    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    info = {
        current_time:
            {
                "魔力值": magicpower,
                "获得数": gain,
                "上传量": uploads,
                "下载量": downloads,
                "分享率": ratio
            }
    }
    return info


def re_HDDolby(cont):
    soup = BeautifulSoup(cont, 'html.parser')
    data = str(soup.select('td.bottom:nth-child(1) > span:nth-child(1)'))
    data_sp = data.strip().split('</font>')
    # 魔力值
    sp_1 = data_sp[1].strip().split(' ')[2]
    magicpower = sp_1.strip().split('\xa0')[0]
    # 获得数
    gain = re.search(r'签到已得\d+', sp_1).group(0)
    # 分享率
    ratio = data_sp[3].strip().split(' ')[0]
    # 下载量
    downloads = data_sp[5].strip().split(' ')[0]
    # 上传量
    uploads = data_sp[4].strip().split(' ')[0]
    # 做种积分
    points = data_sp[6].strip().split(' ')[0]

    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    info = {
        current_time:
            {
                "魔力值": magicpower,
                "获得数": gain,
                "上传量": uploads,
                "下载量": downloads,
                "分享率": ratio,
                "做种积分": points
            }
    }
    return info


def re_PTTime(cont):
    soup = BeautifulSoup(cont, 'html.parser')
    # 分享率
    ratio_data = str(soup.select('span.mr5:nth-child(1)'))
    ratio_sp = ratio_data.strip().split('</font>')[1]
    ratio = ratio_sp.strip().split('</span>')[0]
    # 下载量
    downloads_data = str(soup.select('span.mr5:nth-child(3)'))
    downloads_sp = downloads_data.strip().split('</font>')[1]
    downloads = downloads_sp.strip().split('</span>')[0]
    # 上传量
    uploads_data = str(soup.select('span.mr5:nth-child(2)'))
    uploads_sp = uploads_data.strip().split('</font>')[1]
    uploads = uploads_sp.strip().split('</span>')[0]
    # 魔力值 获得数
    data = str(soup.select('span.mr5:nth-child(7)'))
    data_sp = data.strip().split('<a')[1]
    magicpower_sp = data_sp.strip().split(' ')[2]
    magicpower = magicpower_sp.strip().split('(')[0]
    gain = re.search(r'获得\d+', magicpower_sp).group(0)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    info = {
        current_time:
            {
                "魔力值": magicpower,
                "获得数": gain,
                "上传量": uploads,
                "下载量": downloads,
                "分享率": ratio
            }
    }
    return info


def main():
    directory_path = os.path.dirname(os.path.abspath(__file__))
    filename = directory_path + '/data/data.json'
    with open(filename, 'r', encoding='utf-8') as file:
        content = json.load(file)

    failed_pt = []
    successnu = 0
    failnu = 0

    for i in range(0, 3):
        url = content[f'{i}']['url']
        headers = content[f'{i}']['header']
        t = sign_pt(url=url, headers=headers)

        if i == 0 and t:
            successnu += 1
            info = re_PTTime(cont=raw)
            log(info, path='PTTime_log.json')
        elif i == 0 and not t:
            failnu += 1
            failed_pt.append('PTTime')

        elif i == 1 and t:
            successnu += 1
            info = re_HDDolby(cont=raw)
            log(info, path='HDDolby_log.json')
        elif i == 1 and not t:
            failnu += 1
            failed_pt.append('HDDolby')

        elif i == 2 and t:
            successnu += 1
            info = re_HDFans(cont=raw)
            log(info, path='HDFans_log.json')
        elif i == 2 and not t:
            failnu += 1
            failed_pt.append('HDFans')

    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    renew = {
        str(current_time): {
            "成功数": successnu,
            "失败数": failnu,
            "签到失败目录": failed_pt
        }
    }
    log(data=renew, path='log.json')


if __name__ == "__main__":
    main()
