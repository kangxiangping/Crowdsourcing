#-*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import pandas as pd
from . import vgg19_trainable as vgg19
from . import utils
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def data_procesing(fileList): #列表中要求直接就是路径
    batch = np.zeros((len(fileList), 224, 224, 3), dtype=float)
    for i in range(len(fileList)):
        img = utils.load_image(fileList[i])
        img = img.reshape((1, 224, 224, 3))
        batch[i] = img[0]
    return batch


def cal_easiness(prob):
    easi = 0
    for i in range(len(prob)):
        easi += prob[i]*np.log(prob[i])
    return easi

def Selfpaced(taskId_list, task_batch):
    tf.reset_default_graph()
    with tf.Session(config=tf.ConfigProto(gpu_options=(tf.GPUOptions(per_process_gpu_memory_fraction=0.7)))) as sess:
        if len(taskId_list) <= 40:
            images = tf.placeholder(tf.float32, [len(taskId_list), 224, 224, 3])
            train_mode = tf.placeholder(tf.bool)

            vgg = vgg19.Vgg19('static/data/vgg19.npy')
            vgg.build(images, train_mode)

            # sess.run(tf.initialize_all_variables())
            sess.run(tf.global_variables_initializer())

            feed_dict = {images: task_batch, train_mode: False}
            prob = sess.run(vgg.prob, feed_dict=feed_dict)
            feature = pd.DataFrame(prob, index=taskId_list)

            tf.get_default_graph().finalize()
            return feature
        else:
            num = len(taskId_list)//40
            feature = pd.DataFrame(index=[j for j in range(len(taskId_list))], columns=[j for j in range(1000)])

            images = tf.placeholder(tf.float32, [40, 224, 224, 3])
            train_mode = tf.placeholder(tf.bool)

            vgg = vgg19.Vgg19('static/data/vgg19.npy')
            vgg.build(images, train_mode)
            sess.run(tf.global_variables_initializer())

            for i in range(num):
                feed_dict = {images: task_batch[i*40:i*40+40], train_mode: False}
                prob = sess.run(vgg.prob, feed_dict=feed_dict)
                feature[i*40: i*40+40] = prob

            images = tf.placeholder(tf.float32, [len(taskId_list)-40*num, 224, 224, 3])

            vgg.build(images, train_mode)

            # sess.run(tf.initialize_all_variables())
            sess.run(tf.global_variables_initializer())

            feed_dict = {images: task_batch[num * 40:len(taskId_list)], train_mode: False}
            prob = sess.run(vgg.prob, feed_dict=feed_dict)
            feature[num*40: len(taskId_list)] = prob

            feature.index = taskId_list
            tf.get_default_graph().finalize()

            return feature

def goldTaskSelected(clustering_data, classes, taskNum, goldNum): #cluster_data是特征向量，df,行列索引都有，classes是类别数， taskNum是总的任务数，goldNum是goldenTask数量
    taskId = clustering_data.index

    kmeans = KMeans(n_clusters=classes)  # 创建一个K-均值聚类对象
    kmeans.fit(clustering_data.values)
    label_list = kmeans.labels_
    center = kmeans.cluster_centers_

    order_task = []

    for label in range(classes):
        index_list = [index for index, l in enumerate(label_list) if l == label]
        distance = pd.Series(index=taskId[index_list])
        dis = cdist(clustering_data.iloc[index_list], np.array(center[label]).reshape(1, -1), metric='euclidean')
        for i in range(len(index_list)):
            distance[taskId[index_list[i]]] = dis[i][0]
        distance_sorted = distance.sort_values(ascending=True)
        if label == classes - 1:
            num = goldNum - len(order_task)
        else:
            num = round(goldNum * (len(index_list) / taskNum))
        order_task.extend(distance_sorted.index[:num])
    return order_task #返回goldTaskID























