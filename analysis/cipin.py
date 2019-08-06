# 导入扩展库
import os
import collections # 词频统计库
import pandas as pd
import math

# 读取文件
def read_data(file):
    data = []
    with open(os.path.join('D:/analysis/data', file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            review = line.split("\t")
            data.append(review)
    print(len(data))
    return data

pre_pos = read_data('pre_pos.csv')
pre_neg= read_data('pre_neg.csv')

# 去除词库
remove_words=[]
with open('D:/analysis/data/stopwords.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line=line.strip()
        line=line.lower()
        remove_words.append(str(line)) 

def getcipin(text,phone):     
    seg_list_temp = text.split(" ")
    object_temp=[]
    for word in seg_list_temp: # 循环读出每个分词
        word=word.strip()
        word=word.lower()
        if word not in remove_words: # 如果不在去除词库中
            object_temp.append(word) # 分词追加到列表
    # 词频统计
    word_counts_temp = collections.Counter(object_temp) # 对分词做词频统计 
#    word_most=word_counts_temp.most_common(100)
    df = pd.DataFrame.from_dict(word_counts_temp,orient='index',columns=[phone])
    return df



phone_list=['iPhone 6S','iPhone 6S Plus','iPhone 7','iPhone 7 Plus','iPhone 8','iPhone 8 Plus','iPhone X','iPhone XS','iPhone XS Max','iPhone XR']


word_pos_10=pd.DataFrame()

for phone in phone_list:
    text_temp=""
    for i in pre_pos:
        if i[0]==phone:
            text_temp=text_temp+i[8]
#    phone=phone.replace(" ","_")
#    exec ("%s_count=getcipin(text_temp)"%phone)
    word_pos_10=pd.concat([word_pos_10,getcipin(text_temp,phone)],axis=1)

#替换Nan为0
final_pos=word_pos_10.where(word_pos_10.notnull(), 0)
final_pos=final_pos[final_pos>4]
final_pos=final_pos.dropna(axis=0,how="any")
#final_pos.to_csv('D:\\analysis\\data\\count_10_pos.csv', sep=',', header=True, index=True)
#变百分数
#列（即投影到列）求和
#行（即投影到行）除法
final_pos=final_pos.div(final_pos.sum(axis=0), axis=1)
#final_pos.to_csv('D:\\analysis\\data\\words_per.csv', sep=',', header=True, index=True)

f = lambda x :math.log(x) if x !=0 else x
duishu_pos=final_pos.applymap(f)
duishu_pos.to_csv('D:\\analysis\\data\\duishu_pos.csv', sep='\t', header=True, index=True)


word_neg_10=pd.DataFrame()

for phone in phone_list:
    text_temp=""
    for i in pre_neg:
        if i[0]==phone:
            text_temp=text_temp+i[8]
#    phone=phone.replace(" ","_")
#    exec ("%s_count=getcipin(text_temp)"%phone)
    word_neg_10=pd.concat([word_neg_10,getcipin(text_temp,phone)],axis=1)

#替换Nan为0
final_neg=word_neg_10.where(word_neg_10.notnull(), 0)
final_neg=final_neg[final_neg>0]
final_neg=final_neg.dropna(axis=0,how="any")
#final_pos.to_csv('D:\\analysis\\data\\count_10_pos.csv', sep=',', header=True, index=True)
#变百分数
#列（即投影到列）求和
#行（即投影到行）除法
final_neg=final_neg.div(final_neg.sum(axis=0), axis=1)
#final_neg.to_csv('D:\\analysis\\data\\words_per.csv', sep=',', header=True, index=True)
f = lambda x :math.log(x) if x !=0 else x
duishu_neg=final_neg.applymap(f)
duishu_neg.to_csv('D:\\analysis\\data\\duishu_neg.csv', sep='\t', header=True, index=True)



##计算列的和
#final.loc['Col_sum'] = final.apply(lambda x: x.sum())
##计算行的和
#final['Row_sum'] = final.apply(lambda x: x.sum(), axis=1)
#final.to_csv('D:\\analysis\\data\\words_count.csv', sep=',', header=True, index=True)


text_pos=""
text_neg=""
for i in pre_pos:
    text_pos=text_pos+i[8]
for i in pre_neg:
    text_neg=text_neg+i[8]


# 文本分词
seg_list_pos = text_pos.split(" ")
seg_list_neg = text_neg.split(" ")
# 去除词库
remove_words=[]
with open('D:/analysis/data/stopwords.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line=line.strip()
        line=line.lower()
        remove_words.append(str(line)) 

object_pos=[]
object_neg=[]
for word in seg_list_pos: # 循环读出每个分词
    word=word.strip()
    word=word.lower()
    if word not in remove_words: # 如果不在去除词库中
        object_pos.append(word) # 分词追加到列表

for word in seg_list_neg: # 循环读出每个分词
    word=word.strip()
    word=word.lower()
    if word not in remove_words: # 如果不在去除词库中
        object_neg.append(word) # 分词追加到列表
# 词频统计
word_counts_pos = collections.Counter(object_pos) # 对分词做词频统计
word_counts_neg = collections.Counter(object_neg) # 对分词做词频统计.

word_pos=pd.DataFrame.from_dict(word_counts_pos,orient='index',columns=["word"])
word_pos=word_pos[word_pos['word']>200]

word_neg=pd.DataFrame.from_dict(word_counts_neg,orient='index',columns=["word"])
word_neg=word_neg[word_neg['word']>40]

word_pos.to_csv('D:\\analysis\\data\\word_pos.csv', sep=',', header=True, index=True)
word_neg.to_csv('D:\\analysis\\data\\word_neg.csv', sep=',', header=True, index=True)



#pre_list=pre_pos+pre_neg
#
#text_all=""
#for i in pre_list:
#    text_all=text_all+i[8]
#
#words_all=text_all.split(" ")
#object_all=[]
#for word in words_all: # 循环读出每个分词
#    word=word.strip()
#    word=word.lower()
#    if word not in remove_words: # 如果不在去除词库中
#        object_all.append(word) # 分词追加到列表
## 词频统计
#words_counts_all = collections.Counter(object_all) # 对分词做词频统计
#words_all_count=pd.DataFrame.from_dict(words_counts_all,orient='index',columns=["word"])
##变百分数
##列（即投影到列）求和
##行（即投影到行）除法
#words_counts_all_per=words_all_count.div(words_all_count.sum(axis=0), axis=1)
#words_all_count=words_all_count[words_all_count['word']>200]
#words_all_count.to_csv('D:\\analysis\\data\\words_all_count.csv', sep=',', header=True, index=True)
