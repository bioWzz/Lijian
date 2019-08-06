import numpy as np
import os

# 读取文件
def read_data(file):
    data = []
    with open(os.path.join('D:/analysis/data/1', file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            review = line.split("\t")
            review[1]=review[1].strip()
            data.append(review)
    print(len(data))
    return data


def load_dataset():
    review_list=[]
    class_vec=[]
    sent_list =read_data('review_pos.csv')+read_data('review_neg.csv')
    
    for i in sent_list:
        review =i[0].split(" ")
        review_list.append(review)
        class_vec.append(i[1])
    return review_list, class_vec
 
def create_vocab_list(dataset):
	vocab_set = set([])
	
	for doc in dataset:
		vocab_set = vocab_set | set(doc)
	
	return list(vocab_set)
 
def set_of_words2vec(vocab_list, input_set):
	return_vec = [0] * len(vocab_list)
	
	for word in input_set:
		if word in vocab_list:
			return_vec[vocab_list.index(word)] = 1
	
	return return_vec
 
def trainNB(train_matrix, train_catagory):
	num_train_docs = len(train_matrix)
	num_words = len(train_matrix[0])
	pos_num = 0
	for i in train_catagory:
		if i == 1:
			pos_num += 1
	pAbusive = pos_num / float(num_train_docs)
	p0_num = np.ones(num_words)
	p1_num = np.ones(num_words)
	p0_demon = 2.0
	p1_demon = 2.0
	
	for i in range(num_train_docs):
		if train_catagory[i] == 1:
			p1_num += train_matrix[i]
			p1_demon += sum(train_matrix[i])
		else:
			p0_num += train_matrix[i]
			p0_demon += sum(train_matrix[i])
	
	p1_vect = np.log(p1_num / p1_demon)
	p0_vect = np.log(p0_num / p0_demon)
	
	return p0_vect, p1_vect, pAbusive
 
def classifyNB(vec2classify, p0_vec, p1_vec, pClass1):
	p1 = sum(vec2classify * p1_vec) + np.log(pClass1)
	p0 = sum(vec2classify * p0_vec) + np.log(1.0 - pClass1)
	
	if p1 > p0:
		return 1
	elif p0 > p1:
		return 0
	else:
		return -1
	
	
list_sents, list_classes = load_dataset()
my_vocab_list = create_vocab_list(list_sents)
train_mat = []
for sent_in_doc in list_sents:
	train_mat.append(set_of_words2vec(my_vocab_list, sent_in_doc))
 
p0V, p1V, pAb = trainNB(train_mat, list_classes)

all_list=read_data("review_tag.csv")
n=0
for line in all_list:
    review =line[0]
    lable=line[1]
    pre_lable=classifyNB(np.array(set_of_words2vec(my_vocab_list, review.split(" "))), p0V, p1V, pAb)
    if lable==str(pre_lable):
        print(pre_lable)
    else:
        print(lable)
        print(pre_lable)
        n=n+1
print(n/len(all_list))