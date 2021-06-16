from django.shortcuts import render
from project.models import *
from dataset.models import *
from django.http import FileResponse
import pandas as pd
from django.conf import settings


#工具类方法

def getTruth2(taskId): #根据任务id，获取对应图片的名字，获得真值，对应不同的数据调用不同的方法即可
    task = Task.objects.get(id=taskId)
    picture = Picture.objects.get(id=task.pictureId_id)
    name = picture.name
    dict = {"n02108551": '藏獒', 'n02110063': '阿拉斯加', 'n02110185': '哈士奇', 'n02111277': '纽芬兰犬'}
    return dict[name.split('_')[0]]


def getTruth3(taskId):  # 根据任务id，获取对应图片的名字，获得真值，对应不同的数据调用不同的方法即可
   task = Task.objects.get(id=taskId)
   picture = Picture.objects.get(id=task.pictureId_id)
   name = picture.name
   dict = {"n02110958": '巴哥犬', 'n02085620': '吉娃娃', 'n02106166': '边牧', 'n02111277': '纽芬兰犬'}
   return dict[name.split('_')[0]]

def getTruth(taskId):  # 根据任务id，获取对应图片的名字，获得真值，对应不同的数据调用不同的方法即可
   task = Task.objects.get(id=taskId)
   picture = Picture.objects.get(id=task.pictureId_id)
   name = picture.name
   dict = {"n02085936": '马耳他犬', 'n02088364': '猎兔犬', 'n02091134': '小灵狗', 'n02087046': '玩具梗'}
   return dict[name.split('_')[0]]
# Create your views here.

def export(request):
   projects = Project.objects.all().order_by('id')
   context = {'projects': projects}
   return render(request, 'login/export.html', context)

