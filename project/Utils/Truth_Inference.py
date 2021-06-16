import numpy as np
import pandas as pd

def truth_inference(labels, S, tasks, workers, classes, goldTasks): #labels是标注数据，tasks是任务的难度，workers是工人的能力，classes是类别数, tasks和workers是pandas的series
    # S = pd.DataFrame(index=labels.columns, columns=[i for i in range(1, classes+1)]).fillna(0, inplace=True)
    go = True #注意S的列索引是string类型的，在E步，不需要对golden tasks进行推理，但是在M步依旧可以用
    unGold = []
    for id in labels.columns:
        if id not in goldTasks:
            unGold.append(id)
    iter = 0
    while(go and iter<=20):
        # E 步骤
        for task in unGold:
            for j in range(1, classes+1):
                S_ij = 1
                for worker in workers.index:
                    if labels.loc[worker][task]==0:
                        pass
                    elif labels.loc[worker][task]==j:
                        S_ij *= 1/(1+np.exp(-workers[worker]/tasks[task]))
                    else:
                        S_ij *= (1-(1 / (1 + np.exp(-workers[worker] / tasks[task]))))/(classes-1)
                # S.loc[task][j] = S_ij if S_ij<1 else 0
                if S_ij<1:
                    S.loc[task][str(j)] = S_ij
                else:
                    pass  #如果任务没有答案的话，应该保持原样而不能设为0
            sigma = sum(S.loc[task])
            if sigma != 0:
                for j in range(1, classes+1):
                  S.loc[task][str(j)] = S.loc[task][str(j)]/sigma

        # M步骤，这一步骤，那些goldTask依然可以用来计算
        go = False
        for worker in workers.index:
            qw = 0
            sig = 0
            for task in labels.columns:
                if labels.loc[worker][task]!=0:
                    qw += S.loc[task][str(labels.loc[worker][task])] * tasks[task]
                    sig += tasks[task]
            # if workers[worker] != qw/sig: #如果让相等的话，可能迭代次数较多
            if sig!=0:
                if abs(workers[worker] - qw/sig)>10**-2:
                    go = True

                workers[worker] = qw/sig
        iter += 1
    return S, workers
    #有一个问题就是qw的更新，我们这里是全局再次推理的，似乎不需要进行更新
    #S是更新的概率矩阵，workers是新的工人能力






