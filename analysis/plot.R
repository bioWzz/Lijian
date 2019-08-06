setwd("D:/analysis")
library(ggplot2)
library(lubridate)
library(showtext)
# info_pos<-read.csv("data/info_pos.csv",header = FALSE,sep="\t",encoding = "UTF-8")
# info_neg<-read.csv("data/info_neg.csv",header = FALSE,sep="\t",encoding = "UTF-8")
data_all<-read.csv("data/info_all.csv",header = FALSE,sep="\t",encoding = "UTF-8")

# names(info_pos)<-c('phone','size','color','star','date','site')
# names(info_neg)<-c('phone','size','color','star','date','site')
names(data_all)<-c('phone','size','color','star','date','site','label')
site=as.matrix(data_all$site)
for(i in 1:length(site)){
  if(site[i]=="it"){
    site[i]<-"意大利"
  }
}
data_all$site<-site

data_all$标签<-data_all$label
data_all$标签[data_all$标签==1]<-"好评"
data_all$标签[data_all$标签==0]<-"差评"




# 
# info_pos$month<-apply(as.matrix(info_pos$date), 1, month)
# info_pos$quarter<-apply(as.matrix(info_pos$date), 1, quarter)
# info_pos$year<-apply(as.matrix(info_pos$date), 1, year)
# info_neg$month<-apply(as.matrix(info_neg$date), 1, month)
# info_neg$quarter<-apply(as.matrix(info_neg$date), 1, quarter)
# info_neg$year<-apply(as.matrix(info_neg$date), 1, year)
data_all$month<-apply(as.matrix(data_all$date), 1, month)
data_all$quarter<-apply(as.matrix(data_all$date), 1, quarter)
data_all$year<-apply(as.matrix(data_all$date), 1, year)


noblank<-theme(panel.grid.major =element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(),axis.line = element_line(colour = "black"))
windowsFonts(A=windowsFont("Times New Roman"), H=windowsFont("微软雅黑"))
font_and_title<-theme(plot.title = element_text(hjust = 0.5,size=16,family="H"))



difsite<-ggplot(data_all,aes(x=site,fill=phone))+geom_bar(stat='count',position = "fill")+noblank
difsite<-difsite+labs(title="不同地区不同产品的占比", x="地区", y="比例")+theme_bw()+font_and_title
difsite<-difsite+coord_polar()
difsite<-difsite+theme(
  panel.grid = element_blank(),
  panel.border= element_blank(),
  axis.text.y = element_blank(),
  axis.ticks = element_blank(),
  axis.title = element_blank()
) 
difsite<-difsite+scale_fill_hue(l=50)
ggsave(difsite,file="img/Fig4偏好性.png",width=8,height=6)

showtext_auto(enable = TRUE)
pdf("img/pdf/Fig4偏好性.pdf")
difsite
dev.off()

# 
# month_plot<-ggplot(X,aes(x=month,colour=phone,group=phone))+geom_line(stat='count',size=1)+scale_x_continuous(breaks = seq(1,12,1))+noblank
# month_plot<-month_plot+labs(title="评论数量随月份的变化", x="月份", y="评论数")
# month_plot<-month_plot+font_and_title
# ggsave(month_plot,file="img/Fig4month.png",width = 8,height =4)
#   
# quarter_plot<-ggplot(X,aes(x=quarter,colour=phone,group=phone))+geom_line(stat='count',size=1)+noblank
# quarter_plot<-quarter_plot+labs(title="评论数量随季度的变化", x="季度", y="评论数")
# quarter_plot<-quarter_plot+font_and_title
# ggsave(quarter_plot,file="img/quarter.png",width = 8,height =4)


phone_num<-as.data.frame(table(data_all$phone,data_all$site,data_all$标签))
names(phone_num)<-c('phone','site','label','num')
plot_cor<-ggplot(phone_num,aes(x=phone,y=num,fill=label))+geom_histogram(stat="identity",position = "fill")
plot_cor<-plot_cor+labs(title="两类评论的占比随商品时序的变化", x="产品", y="评论比例")
plot_cor<-plot_cor+scale_fill_hue(l=50)+theme(text= element_text(size=16,family="H"))
plot_cor<-plot_cor+noblank+font_and_title
ggsave(plot_cor,file="img/时序与评论相关性.png",width = 12,height =4)

pdf("img/pdf/时序与评论相关性.pdf",width = 12,height =4)
plot_cor
dev.off()





t_all<-as.data.frame(table(data_all$phone,data_all$标签))
t_all<-cbind(t_all[,1],c(rep("all",20)),t_all[,2:3])
phone_num2<-as.data.frame(table(data_all$phone,data_all$site,data_all$标签))
names(t_all)<-c('phone','site','label','num')
names(phone_num2)<-c('phone','site','label','num')
phone_num2<-rbind(phone_num2,t_all)

difsite2<-ggplot(phone_num2,aes(x=site,y=num,fill=label))
difsite2<-difsite2+noblank+font_and_title
difsite2<-difsite2+facet_wrap(~phone,ncol=5)
difsite2<-difsite2+geom_bar(stat='identity',position = "fill")
difsite2<-difsite2+labs(title="不同地区评价的差异", x="国家", y="评论比例")
difsite2<-difsite2+scale_fill_hue(l=50)
difsite2<-difsite2+theme(axis.text.x = element_text(angle = 45, hjust = 1),text = element_text(hjust = 0.5,size=16,family="H"))
ggsave(difsite2,file="img/不同地区评价的差异.png",width = 12,height =6)
pdf("img/pdf/不同地区评价的差异.pdf",width = 12,height =6)
difsite2
dev.off()

