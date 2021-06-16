import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
df = pd.read_excel('E:\Download\识别狗的品种_实验五.xlsx', engine='openpyxl')

dict2 = {"n02108551": '藏獒', 'n02110063': '阿拉斯加', 'n02110185': '哈士奇', 'n02111277': '纽芬兰犬'}
dict3 = {"n02110958": '巴哥犬', 'n02085620': '吉娃娃', 'n02106166': '边牧', 'n02111277': '纽芬兰犬'}
dict = {"n02085936": '马耳他犬', 'n02088364': '猎兔犬', 'n02091134': '小灵狗', 'n02087046': '玩具梗'}
correct = 0
total = 0


for i in df.index:
    if not pd.isnull(df.loc[i]['answer']):
        total += 1
        if dict[df.loc[i]['name'].split('_')[0]] == df.loc[i]['answer']:
            correct += 1
print(correct/total)
print(total)



# def goldTaskSelected(clustering_data, classes, taskNum, goldNum): #cluster_data是特征向量，df,行列索引都有，classes是类别数， taskNum是总的任务数，goldNum是goldenTask数量
#     taskId = clustering_data.index
#
#     kmeans = KMeans(n_clusters=classes)  # 创建一个K-均值聚类对象
#     kmeans.fit(clustering_data.values)
#     label_list = kmeans.labels_
#     center = kmeans.cluster_centers_
#
#     for c in range(classes):
#         index_list = [index for index, l in enumerate(label_list) if l == c]
#         print(c, round(len(index_list)))
#
#
#     order_task = []
#
#     for label in range(classes):
#         index_list = [index for index, l in enumerate(label_list) if l == label]
#         distance = pd.Series(index=taskId[index_list])
#         dis = cdist(clustering_data.iloc[index_list], np.array(center[label]).reshape(1, -1), metric='euclidean')
#         for i in range(len(index_list)):
#             distance[taskId[index_list[i]]] = dis[i][0]
#         distance_sorted = distance.sort_values(ascending=True)
#         if label == classes - 1:
#             num = goldNum - len(order_task)
#         else:
#             num = int(goldNum * (len(index_list) / taskNum))
#         order_task.extend(distance_sorted.index[:num])
#     return order_task #返回goldTaskID
#
# feature = pd.read_csv('D:\PycharmProject\OnlineCrowd\static\media\\feature\\101.csv', index_col=0)
# classes = 4
# taskNum = 400
# goldNum = 20
#
# goldTaskSelected(feature, classes, taskNum, goldNum)



