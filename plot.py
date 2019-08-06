# 导入扩展库
import os
import collections # 词频统计库
import wordcloud # 词云展示库
import matplotlib.pyplot as plt # 图像展示库

# 读取文件
def read_data(file):
    data = []
    with open(os.path.join('/home/li/桌面/plot/', file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            review = line.split("\t")
            data.append(review)
    print(len(data))
    return data

pre_pos = read_data('review_pre_pos.csv')
pre_neg= read_data('review_pre_neg.csv')

pre_list=pre_pos+pre_neg
phone_list=['','','','','','','','','','']

L=[]
for i in pre_list:
    print(i[0])
    if i[1] not in L:
        L.append(i[1])
print(" ".join(L))


text_pos=""
text_neg=""
for i in pre_pos:
    text_pos=text_pos+i[9]
for i in pre_neg:
    text_neg=text_neg+i[9]


# 文本分词
seg_list_pos = text_pos.split(" ")
seg_list_neg = text_neg.split(" ")
# 去除词库
remove_words=[]
with open('/home/li/桌面/plot/stopwords.csv', 'r', encoding='utf-8') as f:
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
word_counts_neg = collections.Counter(object_neg) # 对分词做词频统计
word_counts_pos.most_common(200)

# 词频展示

wc = wordcloud.WordCloud(
        scale=4,
        max_words = 150,
        background_color="white", #设置背景为白色，默认为黑色
        width=1490,              #设置图片的宽度
        height=990,              #设置图片的高度
        margin=10,               #设置图片的边缘
        max_font_size=200,
        min_font_size=20,
        random_state=30,
        )

#pos
wc.generate_from_frequencies(word_counts_pos)
fig1 = plt.gcf()
plt.imshow(wc)
plt.axis("off")
plt.show()
fig1.savefig('/home/li/桌面/plot/pos.png', dpi=300)
my_wordcloud_neg = wordcloud.WordCloud(background_color="white",width=1000,height=1000)

#neg
wc.generate_from_frequencies(word_counts_neg)
fig2 = plt.gcf()
plt.imshow(wc)
plt.axis("off")
plt.show()
fig2.savefig('/home/li/桌面/plot/neg.png', dpi=300)




