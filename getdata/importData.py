# coding: utf-8
import re
import emoji
result = list()
n=1
with open('D:/data/data_us.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f.readlines():
        print(n)
        # co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        # line = re.sub(co, '', line)
        # print(line)
        # line = emoji.demojize(line)

        res = re.findall(r'(iPhone [\w\ ]+),(\d{2,3}GB),([\w\ \/\(\)]*),(.*),(\d{1}),(.*),(\d{4}-\d{2}-\d{2}),(.*)', line, flags=0)[0]
        print(res)
        n = n+1
        result.append(res)
    print(len(result))
f.close()


with open('D:/data/data_all.txt', 'a', encoding='utf-8') as fileObject:
    # header = ["phone_name", "size", "color", "username", "star", "title", "date", "review"]
    # fileObject.write('\t'.join(header)+"\n")
    for word in result:
        # print(word)
        l=[]
        for i in range(0, len(word)):
           l.append(word[i].strip())
        fileObject.write('\t'.join(l) + '\n')
fileObject.close()