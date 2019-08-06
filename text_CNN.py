import d2lzh as d2l
from mxnet import gluon, init, nd
from mxnet.contrib import text
from mxnet.gluon import data as gdata, loss as gloss, nn
import random
import os

train_data = []
test_data = []


def read_data(file):
    data = []
    with open(os.path.join('/home/li/桌面/amazon/data/', file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            review = line.split("\t")
            review[1] = int(review[1].strip())
            data.append(review)
    random.shuffle(data)
    print(len(data))
    print(data[1])
    return data


def preprocess_imdb(data, vocab):  # 本函数已保存在d2lzh包中方便以后使用
    max_l =200  # 将每条评论通过截断或者补0，使得长度变成500

    def pad(x):
        return x[:max_l] if len(x) > max_l else x + [0] * (max_l - len(x))

    tokenized_data = d2l.get_tokenized_imdb(data)
    features = nd.array([pad(vocab.to_indices(x)) for x in tokenized_data])
    labels = nd.array([score for _, score in data])
    return features, labels

pos_data = read_data('review_pos.csv')
neg_data = read_data('review_neg.csv')
train_data = pos_data[0:int(len(pos_data) * 0.8)] + neg_data[0:int(len(neg_data) * 0.8)]
test_data = pos_data[int(len(pos_data) * 0.9):len(pos_data)] + neg_data[int(len(neg_data) * 0.9):len(neg_data)]
val_data = pos_data[int(len(pos_data) * 0.8):int(len(pos_data) * 0.9)] + neg_data[int(len(neg_data) * 0.8):int(
    len(neg_data) * 0.9)]
random.shuffle(train_data)
print(len(train_data))
print(len(test_data))

vocab = d2l.get_vocab_imdb(train_data+test_data)
print('# words in vocab:', len(vocab))

batch_size = 64
train_set = gdata.ArrayDataset(*preprocess_imdb(train_data, vocab))
test_set = gdata.ArrayDataset(*preprocess_imdb(test_data, vocab))
train_iter = gdata.DataLoader(train_set, batch_size, shuffle=True)
test_iter = gdata.DataLoader(test_set, batch_size)

class TextCNN(nn.Block):
    def __init__(self, vocab, embed_size, kernel_sizes, num_channels,
                 **kwargs):
        super(TextCNN, self).__init__(**kwargs)
        self.embedding = nn.Embedding(len(vocab), embed_size)
        # 不参与训练的嵌入层
        self.constant_embedding = nn.Embedding(len(vocab), embed_size)
        self.dropout = nn.Dropout(0.5)
        self.decoder = nn.Dense(2)
        # 时序最大池化层没有权重，所以可以共用一个实例
        self.pool = nn.GlobalMaxPool1D()
        self.convs = nn.Sequential()  # 创建多个一维卷积层
        for c, k in zip(num_channels, kernel_sizes):
            self.convs.add(nn.Conv1D(c, k, activation='relu'))

    def forward(self, inputs):
        # 将两个形状是(批量大小, 词数, 词向量维度)的嵌入层的输出按词向量连结
        embeddings = nd.concat(
            self.embedding(inputs), self.constant_embedding(inputs), dim=2)
        # 根据Conv1D要求的输入格式，将词向量维，即一维卷积层的通道维，变换到前一维
        embeddings = embeddings.transpose((0, 2, 1))
        # 对于每个一维卷积层，在时序最大池化后会得到一个形状为(批量大小, 通道大小, 1)的
        # NDArray。使用flatten函数去掉最后一维，然后在通道维上连结
        encoding = nd.concat(*[nd.flatten(
            self.pool(conv(embeddings))) for conv in self.convs], dim=1)
        # 应用丢弃法后使用全连接层得到输出
        outputs = self.decoder(self.dropout(encoding))
        return outputs




embed_size, kernel_sizes, nums_channels =100, [2, 4, 6 ,8], [100, 100, 100]
ctx = d2l.try_all_gpus()
net = TextCNN(vocab, embed_size, kernel_sizes, nums_channels)
net.initialize(init.Xavier(), ctx=ctx)
# net.load_parameters("D:/data/model_cnn.params")

glove_embedding = text.embedding.create(
    'glove', pretrained_file_name='glove.6B.100d.txt', vocabulary=vocab)
net.embedding.weight.set_data(glove_embedding.idx_to_vec)
net.constant_embedding.weight.set_data(glove_embedding.idx_to_vec)
net.constant_embedding.collect_params().setattr('grad_req', 'null')

lr, num_epochs = 0.001,10
trainer = gluon.Trainer(net.collect_params(), 'adam', {'learning_rate': lr})
loss = gloss.SoftmaxCrossEntropyLoss()
d2l.train(train_iter, test_iter, net, loss, trainer, ctx, num_epochs)
#net.save_parameters('/home/li/桌面/amazon/model_cnn.params')

def softmax(X):
    X_exp=X.exp()
    partition=X_exp.sum(axis=1,keepdims=True)
    return X_exp/partition
def predict_sentiment(net, vocab, sentence):
    """Predict the sentiment of a given sentence."""
    sentence = nd.array(vocab.to_indices(sentence), ctx=d2l.try_gpu())
    label = nd.argmax(net(sentence.reshape((1, -1))), axis=1)
    y_score=softmax(net(sentence.reshape((1, -1))))
    res='positive' if label.asscalar() == 1 else 'negative'
    return res,y_score[0][1].asscalar()



num_val = len(val_data)
n = 0
y_score=[]
y_test=[]
for i in val_data:
    
    label = i[1]
    review = i[0].split(" ")
    if len(review)<6:
        while (6-len(review))>0:
            review.append(" ")
    pre,score = predict_sentiment(net, vocab, review)
   
    y_score.append(score)
    if pre=="positive":
        pre_lab=1
    else:
        pre_lab=0
    y_test.append(label)
    if pre_lab == label:
        n = n + 1
print('%.2f%%'%((n/num_val)*100))


import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.metrics import roc_curve, auc  ###计算roc和auc
fpr,tpr,threshold = roc_curve(y_test, y_score) ###计算真正率和假正率
roc_auc = auc(fpr,tpr) ###计算auc的值

pdf = PdfPages('roc.pdf')
plt.figure()
lw = 2
plt.figure(figsize=(10,10))

plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='AUC (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
font1 = {
'size'   : 16,
}

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate',font1)
plt.ylabel('True Positive Rate',font1)
plt.legend(loc="lower right")
plt.tick_params(labelsize=23)
plt.show()
pdf.savefig()
plt.close()
pdf.close() 



#def read_file(file):
#    data = []
#    with open(os.path.join('/home/li/桌面/amazon/data/', file), 'r', encoding='utf-8') as f:
#        for line in f.readlines():
#            review = line.split("\t")
#            review[9] = review[9].strip()
#            data.append(review)
#    random.shuffle(data)
#    return data
#
#data_all=read_file("review_tag.csv")
#
#for i in data_all:
#    i.remove(i[0])
#    review = i[8].split(" ")
#    if len(review)<6:
#        while (6-len(review))>0:
#            review.append(" ")
#    pre = d2l.predict_sentiment(net, vocab, review)
#    if pre == "positive":
#        i.append("1")
#    else:
#        i.append("0")
#        
#
#f1=open('/home/li/桌面/amazon/data/pre_pos.csv', mode='w', encoding='utf-8')
#f2=open('/home/li/桌面/amazon/data/pre_neg.csv', mode='w', encoding='utf-8')
#for i in data_all:
#    if i[9]==str(1):
#        f1.write("\t".join(i)) 
#        f1.write("\n")
#    else:
#        f2.write("\t".join(i))
#        f2.write("\n")
#f1.close
#f2.close