import pandas as pd
import numpy as np
import random
def entropy(prob):
    entropy = 0
    for i in range(len(prob)):
        if prob[i] == 0:
            prob[i] += 10**-2
        entropy += prob[i]*np.log(prob[i])
    return -entropy

def task_assignment(labels, S, workers, tasks, k, classes, workerID): #k是分配的任务数目，S是csv文件, workerID是当前请求任务的工人, workers和tasks是工人的能力和难度，是一个series
    Benefit = pd.DataFrame(columns=['taskID', 'benefit'])
    for task in labels.columns:
        if labels.loc[workerID][task] == 0:
            H_Si = entropy(S.loc[task])
            predict = {} #存放预测工人给出每一类别的概率
            for a in range(1, classes+1):
                predict[a] = S.loc[task][str(a)]*(1/(1+np.exp(-workers[workerID]/tasks[task]))) + (1-S.loc[task][str(a)])*(1-(1/(1+np.exp(-workers[workerID]/tasks[task]))))/(classes-1)
            H_Si_hat = 0

            for a in range(1, classes+1):
                s_i = np.zeros((classes,), dtype=float)
                for j in range(1, classes+1):
                    if j==a:
                        s_i[j-1] = S.loc[task][str(j)]*(1/(1+np.exp(-workers[workerID]/tasks[task])))
                    else :
                        s_i[j-1] = S.loc[task][str(j)]*(1-(1/(1+np.exp(-workers[workerID]/tasks[task]))))/(classes-1)
                sig = sum(s_i)
                for j in range(classes):
                    s_i[j] = s_i[j]/sig
                H_Si_hat += entropy(s_i) * predict[a]
            Benefit = Benefit.append({'taskID': task, 'benefit': H_Si- H_Si_hat }, ignore_index=True)
    Benefit = Benefit.sort_values(by="benefit", ascending=False)

    if Benefit.shape[0] > k:
        return Benefit[0:k]['taskID'].tolist()
    else:
        return Benefit['taskID'].tolist()


def Crowd_Random(labels, S, workers, tasks, k, classes, workerID, ordered_task):
    unassigned = []
    for task in labels.columns:
        if labels.loc[workerID][task] == 0:
            unassigned.append(task)
    unassigned = list(set(unassigned) - set(ordered_task))
    return random.sample(unassigned, k)

def iCrowd(labels, S, workers, tasks, k, classes, workerID, ordered_task):
    assigned = [] #这是已分配的任务列表
    for task in labels.columns:
        if labels.loc[workerID][task] != 0:
            assigned.append(task)
    #获取任务由简单到难的任务列表，再剔除掉已经分配的，然后再选择前k个
    order = tasks.sort_values(ascending=True)
    order_index = order.index
    to_assign = list(set(order_index) - set(assigned))
    return to_assign[:k]




