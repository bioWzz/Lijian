import d2lzh as d2l
from mxnet import gluon, init, nd
from mxnet.contrib import text
from mxnet.gluon import data as gdata, loss as gloss, nn, rnn, utils as gutils
import os
import random

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
    max_l = 500  # 将每条评论通过截断或者补0，使得长度变成500

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

for X, y in train_iter:
    print('X', X.shape, 'y', y.shape)
    break
print('#batches:', len(train_iter))


class BiRNN(nn.Block):
    def __init__(self, vocab, embed_size, num_hiddens, num_layers, **kwargs):
        super(BiRNN, self).__init__(**kwargs)
        self.embedding = nn.Embedding(len(vocab), embed_size)
        # bidirectional设为True即得到双向循环神经网络
        self.encoder = rnn.LSTM(num_hiddens, num_layers=num_layers,
                                bidirectional=True, input_size=embed_size)
        self.decoder = nn.Dense(2)

    def forward(self, inputs):
        # inputs的形状是(批量大小, 词数)，因为LSTM需要将序列作为第一维，所以将输入转置后
        # 再提取词特征，输出形状为(词数, 批量大小, 词向量维度)
        embeddings = self.embedding(inputs.T)
        # rnn.LSTM只传入输入embeddings，因此只返回最后一层的隐藏层在各时间步的隐藏状态。
        # outputs形状是(词数, 批量大小, 2 * 隐藏单元个数)
        outputs = self.encoder(embeddings)
        # 连结初始时间步和最终时间步的隐藏状态作为全连接层输入。它的形状为
        # (批量大小, 4 * 隐藏单元个数)。
        encoding = nd.concat(outputs[0], outputs[-1])
        outs = self.decoder(encoding)
        return outs


embed_size, num_hiddens, num_layers, ctx = 100, 100, 2, d2l.try_gpu()

net = BiRNN(vocab, embed_size, num_hiddens, num_layers)
net.initialize(init.Xavier(), ctx=ctx)

glove_embedding = text.embedding.create(
    'glove', pretrained_file_name='glove.6B.100d.txt', vocabulary=vocab)
net.embedding.weight.set_data(glove_embedding.idx_to_vec)
net.embedding.collect_params().setattr('grad_req', 'null')
# net.load_parameters('/home/li/桌面/amazon/model.params')

lr, num_epochs = 0.01, 5
trainer = gluon.Trainer(net.collect_params(), 'adam', {'learning_rate': lr})
loss = gloss.SoftmaxCrossEntropyLoss()
d2l.train(train_iter, test_iter, net, loss, trainer, ctx, num_epochs)


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
    y_test.append(pre_lab)
    if pre_lab == label:
        n = n + 1
print('%.2f%%'%((n/num_val)*100))


import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc  ###计算roc和auc
fpr,tpr,threshold = roc_curve(y_test, y_score) ###计算真正率和假正率
roc_auc = auc(fpr,tpr) ###计算auc的值

plt.figure()
lw = 2
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()