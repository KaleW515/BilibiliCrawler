import requests
from bs4 import BeautifulSoup
import re
import json
import time
import pandas as pd


def get_aids():
    id = [1, 168, 3, 129, 4, 36, 188, 160, 119, 155, 5, 181]
    aids = []
    for i in id:
        useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        header = {
            'referer': 'no-referrer-when-downgrade',
            'user-agent': useragent,
        }
        posturl = 'https://www.bilibili.com/ranking/all/'+str(i)+'/0/3'
        r = requests.get(posturl, headers=header)
        soup = BeautifulSoup(r.text, 'lxml')
        data = soup.select(
            '#app > div.b-page-body > div > div.rank-container > div.rank-body > div.rank-list-wrap > ul > li > div.content')
        for item in data:
            ul = item.find_all('a')
            for a in ul:
                aids.append(re.findall(r"\d\d\d\d\d\d\d\d", a.get("href")))
                break
    return aids


def get_data(aids):
    header = {
        'referer': 'no-referrer-when-downgrade',
        'User-Agent': 'BiLiBiLi WP Client/1.0.0 (wk@kalew515.com)',
    }
    result = []
    for aid in aids:
        url = 'http://api.bilibili.com/archive_stat/stat?aid=' + str(aid)[2:-2]
        try:
            res = requests.get(url, headers=header, timeout=6).json()
            time.sleep(0.6)
            data = res['data']
            msg = {
                'aid': data['aid'],        # 视频编号
                'view': data['view'],       # 播放量
                'danmaku': data['danmaku'],    # 弹幕数
                'reply': data['reply'],      # 评论数
                'favorite': data['favorite'],   # 收藏数
                'coin': data['coin'],       # 硬币数
                'share': data['share'],       # 分享数
                'like': data['like'],      # 点赞数
                'dislike': data['dislike'],  # 不喜欢
                'no_reprint': data['no_reprint'],  # 是否原创
                'copyright': data['copyright']  # 著作权保护
            }
            result.append(msg)
        except:
            pass
    return result


def write_csv(msg):
    column = ['aid', 'view', 'danmaku', 'reply', 'favorite', 'coin',
              'share', 'like', 'dislike', 'no_reprint', 'copyright']
    data = pd.DataFrame(columns=column, data=msg)
    data.to_csv('msg.csv', index=False)


if __name__ == '__main__':
    aids = get_aids()
    msg = get_data(aids)
    write_csv(msg)
