setwd("D:/analysis")
library(ggplot2)
library(showtext)
showtext.auto(enable = TRUE)
font.add('SimSun', 'simsun.ttc','Times New Roman')

data_t<-read.csv("data/结果统计.csv",header = T,sep=",",encoding = "UTF-8")


noblank<-theme(panel.grid.major =element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(),axis.line = element_line(colour = "black"))
pt<-ggplot(data_t,aes(x=star,y=count))
pt<-pt+noblank
pt<-pt+facet_wrap(~label,ncol=2)
pt<-pt+geom_bar(stat='identity',fill="#4169E1")
pt<-pt+geom_text(aes(label=p), vjust=-0.2)
pt<-pt+labs(title = "预测结果统计",x = "星级", y = "条数")+theme(plot.title = element_text(size=16,hjust = 0.5),text=element_text(size = 16,family = "The New Roman"))

pdf("img/pdf/结果统计.pdf",width=8,height=4)
pt
dev.off()
