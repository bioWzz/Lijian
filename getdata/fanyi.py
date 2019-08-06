import json
import urllib.request
import urllib.parse
from HandleJs import Py4Js
import pymysql
import time
import re
import emoji


def open_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def buildUrl(content, tk, tl):
    baseUrl = 'http://translate.google.cn/translate_a/single'
    baseUrl += '?client=t&'
    baseUrl += 'sl=auto&'
    baseUrl += 'tl=' + str(tl) + '&'
    baseUrl += 'hl=zh-CN&'
    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'clearbtn=1&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'srcrom=0&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + content
    return baseUrl


def translate(content, tk, tl):
    content = urllib.parse.quote(content)
    url = buildUrl(content, tk, tl)

    result = open_url(url)
    res_json = json.loads(result)
    if len(res_json[0]) == 1:
        trans_text = res_json[0][0][0]
    else:
        trans_text = res_json[0][0][0]
        for i in range(1, len(res_json[0])):
            if res_json[0][i][0] != None:
                trans_text = trans_text + res_json[0][i][0]
    # sl是要翻译的源语种
    sl = res_json[8][0][0]
    return trans_text


def google_translate(content):
    # content是要翻译的内容
    # tl是要翻译的目标语种，值参照ISO 639-1标准，如果翻译成中文"zh/zh-CN简体中文"
    js = Py4Js()
    tl = "zh-CN"
    tk = js.getTk(content)
    # print(content)
    review = []
    if len(content) < 4000:
        trans_text = translate(content, tk, tl)
        time.sleep(0.5)
    else:
        review = content.split(u'.')
        temp = []
        temp.append(google_translate(".".join(review[0:(len(review) // 2)])))
        time.sleep(0.5)
        temp.append(google_translate(".".join(review[(len(review) // 2):len(review)])))
        time.sleep(0.5)
        trans_text = ".".join(temp)
    return trans_text


# trasnlation_list = []
# translate_file = open('D:/data/data_de_trans.txt', "w", encoding='utf-8')
# with open('D:/data/test.txt', 'r',  encoding='utf-8') as f:
#     next(f)
#     for element in f:
#         trasnlation_list.append(element.strip())
# count=0
# for i in range(13,len(trasnlation_list)):
#     print("翻译第"+str(i+1)+"行")
#     trans_res=[]
#     line = re.split("\t", trasnlation_list[i])
#     trans_res.append(line[0])
#     trans_res.append(line[1])
#     trans_res.append(line[2])
#     trans_res.append(line[3])
#     trans_res.append(line[4])
#     trans_res.append(google_translate(line[5]))
#     time.sleep(1)
#     trans_res.append(line[6])
#
#     review = line[7]
#     print(review)
#     if len(review) < 4000:
#         trans_res.append(google_translate(str(review)))
#         translate_file.write("\t".join(trans_res) + '\n')
#     else:
#         review = re.split("\.", line[7])
#         print(review)
#         temp=[]
#         for rw in review:
#             temp.append(google_translate(rw))
#         trans_res.append('.'.join(temp))
#         translate_file.write("\t".join(trans_res) + '\n')
#     print(trans_res[7])
#     count += 1
#     print('complete', '%.1f%%' % ((count / len(trasnlation_list)) * 100))
#     time.sleep(1)
# f.close()
# translate_file.close()


conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="amazon", charset='utf8mb4')


def insertData(list):
    with conn:
        # print(len(list))
        cursor = conn.cursor()
        sql = "update data_all_trans_zh set title=%s,review=%s where id=%s;"
        cursor.execute(sql, list)


datalist = []
with conn:
    cursor = conn.cursor()
    sql = "select id,title,review,star from data_all where id in (SELECT id from data_all_trans_zh where review IS NULL)"
    cursor.execute(sql)
    results = cursor.fetchall()
    for it in results:
        datalist.append(it)
n = 1
for line in datalist:
    if n % 300 == 0:
        time.sleep(10)
    list = []
    print("review id为:" + str(line[0]))
    em = re.compile(u':[\w_\-\ ]+?:|▲|▼|⭐')
    print(line[1])
    print(line[2])
    title_org = emoji.demojize(line[1])
    review_org = emoji.demojize(line[2])
    title_org = em.sub('', title_org)
    review_org = em.sub('', review_org)

    if title_org == '' or review_org == '':
        if line[3] == '5':
            title_org = 'Perfect'
            review_org = 'Perfect'
        elif line[3] == '4':
            title_org = 'Good'
            review_org = 'Good'
        elif line[3] == '3':
            title_org = 'Not good'
            review_org = 'Not good'
        else:
            title_org = 'Bad'
            review_org = 'Bad'
        print(title_org)

    title = google_translate(title_org)
    review = google_translate(review_org)
    list.append(title)
    list.append(review)
    list.append(line[0])
    print(list)
    insertData(list)
    n = n+1
conn.close()
