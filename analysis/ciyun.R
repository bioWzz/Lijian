setwd("D:/analysis")
library(wordcloud2)
# words<-read.csv2("data/words_all_count.csv",header = T,sep=",",encoding = "UTF-8")
# index <- order(-words[,2])
# words_order<-words[index,]
# wordcloud2(words_order,size = 1,shape="circle",color = "random-dark",minRotation = -pi/3, maxRotation = pi/3,rotateRatio = 0.8)

words_pos<-read.csv2("data/word_pos.csv",header = T,sep=",",encoding = "UTF-8")
index <- order(-words_pos[,2])
words_pos_order<-words_pos[index,]
wordcloud2(words_pos_order,size = 0.8,shape="circle",color = "random-dark",minRotation = -pi/3, maxRotation = pi/3,rotateRatio = 0.8)


words_neg<-read.csv2("data/word_neg.csv",header = T,sep=",",encoding = "UTF-8")
index <- order(-words_neg[,2])
words_neg_order<-words_neg[index,]
wordcloud2(words_neg_order,size = 0.8,shape="circle",color = "random-dark",minRotation = -pi/3, maxRotation = pi/3,rotateRatio = 0.8)

