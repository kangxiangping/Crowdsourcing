from django.shortcuts import render
from . import models
from django.views.decorators.csrf import csrf_exempt
import time
from dataset.models import Dataset, Picture
import datetime
import os
import pandas as pd
from django.conf import settings
# Create your views here.
from .Utils import selfpaced
from .Utils import Task_Assignment
from .Utils import Truth_Inference
from .Utils import Task_difficulty
from login import views
from login import models as lgModels
from django.http import JsonResponse



def index(request):
    # projects = models.Project.objects.all()
    # context = {'projects': projects}
    return views.index(request) #这个是django里面找HTML的路径，不是html的方式



def step1(request):
    return render(request, 'login/createProject1.html')

@csrf_exempt
def step2(request):
    name = request.POST.get('name', None)
    description = request.POST.get('description', None)
    point = request.POST.get('point', None)
    budget = request.POST.get('budget', None)
    deadline = request.POST.get('deadline', None)
    if name and point and budget and deadline:
        user = request.session['user']

        u = lgModels.User.objects.get(id=user.id)
        u.point = u.point - int(budget)
        u.save()  # 如果积分不够的话会减成负的，所以这个地方也得注意，加一个alert，但是咱就暂时不考虑了，因为比较麻烦

        timeArray = time.strptime(deadline, "%Y-%m-%dT%H:%M")
        timeStamp = int(time.mktime(timeArray))
        value = datetime.datetime.fromtimestamp(timeStamp)
        obj = models.Project(name=name, description=description,  point=point, budget=budget, deadline=value, creator_id=user.id)
        obj.save()


        datasets = Dataset.objects.filter(creator_id=user.id)
        context = {'datasets': datasets, 'project_id': obj.id}
        return render(request, 'login/createProject2.html', context)
    else:
        return render(request, 'login/createProject1.html')

@csrf_exempt
def step3(request, project_id):
    dataset_id = request.POST.get('selectedDataset', None)
    project = models.Project.objects.get(id=project_id)
    project.datasetId_id = dataset_id
    dataset = Dataset.objects.get(id=dataset_id)
    dataset.isUsed = 1
    project.imgUrl = dataset.coverUrl
    project.taskCount = dataset.imgCount
    project.save()
    context = {'project_id': project_id}
    return render(request, 'login/createProject3.html', context)



@csrf_exempt
def finish(request, project_id):
    type = "单标记"
    question = request.POST.get('question', None)
    tag = request.POST.get('tag', None)
    goldNum = request.POST.get('goldNum', None)
    batchNum = request.POST.get('batchNum', None)

    project = models.Project.objects.get(id=project_id)
    dataset_id = project.datasetId_id
    dataset = Dataset.objects.get(id=dataset_id)
    project.type = type
    project.question = question
    project.tag = tag
    project.finishedCount = 0
    project.taskCount = dataset.imgCount
    project.goldNum = int(goldNum)
    project.batchNum = int(batchNum)
    project.save()

    pictures = Picture.objects.filter(datasetId=dataset_id)
    for picture in pictures:
        models.Task(projectId_id=project_id, pictureId_id=picture.id).save()







    index = 0
    tasks = models.Task.objects.filter(projectId_id=project_id).order_by('id')
    tasksId = [task.id for task in tasks]
    #之后需要在此处选择具有代表性的任务作为golden tasks，暂时随机选择goldNum个任务，就是此处，每个簇中选择最靠近中心点的任务，数量和这一簇的数量成正比
    #现在已经存放到每个人对应的字段中，现在只需要把id存放到ordered_task就行了，应该在特征提取之后

    # 创建项目时，还需要提取图片的特征，存储为相应的文件

    # 首先生成batch数据,tasks是项目中所有的任务
    fileList = []
    for batch_task in tasks:
        url = models.Picture.objects.get(id=batch_task.pictureId_id).url
        fileList.append('static/' + url)
    batch = selfpaced.data_procesing(fileList)  # batch中数据和taskID是依次对应的
    feature = selfpaced.Selfpaced(tasksId, batch)  # 提取出对应图片的特征，pd.Dataframe,行索引是taskID
    media_root = settings.MEDIA_ROOT
    path = media_root + 'feature/'
    fileName = str(project_id) + '.csv'
    feature.to_csv(path + fileName)

    #feature 就是提取的特征，行索引是taskId


    goldNum2 = int(goldNum)

    classes = len(tag.split(';'))
    # 需要生成golden tasks，存放到每个人的对应字段中
    ordered_tasks = selfpaced.goldTaskSelected(feature, classes, len(tasks), goldNum2)

    for i in range(goldNum2):
        obj = models.Task.objects.get(id=ordered_tasks[i])
        obj.gold = 1
        obj.save()

    u = request.session['user']
    user = lgModels.User.objects.get(id=u.id)
    s = ""
    for j in range(len(ordered_tasks)):
        s += str(int(ordered_tasks[j]))
        if j < len(ordered_tasks)-1:
            s += ";"
    user.assignedTasks = s
    user.save()


    task_str = user.assignedTasks
    task_str_split = task_str.split(';')
    ordered_tasks = [int(tID) for tID in task_str_split]


    task = models.Task.objects.get(id=ordered_tasks[index])
    picture = Picture.objects.get(id=task.pictureId_id)
    imgUrl = picture.url
    question = project.question
    type = project.type
    tags = project.tag.split(";")
    context = {'index': index + 1, 'taskId': task.id, 'projectId': project_id, 'imgUrl': imgUrl, 'question': question,
               'type': type, 'tags': tags, 'taskCount': goldNum2, 'batch': -1}

    # 创建项目时，也需要创建项目的S文件，是csv文件, S.csv是存放目前答案的概率分布的，类别与数字对应关系就是tag中的序号 tags = project.tag.split(";")
    S = pd.DataFrame(index=[t.id for t in tasks], columns=[i+1 for i in range(len(tags))])
    S.fillna(1/len(tags), inplace=True)
    media_root = settings.MEDIA_ROOT
    path = media_root + 'predict/'
    fileName = str(project_id) + '.csv'
    S.to_csv(path + fileName)



    return render(request, 'login/working.html', context)