def download(request, project_id): #进行答案聚合，并且生成excel，保存到文件中
   project = Project.objects.get(id=project_id)
   tags = project.tag.split(";")

   df = pd.DataFrame(columns=["name", "answer"])

   media_root = settings.MEDIA_ROOT
   path = media_root + 'predict/'
   fileName = str(project_id) + '.csv'
   S = pd.read_csv(path + fileName, index_col=0)

   tasks = Task.objects.filter(projectId_id=project_id)
   for task in tasks:
      if task.gold==0:
         probab = S.loc[task.id].tolist()
         if len(set(probab)) == 1:
            pass
         else:
            task.truth=tags[int(S.loc[task.id].idxmax())-1]
      picture = Picture.objects.get(id=task.pictureId_id)
      df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)


   media_root = settings.MEDIA_ROOT
   path = media_root + '/answers/'
   fileName = str(project_id)+project.description+'.xlsx'
   df.to_excel(path+fileName, index=None)
   file = open(path+fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = project.description+'.xlsx'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   return response



def annotations(request, project_id): #输出工人标注数据
   # project = Project.objects.get(id=project_id)
   # tags = project.tag.split(";")
   #
   # df = pd.DataFrame(columns=["name", "answer"])
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + 'predict/'
   # fileName = str(project_id) + '.csv'
   # S = pd.read_csv(path + fileName, index_col=0)
   #
   # tasks = Task.objects.filter(projectId_id=project_id)
   # for task in tasks:
   #    if task.gold==0:
   #       task.truth=tags[int(S.loc[task.id].idxmax())-1]
   #    picture = Picture.objects.get(id=task.pictureId_id)
   #    df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)
   #
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + '/answers/'
   # fileName = str(project_id)+project.description+'.xlsx'
   # df.to_excel(path+fileName, index=None)
   # file = open(path+fileName, 'rb')
   # response = FileResponse(file)
   # response['Content-Type'] = 'application/octet-stream'
   # name = project.description+'.xlsx'
   # response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   # # return response

   project = Project.objects.get(id=project_id)
   tags = project.tag.split(";")

   workers = Workers.objects.filter(projectId_id=project_id)
   workersId = [worker.worker_id for worker in workers]

   tasks = Task.objects.filter(projectId_id=project_id).order_by('id')
   taskId = [task.id for task in tasks]


   labels = pd.DataFrame(index=workersId, columns=taskId)  # 这个workersID应该从那个quality里面查询
   labels.fillna(0, inplace=True)
   finisheds = Finished.objects.filter(projectId_id=project_id)
   for finshed in finisheds:
      labels.loc[finshed.userid_id][finshed.taskid_id] = tags.index(finshed.answer) + 1



   pictures = []
   for t in tasks:
      picture = Picture.objects.get(id=t.pictureId_id)
      pictures.append(picture.name)

   labels.columns = pictures

   media_root = settings.MEDIA_ROOT
   path = media_root + '/annotations/'
   fileName = str(project_id) + '_annotaions.csv'
   labels.to_csv(path + fileName)
   file = open(path + fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = str(project_id) + '_annotaions.csv'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   return response


#希望能下载到finished数据

def annotations_batch(request, project_id): #输出工人标注数据
   # project = Project.objects.get(id=project_id)
   # tags = project.tag.split(";")
   #
   # df = pd.DataFrame(columns=["name", "answer"])
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + 'predict/'
   # fileName = str(project_id) + '.csv'
   # S = pd.read_csv(path + fileName, index_col=0)
   #
   # tasks = Task.objects.filter(projectId_id=project_id)
   # for task in tasks:
   #    if task.gold==0:
   #       task.truth=tags[int(S.loc[task.id].idxmax())-1]
   #    picture = Picture.objects.get(id=task.pictureId_id)
   #    df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)
   #
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + '/answers/'
   # fileName = str(project_id)+project.description+'.xlsx'
   # df.to_excel(path+fileName, index=None)
   # file = open(path+fileName, 'rb')
   # response = FileResponse(file)
   # response['Content-Type'] = 'application/octet-stream'
   # name = project.description+'.xlsx'
   # response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   # # return response

   finisheds = Finished.objects.filter(projectId_id=project_id)

   df = pd.DataFrame(columns=['workerID', 'taskID', 'name', 'answer', 'batch', 'method'])
   for finish in finisheds:
      taskID = finish.taskid_id
      task = Task.objects.get(id=taskID)
      picture = Picture.objects.get(id = task.pictureId_id)
      name = picture.name
      df = df.append([{'workerID': finish.userid_id, 'taskID': finish.taskid_id, 'name': name, 'answer': finish.answer, 'batch': finish.batch, 'method': finish.method}],
                                 ignore_index=True)

   media_root = settings.MEDIA_ROOT
   path = media_root + '/annotations/'
   fileName = str(project_id) + '_annotaions_batch.xlsx'
   df.to_excel(path + fileName)
   file = open(path + fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = str(project_id) + '_annotaions_batch.xlsx'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))

   return response


def taskDiff(request, project_id):  # 输出工人标注数据
   # project = Project.objects.get(id=project_id)
   # tags = project.tag.split(";")
   #
   # df = pd.DataFrame(columns=["name", "answer"])
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + 'predict/'
   # fileName = str(project_id) + '.csv'
   # S = pd.read_csv(path + fileName, index_col=0)
   #
   # tasks = Task.objects.filter(projectId_id=project_id)
   # for task in tasks:
   #    if task.gold==0:
   #       task.truth=tags[int(S.loc[task.id].idxmax())-1]
   #    picture = Picture.objects.get(id=task.pictureId_id)
   #    df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)
   #
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + '/answers/'
   # fileName = str(project_id)+project.description+'.xlsx'
   # df.to_excel(path+fileName, index=None)
   # file = open(path+fileName, 'rb')
   # response = FileResponse(file)
   # response['Content-Type'] = 'application/octet-stream'
   # name = project.description+'.xlsx'
   # response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   # # return response

   tasks = Task.objects.filter(projectId_id=project_id)
   taskIDs = [task.id for task in tasks]
   #返回一个csv, id是task的id，只有一列是任务的难度
   df = pd.DataFrame(columns=['diff'], index=taskIDs)
   for task in tasks:
      df.loc[task.id]['diff'] = task.difficulty

   media_root = settings.MEDIA_ROOT
   path = media_root + '/quality/'
   fileName = str(project_id) + '_task_difficulty.csv'
   df.to_csv(path + fileName)
   file = open(path + fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = str(project_id) + '_task_difficulty.csv'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))

   return response

