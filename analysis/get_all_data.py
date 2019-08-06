# 导入扩展库
import os
import pandas as pd
# 读取文件
def read_data(file):
    data = []
    with open(os.path.join('D:/analysis/data', file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            review = line.split("\t")
            review[9]=review[9].strip()
            data.append(review)
    print(len(data))
    return data


switchdic={"us":lambda x:"美国",
           "uk":lambda x:"英国",
           "de":lambda x:"德国",
           "it":lambda x:"it",
           "fr":lambda x:"法国",
            
            }

pre_pos = read_data('pre_pos.csv')
pre_neg= read_data('pre_neg.csv')
pre_list_all=pre_pos+pre_neg
temp_b=[]
for i in pre_list_all:
    b=[]
    b.append(i[0])
    b.append(i[1])
    b.append(i[2])
    b.append(i[4])
    b.append(i[6])
    b.append(switchdic[i[7]](i[7]))
    b.append(i[9])
    temp_b.append(b)
temp_b=pd.DataFrame(temp_b)
temp_b.to_csv('D:\\analysis\\data\\info_all.csv', sep='\t', header=False, index=False)



temp_b=[]
for i in pre_pos:
    b=[]
    b.append(i[0])
    b.append(i[1])
    b.append(i[2])
    b.append(i[4])
    b.append(i[6])
    b.append(switchdic[i[7]](i[7]))
    b.append(i[9])
    temp_b.append(b)
temp_b=pd.DataFrame(temp_b)
temp_b.to_csv('D:\\analysis\\data\\info_pos.csv', sep='\t', header=False, index=False)



temp_b=[]
for i in pre_neg:
    b=[]
    b.append(i[0])
    b.append(i[1])
    b.append(i[2])
    b.append(i[4])
    b.append(i[6])
    b.append(switchdic[i[7]](i[7]))
    b.append(i[9])
    temp_b.append(b)
temp_b=pd.DataFrame(temp_b)
temp_b.to_csv('D:\\analysis\\data\\info_neg.csv', sep='\t', header=False, index=False)
