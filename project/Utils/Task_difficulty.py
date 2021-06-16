from sklearn.kernel_ridge import KernelRidge
import numpy as np
import pandas as pd
import copy
# y = [0.1, 0.2]
# X= [] #任务的特征
# for i in range(len(y)):
#     y[i] = -np.log(1 / y[i] - 1)
# clf = KernelRidge(alpha=10 ** -3, kernel='linear', gamma=None)
# clf.fit(X, y)

def task_difficulty(feature, error_rate):                                                            #feature是所有任务的特征(dataframe)，error_rate是golden tasks的错误率(series)，输出要求是所有任务的难度(series
    error_rate_save = copy.deepcopy(error_rate)
    for taskID in error_rate.index:
        if error_rate[taskID]==1:
            error_rate[taskID] = error_rate[taskID] - 10**-3
        if error_rate[taskID]==0:
            error_rate[taskID] = error_rate[taskID] + 10 ** -3
        error_rate[taskID] = -np.log(1 / error_rate[taskID] - 1)                                     #此处error_rate有可能=1，
    clf = KernelRidge(alpha=10 ** -3, kernel='linear', gamma=None)
    clf.fit(feature.loc[error_rate.index.tolist()], error_rate.to_list())
    toPredictTaskID = []
    for id in feature.index:
        if id not in error_rate.index:
            toPredictTaskID.append(id)
    predict = clf.predict(feature.loc[toPredictTaskID])
    for i in range(len(predict)):
        predict[i] = 1/(1+np.exp(-predict[i]))

    predict_Series = pd.Series(predict, index=toPredictTaskID)
    return pd.concat([error_rate_save, predict_Series], axis=0)


# def letgo(a):
#     a.loc[0]['value']=1
#     return a
#
# test = pd.DataFrame(index=[0], columns=['index', 'value'])
# test.fillna(0, inplace=True)
# print(test)
# test2 = letgo(test)
# print('new_test', test) #是引用，传入的参数会修改
# print(test2)

# test = pd.DataFrame([[1,2],[1,2],[1,2],[1,2]])
# print(test.loc[:2])
# print(test.loc[:2].shape)
#
# ser1 = pd.Series([1, 2], index=['a', 'b'])
# ser2 = pd.Series([3, 4], index=['c', 'd'])
# ser3 = pd.concat([ser1, ser2], axis=0)
# print(ser3)