def begin(request, project_id): #在此处嵌入任务分配算法

    index = 0
    project = models.Project.objects.get(id=project_id)
    tags = project.tag.split(";")
    user = request.session['user']

    try:
        models.Workers.objects.get(projectId_id=project_id, worker_id=user.id) #有工作记录，就正常分配，如果没找到说明是第一次，应该分配golden tasks
        tasks = models.Task.objects.filter(projectId_id=project_id).order_by('id')
        taskId = [task.id for task in tasks]
        media_root = settings.MEDIA_ROOT
        path = media_root + 'predict/'
        fileName = str(project_id) + '.csv'
        S = pd.read_csv(path + fileName, index_col=0)
        workers = models.Workers.objects.filter(projectId_id=project_id)
        workersId = [worker.worker_id for worker in workers]
        labels = pd.DataFrame(index=workersId, columns=taskId)  # 这个workersID应该从那个quality里面查询
        labels.fillna(0, inplace=True)
        finisheds = models.Finished.objects.filter(projectId_id=project_id)
        for finshed in finisheds:
            labels.loc[finshed.userid_id][finshed.taskid_id] = tags.index(finshed.answer) + 1
        classes = len(tags)
        workerID = user.id
        # k值也设置成任务的25%, 这个k是分配的任务数目
        k = project.batchNum

        tasks_diff = pd.Series(index=taskId)
        for task in tasks:
            tasks_diff[task.id] = task.difficulty

        workers_qw = pd.Series(index=workersId)
        for worker in workers:
            workers_qw[worker.worker_id]=worker.qw

        #分配任务时还要考虑任务的预算

        max = project.budget//project.point

        if k > max:
            k = max

        ordered_tasks = []
        #这里并行的采用四种方法，所以每个方法就分配k//4个任务即可
        #顺序是SPCrowd, CrowdWT, Random, iCrowd
        #这一个分配两个方法的，前5个是SP，后5个是crowdWT
        ordered_tasks.extend(Task_Assignment.task_assignment(labels, S, workers_qw, tasks_diff, k//2, classes, workerID))

        #Random
        ordered_tasks.extend(Task_Assignment.Crowd_Random(labels, S, workers_qw, tasks_diff, k//4, classes, workerID, ordered_tasks))

        #iCrowd
        ordered_tasks.extend(
            Task_Assignment.iCrowd(labels, S, workers_qw, tasks_diff, k // 4, classes, workerID, ordered_tasks))




        user_db = lgModels.User.objects.get(id=user.id)
        s = ""
        for j in range(len(ordered_tasks)):
            s += str(int(ordered_tasks[j]))
            if j < len(ordered_tasks) - 1:
                s += ";"
        user_db.assignedTasks = s
        user_db.save()



        if len(ordered_tasks)==0:
            projects = models.Project.objects.all()
            for project in projects:
                finished = models.Finished.objects.filter(userid_id=user.id, projectId_id=project.id)
                project.finishedCount = len(finished)
            context = {'projects': projects, 'message': '任务已全部完成', 'uid': user.id}
            return render(request, 'login/index.html', context)

    # 需要生成有序的任务列表,简单的排在前面
    except Exception as r:  #分配golden tasks之后就应该在workers中添加其对应的一项
        print(r)
        goldTasks = models.Task.objects.filter(projectId_id=project_id, gold=1)

        ordered_tasks = [goldTask.id for goldTask in goldTasks]

        user_db = lgModels.User.objects.get(id=user.id)
        s = ""
        for j in range(len(ordered_tasks)):
            s += str(int(ordered_tasks[j]))
            if j < len(ordered_tasks) - 1:
                s += ";"
        user_db.assignedTasks = s
        user_db.save()

        models.Workers(projectId_id=project_id, worker_id=user.id, qw=0).save()
        project.workerNum = project.workerNum + 1
        project.save()

    user_db = lgModels.User.objects.get(id=user.id)
    task_str = user_db.assignedTasks
    task_str_split = task_str.split(';')
    ordered_tasks = [int(tID) for tID in task_str_split]

    task = models.Task.objects.get(id=ordered_tasks[index])
    picture = Picture.objects.get(id=task.pictureId_id)
    imgUrl = picture.url
    question = project.question
    type = project.type

    # 获取工人正在进行第几个batch，但是注意，任务发布者也有working页面，不会出现在workers表中，所以没有batch，要注意
    try:
        batch = models.Workers.objects.get(projectId_id=project_id, worker_id=user.id).batch
    except Exception as r:
        batch = -1

    context = {'index': index+1, 'taskId': task.id, 'projectId': project_id, 'imgUrl': imgUrl, 'question': question, 'type': type, 'tags': tags, 'taskCount': len(ordered_tasks), 'batch': batch}
    return render(request, 'login/working.html', context)


def working(request, project_id, index):
    project = models.Project.objects.get(id=project_id)

    user = request.session['user']
    user_db = lgModels.User.objects.get(id=user.id)
    task_str = user_db.assignedTasks
    task_str_split = task_str.split(';')
    ordered_tasks = [int(tID) for tID in task_str_split]

    task = models.Task.objects.get(id=ordered_tasks[index])
    picture = Picture.objects.get(id=task.pictureId_id)
    imgUrl = picture.url
    question = project.question
    type = project.type
    tags = project.tag.split(";")

    #获取工人正在进行第几个batch，但是注意，任务发布者也有working页面，不会出现在workers表中，所以没有batch，要注意
    try:
        batch = models.Workers.objects.get(projectId_id=project_id, worker_id=user.id).batch
    except Exception as r:
        batch = -1
    context = {'index': index+1,  'taskId': task.id, 'projectId': project_id, 'imgUrl': imgUrl, 'question': question, 'type': type, 'tags': tags, 'taskCount': len(ordered_tasks), 'batch': batch}
    return render(request, 'login/working.html', context)

import json
@csrf_exempt
def getAnswer(request):
    user = request.session['user']
    info = json.loads(request.body.decode('utf-8'))
    answer = info['answer']
    project_id = info['projectId']
    taskId = info['taskId']
    index = info['index']   #当是一批次的最后一个任务时，index=len(orderTasks)
    project = models.Project.objects.get(id=project_id)
    task = models.Task.objects.get(id=taskId)

    #此处，记录时也要记录是哪一个方法的注释数据
    if user.id != project.creator_id:
        try:
            finish = models.Finished.objects.get(taskid_id=taskId, userid_id=user.id)
            #这个地方注意了，由于我们加了反馈，所以对于工人再次提交的golden task答案不进行更新了
            if task.gold != 1:
                finish.answer = answer
                finish.save()

        except Exception as r:
            project.finishedCount = project.finishedCount+1 #这个是总共的标注次数
            project.budget = project.budget - project.point
            project.save()

            u = lgModels.User.objects.get(id=user.id)
            u.point = u.point + project.point
            u.finishedCount = u.finishedCount + 1
            u.save()

            batch = models.Workers.objects.get(projectId_id=project_id, worker_id=user.id).batch #这个worker是当前正在完成任务的worker， batch表示工人正在进行的批次
            #注意了，当前index就是任务的序号，从1开始，这里就限定了分配20个任务，不能改
            if index<=5:
                method = 1
            elif index<=10:
                method = 2
            elif index<=15:
                method= 3
            else:
                method= 4
            obj = models.Finished(taskid_id=taskId, answer=answer, projectId_id=project_id, userid_id=user.id, batch=batch, method=method)
            obj.save()


    if task.gold == 1 and project.creator_id == user.id:
        #此处是任务发布者在标注真值，还应该修改S文件
        task.truth = answer
        task.save()

        user_db = lgModels.User.objects.get(id=user.id)
        task_str = user_db.assignedTasks
        task_str_split = task_str.split(';')
        ordered_tasks = [int(tID) for tID in task_str_split]

        if index == len(ordered_tasks):
            media_root = settings.MEDIA_ROOT
            path = media_root + 'predict/'
            fileName = str(project_id) + '.csv'
            tags = project.tag.split(";")
            S = pd.read_csv(path + fileName, index_col=0) #注意列索引变成字符串了，行索引依旧是Int类型的
            for goldId in ordered_tasks:
                for j in range(1, len(tags)+1):
                    if j == tags.index(models.Task.objects.get(id=goldId).truth)+1:
                        S.loc[goldId][str(j)] = 1
                    else :
                        S.loc[goldId][str(j)] = 0
            S.to_csv(path + fileName)




    # 自己不能标注自己的众包任务，所以workers中不应该有任务发布者，并且gold=1,说明工人当前正在进行golden tasks，并且已经完成了，应该对qw进行初始化
    # 错误率是在工人上的错误率，所以任务发布者不需要统计错误率
    if user.id != project.creator_id:
        worker = models.Workers.objects.get(projectId_id=project_id, worker_id=user.id)
        if task.gold==1:
            finishedTask = models.Finished.objects.filter(userid_id=user.id, projectId_id=project_id)
            total = len(finishedTask)
            if total == project.goldNum: #等于golden任务数目
                correct = 0
                for finished  in finishedTask:
                    if finished.answer == models.Task.objects.get(id=finished.taskid_id, gold=1).truth:
                        correct += 1
                worker.qw = correct/total
                worker.batch += 1
                worker.save()

                #此处需要对golden tasks的错误率进行统计，然后预测所有任务的困难度
                goldenTasks = models.Task.objects.filter(projectId_id=project_id, gold=1)
                goldenTasksID = [goldtask.id for goldtask in goldenTasks]

                error_rate = pd.Series(index=goldenTasksID)
                for goldtaskId in goldenTasksID: #统计除了任务发布者之外，标注错误的概率
                    finishedGold = models.Finished.objects.filter(taskid_id=goldtaskId).exclude(userid_id=project.creator_id)
                    total_gold = len(finishedGold)
                    error = 0
                    for finishGold in finishedGold:
                        if finishGold.answer != models.Task.objects.get(id=finishGold.taskid_id).truth:
                            error+=1
                    error_rate[goldtaskId] = error/total_gold

                #获取所有任务的feature
                media_root = settings.MEDIA_ROOT
                path = media_root + 'feature/'
                fileName = str(project_id) + '.csv'
                feature = pd.read_csv(path + fileName, index_col=0)
                allTaskDifficulty= Task_difficulty.task_difficulty(feature, error_rate)
                for diffIndex in allTaskDifficulty.index:
                    obj = models.Task.objects.get(id=diffIndex)
                    obj.difficulty = allTaskDifficulty[diffIndex]
                    obj.save()
                #任务难度更新完毕
            #这个分支就是普通工人在标注golden tasks,获取对应真值，如果错误，则返回正确答案，并且提示特征，如果正确，则返回回答正确，此处完成后还要注意，工人再次提交正确答案不作数了
            truth = models.Task.objects.get(id=taskId, gold=1).truth
            if answer == truth:
                return JsonResponse({"msg": "right"})
            else:
                # return JsonResponse({"msg": "wrong", "truth": truth, "hint": "提示：\n 巴哥犬：脸部皱纹多 \n 吉娃娃：体型小且耳朵大 \n 边牧：黑白相间 \n 纽芬兰犬：被毛丰厚且全身黑色"})
                return JsonResponse({"msg": "wrong", "truth": truth,
                                     "hint": ""})



    #当完成一批次的任务之后，就需要进行真值推理，但是任务发布者在指定真值时，以及工人在完成初始任务时，不需要进行真值推理
    user_db = lgModels.User.objects.get(id=user.id)
    task_str = user_db.assignedTasks
    task_str_split = task_str.split(';')
    ordered_tasks = [int(tID) for tID in task_str_split]

    if index == len(ordered_tasks) and task.gold != 1:
        #获取project
        project = models.Project.objects.get(id=project_id)
        tags = project.tag.split(";")

        #获取任务难度，不会有缺失值
        tasks = models.Task.objects.filter(projectId_id=project_id).order_by('id')
        taskId = [task.id for task in tasks]
        tasks_difficulty = pd.Series(index=taskId)
        for task in tasks:
            tasks_difficulty[task.id] = task.difficulty





        #获取工人能力，不会有缺失值，每一个都有值
        workers = models.Workers.objects.filter(projectId_id=project_id)
        workersId = [worker.worker_id for worker in workers]
        workers_quality = pd.Series(index=workersId)
        for worker in workers:
            workers_quality[worker.worker_id] = worker.qw



        #获取labels
        labels = pd.DataFrame(index=workersId, columns=taskId)  # 这个workersID应该从那个quality里面查询
        labels.fillna(0, inplace=True)
        finisheds = models.Finished.objects.filter(projectId_id=project_id)
        for finshed in finisheds:
            labels.loc[finshed.userid_id][finshed.taskid_id] = tags.index(finshed.answer) + 1
        classes = len(tags)

        media_root = settings.MEDIA_ROOT
        path = media_root + 'predict/'
        fileName = str(project_id) + '.csv'
        S = pd.read_csv(path + fileName, index_col=0)

        goldTasks = models.Task.objects.filter(projectId_id=project_id, gold=1)
        goldTasksID = [gold.id for gold in goldTasks]


        new_S, new_Workers = Truth_Inference.truth_inference(labels, S, tasks_difficulty, workers_quality, classes, goldTasksID)

        new_S.to_csv(path + fileName)

        # 在完成一批次的任务之后，当前工人的批次需要加一,不仅是在这个完成普通任务之后批次加一，在完成golden task之后，批次也需要加一
        curWorker = models.Workers.objects.get(projectId_id=project_id, worker_id=user.id)
        curWorker.batch += 1
        curWorker.save()


        for workerId in new_Workers.index:
            obj = models.Workers.objects.get(worker_id=workerId, projectId_id=project_id)
            obj.qw = new_Workers[workerId]
            obj.save()

        #此处是对当前工人完成批次任务正确的比例进行统计，当前用户的id是user.id，统计完成之后把isCurrent置为0
        # curTasks = models.Finished.objects.filter(projectId_id=project_id, userid_id=user.id, isCurrent=1)
        # correct = 0
        # total = 0
        # for task in curTasks:
        #     total += 1
        #     if task.answer == getTruth(task.taskid_id):
        #         correct += 1
        #
        # #接下来是考虑任务难度统计正确率
        # cor_dif = 0
        # total_dif = 0
        # for task in curTasks:
        #     difficulty = models.Task.objects.get(id=task.taskid_id).difficulty
        #     total_dif += difficulty
        #     if task.answer == getTruth(task.taskid_id):
        #         cor_dif += difficulty
        #     # 防止出现上次那种情况，还是用id索引到对象
        #     obj = models.Finished.objects.get(taskid_id=task.taskid_id, userid_id=user.id)
        #     obj.isCurrent = 0
        #     obj.save()
        # assert total!=0
        # assert total_dif!=0
        # worker = models.Workers.objects.get(worker_id=user.id, projectId_id=project_id)
        # worker.acc += str(correct/total) + ";"
        # worker.acc_diff += str(cor_dif/total_dif) + ";"
        # worker.save()
    #如果是发布者标注，则不返回任何东西，如果是工人在标注golden task，就要返回真值
    #到了此处的话说明是其他情况，不用提示什么
    return JsonResponse({"msg": "nothing"})
    # return render(request, 'login/working.html')


def delete(request, id):
    try:
        obj = models.Project.objects.get(id=id)
        obj.delete()

        media_root = settings.MEDIA_ROOT
        path = media_root + 'predict/'
        fileName = str(id) + '.csv'
        os.remove(path + fileName)

        path = media_root+'feature/'
        fileName = str(id) + '.csv'
        os.remove(path + fileName)
    except:
        pass
    return index(request)


def finishProject(request, id):

    obj = models.Project.objects.get(id=id)
    obj.hasFinished = 1
    obj.save()

    return index(request)