def quality(request, project_id): #acc和acc_diff都在最后统一进行计算，免得中间计算还要搞字符串的准确率，比较麻烦
   # project = Project.objects.get(id=project_id)
   # tags = project.tag.split(";")
   #
   # df = pd.DataFrame(columns=["name", "answer"])
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + 'predict/'
   # fileName = str(project_id) + '.csv'
   # S = pd.read_csv(path + fileName, index_col=0)
   #
   # tasks = Task.objects.filter(projectId_id=project_id)
   # for task in tasks:
   #    if task.gold==0:
   #       task.truth=tags[int(S.loc[task.id].idxmax())-1]
   #    picture = Picture.objects.get(id=task.pictureId_id)
   #    df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)
   #
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + '/answers/'
   # fileName = str(project_id)+project.description+'.xlsx'
   # df.to_excel(path+fileName, index=None)
   # file = open(path+fileName, 'rb')
   # response = FileResponse(file)
   # response['Content-Type'] = 'application/octet-stream'
   # name = project.description+'.xlsx'
   # response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   # # return response

   project = Project.objects.get(id=project_id)

   workers = Workers.objects.filter(projectId_id=project_id)
   workersId = [worker.worker_id for worker in workers]

   #统计每个工人在各个批次的准确率（不考虑任务难度）
   acc_dict = {}
   for worker in workers:
      batch = worker.batch #这个batch实际是一下批次，但是是从0开始的，所以也是当前总共的批次数目
      acc_list =[]
      for i in range(batch):
          correct = 0
          finisheds = Finished.objects.filter(projectId_id=project_id, userid_id=worker.worker_id, batch=i)
          total = len(finisheds)
          if total != 0: #如果等于0，则直接跳过，计算下一批次的准确率
             for finish in finisheds:
                if finish.answer == getTruth(finish.taskid_id):
                   correct += 1
             acc_list.append(correct/total)
      acc_dict[worker.worker_id] = acc_list

   quality = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in acc_dict.items()]))


   # for worker in workers:
   #    qws = worker.acc
   #    qws_split = qws.split(";")
   #    qws_strip = qws_split[:len(qws_split)-1]
   #    qws_float = [float(qu) for qu in qws_strip]
   #    quality[worker.worker_id] = pd.Series(qws_float)

   media_root = settings.MEDIA_ROOT
   path = media_root + '/quality/'
   fileName = str(project_id) + '_acc.csv'
   quality.to_csv(path + fileName)
   file = open(path + fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = str(project_id) + '_acc.csv'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   return response



def quality_diff(request, project_id): #考虑任务难度，来统计工人准确率，这里只是多考虑了任务难度，其他的全都不用变
   # project = Project.objects.get(id=project_id)
   # tags = project.tag.split(";")
   #
   # df = pd.DataFrame(columns=["name", "answer"])
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + 'predict/'
   # fileName = str(project_id) + '.csv'
   # S = pd.read_csv(path + fileName, index_col=0)
   #
   # tasks = Task.objects.filter(projectId_id=project_id)
   # for task in tasks:
   #    if task.gold==0:
   #       task.truth=tags[int(S.loc[task.id].idxmax())-1]
   #    picture = Picture.objects.get(id=task.pictureId_id)
   #    df = df.append({'name': picture.name, 'answer': task.truth}, ignore_index=True)
   #
   #
   # media_root = settings.MEDIA_ROOT
   # path = media_root + '/answers/'
   # fileName = str(project_id)+project.description+'.xlsx'
   # df.to_excel(path+fileName, index=None)
   # file = open(path+fileName, 'rb')
   # response = FileResponse(file)
   # response['Content-Type'] = 'application/octet-stream'
   # name = project.description+'.xlsx'
   # response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   # # return response

   project = Project.objects.get(id=project_id)

   workers = Workers.objects.filter(projectId_id=project_id)
   workersId = [worker.worker_id for worker in workers]

   # 统计每个工人在各个批次的准确率（考虑任务难度）
   acc_dict = {}
   for worker in workers:
      batch = worker.batch  # 这个batch实际是一下批次，但是是从0开始的，所以也是当前总共的批次数目
      acc_list = []
      for i in range(batch):
         correct = 0
         finisheds = Finished.objects.filter(projectId_id=project_id, userid_id=worker.worker_id, batch=i)
         total = 0
         for finish in finisheds:
            difficulty = Task.objects.get(id=finish.taskid_id).difficulty
            total += difficulty
            if finish.answer == getTruth(finish.taskid_id):
               correct += difficulty
         if total != 0: # 如果等于0，则直接跳过，计算下一批次的准确率
            acc_list.append(correct/total)
      acc_dict[worker.worker_id] = acc_list

   quality = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in acc_dict.items()]))



   media_root = settings.MEDIA_ROOT
   path = media_root + '/quality/'
   fileName = str(project_id) + '_acc_difficulty.csv'
   quality.to_csv(path + fileName)
   file = open(path + fileName, 'rb')
   response = FileResponse(file)
   response['Content-Type'] = 'application/octet-stream'
   name = str(project_id) + '_acc_difficulty.csv'
   response['Content-Disposition'] = 'attachment; filename={}'.format(name.encode('utf8').decode('ISO-8859-1'))
   return response






