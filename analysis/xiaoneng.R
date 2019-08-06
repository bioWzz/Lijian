setwd("D:/analysis")
library(ggplot2)
library(showtext)
showtext.auto(enable = TRUE)
font.add('SimSun', 'simsun.ttc','Times New Roman')

cnn<-read.csv("data/CNN.csv",header = T,sep=",",encoding = "UTF-8")
lstm<-read.csv("data/LSTM.csv",header = T,sep=",",encoding = "UTF-8")
cnn$method<-c("cnn")
lstm$method<-c("lstm")
data<-rbind(cnn,lstm)
data$Step<-data$Step+1

noblank<-theme(panel.grid.major =element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(),axis.line = element_line(colour = "black"))

p1<-ggplot(data,aes(x=Step,y=Value,color=method,group=method))+geom_line(size=1)
p1<-p1+labs(title = "两种神经网络准确率随迭代次数的变化",x = "迭代次数 ", y = "准确率")
p1<-p1+scale_color_manual(values=c("#000099","#56B4E9"))
p1<-p1+theme(plot.title = element_text(size=16,hjust = 0.5),text=element_text(size = 16,family = "The New Roman"))
p1<-p1+noblank
ggsave(p1,file="img/两种神经网络准确率随迭代次数的变化.png",width=8,height=4)

pdf("img/pdf/两种神经网络准确率随迭代次数的变化.pdf",width=8,height=6)
p1
dev.off()







method<-c("CNN","LSTM","Naive Bayes")
q<-c(0.92,0.86,0.847)

data_z<-data.frame(method,q)
p2<-ggplot(data_z,aes(x=method,y=q,fill=method))+geom_bar(stat = "identity",width = 0.5)+ ylim(0,1)
p2<-p2+labs(title = "三种算法准确率比较",x = "算法 ", y = "准确率")
p2<-p2+noblank+scale_fill_hue(l=30)+geom_text(aes(label=q), vjust=-0.2)+ theme(plot.title = element_text(size=16,hjust = 0.5),text=element_text(size = 16,family = "The New Roman"))
p2
ggsave(p2,file="img/三种算法准确率比较.png",width=8,height=6)

pdf("img/pdf/三种算法准确率比较.pdf",width=8,height=6)
p2
dev.off()
