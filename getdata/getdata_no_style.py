import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import dateparser

def crawl(url, phone, phone_color, phone_size):
    headers = {
        'accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'cookie': 'csm-hit=tb:s-1G0EMWYNQXNPAKKZJ68W|1563272028775&t:1563272029310&adb:adblk_no; session-token=lKKXtd8CUrAFdzfvoajdKtm5nU8VTAR0bD+X/R7nomtrjUIa62TkzUbQ4UWD8p0wDSf1nAuCRSioeFoMUjxYj+ZVAjymfQ7e+1wIXELT7Uk+TMKPlLprrKvleZR5fIZYjfR68pyjTqanYRLGEKEZEg9SSz+VW7c62/vH8q7feTvizAxSOdxJo0TRWqI+a5bC; session-id-time=2082754801l; session-id=260-8533334-2371525; i18n-prefs=EUR; x-wl-uid=1tkaKLVWq9MgwP34Ys3FGSTlQP5bMJMiMviKLm9whkk5vH9npeNn5b9zBPTTdHPyE7RpEpWDGEf8=; ubid-acbde=262-5774505-3025802; lc-acbde=en_GB',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
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
        review = res.find("span", {"data-hook": "review-body"}).text

        review_date = dateparser.parse(date).date()
        review_star = re.findall(r'\d+', star, flags=0)[0]
        review_title = title.strip()
        review = review.strip()
        res = [phone, phone_size, phone_color, username, review_star, review_title, review_date, review]
        data.append(res)
    save = pd.DataFrame(data)
    save.to_csv("D:/data/data_it.csv", mode='a', index=False, header=False, encoding="utf_8_sig", )

phone = "iPhone XS"
name = "Apple-iPhone-XS-64GB-siderale"
id = "B07HLDMZJZ"
phone_color = "Grigio siderale"
phone_size = "64GB"
total = 13

for i in range(1, (total // 20) + 2):
    print("正在下载第{}页数据...".format(i))
    # 亚马逊商品评论链接
    url = "https://www.amazon.it/"+name+"/product-reviews/"+id+"/ref=cm_cr_getr_d_paging_btm_next_"+str(i)+"?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)+"&pageSize=20"
    print(url)
    crawl(url, phone, phone_color, phone_size)

