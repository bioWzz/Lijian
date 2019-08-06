import pymysql
import re

def insertData(linelist):
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="amazon", charset="utf8mb4")
    with conn:
        cursor = conn.cursor()
        sql = "insert into data_fr values(%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.executemany(sql,linelist)
    conn.close()


with open('D:/data/data_fr.txt', 'r', encoding='utf-8') as f:
    next(f)
    data=[]
    for element in f:
        line = element.strip()
        print(line)
        linelist = re.split("\t", line)
        if len(linelist)<8:
            linelist.append("NA")
        data.append(linelist)
    insertData(data)