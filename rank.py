import requests
import urllib
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


def craw():
    day = ['3']
    rid = ['1', '168', '3', '129', '4', '36',
           '188', '160', '119', '155', '5', '181']
    result = []
    for i in rid:
        url = "https://api.bilibili.com/x/web-interface/ranking?rid=" + i + "&day=3&type=1"
        ret = urllib.request.Request(url=url, method='GET')
        res = urllib.request.urlopen(ret)
        req = str(BeautifulSoup(res, 'html.parser'))
        temp = json.loads(req)
        data = temp["data"]
        msg = data["list"]
        for dic in msg:
            elements = {
                'aid': dic['aid'],
                'coins': dic['coins'],
                'play': dic['play'],
                'pts': dic['pts'],
                'review': dic['video_review'],
            }
            result.append(elements)
    return result


def write_csv(msg):
    column = ['aid', 'coins', 'play', 'pts', 'review']
    data = pd.DataFrame(columns=column, data=msg)
    data.to_csv('rank.csv', index=False)


if __name__ == '__main__':
    result = craw()
    write_csv(result)
