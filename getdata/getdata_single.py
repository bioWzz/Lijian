import requests
from bs4 import BeautifulSoup
import time
import random
import re
import datetime
import pandas as pd
import pymysql.cursors

def crawl(url,phone):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,und;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'session-id=134-9235808-6481244; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:CN"; ubid-main=131-5148826-2432319; x-wl-uid=1XDFtJxR8+YWp/QY+enfaXJVdl7RDOwq+tBECUrGLrpqM2KREaq8lMomk7NJdHJJ1XOaVv2z+5RA=; csm-hit=tb:W2D938WDF1P0FAN6CYKB+s-MC2XS972WG6S082ZSYVF|1563266874448&t:1563266874448&adb:adblk_no; session-token=Hl+1wfSFy/Bn3XRja4PdQRPNxCusTEFvGa4xWe5RD+A5qvsfB324uSC6xMm5KgcNPcNF9tdQvLqK0dlFDezsoWASIsmv0lGob87NyOsifoMEDXXHuxAuW+ByUVeeARnHSWdc8OC3Na0iDoUxBi1RkJVm3RW+FeDak3PJJQUBWI77Qcn5KWnncoWNC3NO+wLm',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    session = requests.Session()
    response = session.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find_all("div", {"data-hook": "review"})
    data = []
    for res in result:

        username = res.find("span", {"class": "a-profile-name"}).text
        star = res.find("span", {"class": "a-icon-alt"}).text
        title = res.find("a", {"data-hook": "review-title"}).text
        date = res.find("span", {"data-hook": "review-date"}).text

        if(res.find("a",{"data-hook": "format-strip"})!=None):
            style = res.find("a", {"data-hook": "format-strip"}).text
            print(style)
            phone_color = re.findall(r"Colour: (.*?)", style, flags=0)[0]
            phone_size = re.findall(r'Size: (.*?GB)Colour', style, flags=0)[0].replace(" ", "")
        else:
            phone_color = "Silver"
            phone_size = "32GB"

        review = res.find("span", {"data-hook": "review-body"}).text
        review_date = datetime.datetime.strptime(date, '%d %B %Y')
        review_star = re.findall(r'\d+', star, flags=0)[0]

        review_title = title.strip()
        review=review.strip()
        res = [phone, phone_size, phone_color, username, review_star, review_title, review_date, review]
        data.append(res)
        # print(res)
    # print(data)
    save = pd.DataFrame(data)
    save.to_csv("D:/data/data.csv", mode='a', index=False, header=False, encoding="utf_8_sig", )

phone = "iPhone XS"
i = 1
url = "https://www.amazon.de/Apple-iPhone-XS-64GB-Space/product-reviews/B07HBCCGY8/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&language=en_GB&pageNumber=2&reviewerType=all_reviews"+str(i)
print(url)
crawl(url, phone)

