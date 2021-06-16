#-*- coding: utf-8 -*-
"""
Simple tester for the vgg19_trainable
"""

import tensorflow as tf
from . import vgg19_trainable as vgg19
import numpy as np

dict = {'n02106662': 0, 'n02109961': 1, 'n02110341': 2, 'n02111277': 3}
bird_dict = {'Albatross': 0, 'Goldfinch': 1, 'Hummingbird': 2, 'indigo bunting': 3, 'Jay': 4}
object_dict = {'backpack': 0, 'binoculars': 1, 'canoe': 2, 'chimp': 3, 'electric guitar': 4, 'goldfish': 5}
mini_dict = {'n01532829': 0, 'n01704323': 1, 'n01910747': 2, 'n02101006': 3}

dog_class_index = [235, 248, 251, 256] #0到3四个类别对应1000个类别中第多少个类别的索引
bird_class_index = [146, 11, 94, 14, 17] #0到4五个类别对应1000个类别中第多少个类别的索引
object_class_index = [414, 447, 472, 367, 546, 1]
mini_class_index = [12, 51, 107, 214]
def data(truth):
    # img1 = Utils.load_image("./test_data/tiger.jpeg")
    # img1_true_result = [1 if i == 292 else 0 for i in xrange(1000)]  # 1-hot result for tiger
    #
    # batch1 = img1.reshape((1, 224, 224, 3))
    # image_list = []
    # for i in range(len(tasks)):
    #     image_list.append(str(int(tasks[i])) + 'sample' + str(int(tasks[i] - 1) // 200) + '.jpeg')
    # img = Utils.load_image(os.path.join('E:\PycharmProject\Feature\dog', image_list[0]))
    # batch = img.reshape((1, 224, 224, 3))
    # for i in range(1, len(tasks)):
    #     img1 = Utils.load_image(os.path.join('E:\PycharmProject\Feature\dog', image_list[i]))
    #     img1 = img1.reshape((1, 224, 224, 3))
    #     batch = np.concatenate((batch, img1), 0)
    true_result = np.zeros((len(truth), 1000), dtype=int)
    for i in range(len(truth)):
        true_result[i, bird_class_index[truth[i]]] = 1
    return true_result


def fine_tune(batch, true_result, num):
    with tf.device('/cpu:0'):
        tf.reset_default_graph()
        with tf.Session() as sess:

            images = tf.placeholder(tf.float32, [num, 224, 224, 3])
            true_out = tf.placeholder(tf.float32, [num, 1000])
            train_mode = tf.placeholder(tf.bool)

            vgg = vgg19.Vgg19('./test_save.npy')
            vgg.build(images, train_mode)

            # print number of variables used: 143667240 variables, i.e. ideal size = 548MB
            # print vgg.get_var_count()

            # init = tf.initialize_all_variables()
            #
            # sess.run(init)
            sess.run(tf.global_variables_initializer())
            # sess.run(tf.global_variables_initializer())

            # test classification
            # prob = sess.run(vgg.prob, feed_dict={images: batch1, train_mode: False})
            # Utils.print_prob(prob[0], './synset.txt')

            # simple 1-step training
            cost = tf.reduce_sum((vgg.prob - true_out) ** 2)
            train = tf.train.GradientDescentOptimizer(0.0001).minimize(cost)
            sess.run(train, feed_dict={images: batch, true_out: true_result, train_mode: True})

            # test classification again, should have a higher probability about tiger
            # prob = sess.run(vgg.prob, feed_dict={images: batch1, train_mode: False})
            # Utils.print_prob(prob[0], './synset.txt')

            # test save
            vgg.save_npy(sess, './test_save.npy')
        tf.get_default_graph().finalize()
