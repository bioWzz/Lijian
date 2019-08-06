setwd("D:/analysis")
library(pheatmap)


data_pos<-read.csv("data/duishu_pos.csv",header = T,row.names = 1,sep="\t",encoding = "UTF-8")
pheatmap(data_pos,cluster_col = FALSE,filename = "img/retu_pos.pdf",cellwidth = 40, cellheight = 15,fontsize = 12)

data_neg<-read.csv("data/duishu_neg.csv",header = T,row.names = 1,sep="\t",encoding = "UTF-8")
pheatmap(data_neg,cluster_col = FALSE,filename = "img/retu_neg.pdf",cellwidth = 40, cellheight = 15,fontsize = 12)
