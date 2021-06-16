from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dataset.models import Dataset
import os
import time
# Create your views here.

def datasets(request):
    user = request.session['user']
    datasets = Dataset.objects.filter(creator_id=user.id)
    context = {'datasets': datasets, 'datasetCount': "共"+str(len(datasets))+"个"}
    return render(request, 'login/dataset.html', context)

@csrf_exempt #增加装饰器，作用是跳过 csrf 中间件的保护
def createDataset(request):
    name = request.POST.get('name', None)
    user = request.session['user']
    if name:
        obj = Dataset(name=name, creator_id=user.id, imgCount=0, isUsed=0)
        obj.save()
    return redirect('/dataset')

def dataset(request, dataset_id): #这是数据集的id，来查询其中包含的数据，在此处需要进行参数填充
    pictures = Picture.objects.filter(datasetId_id=dataset_id)
    context = {'pictures': pictures, 'pictureCount': "共" + str(len(pictures)) + "个", 'dataset_id': dataset_id}
    return render(request, 'login/data.html', context)

@csrf_exempt #增加装饰器，作用是跳过 csrf 中间件的保护
def uploadImg(request, dataset_id):
    files = request.FILES.getlist('pictureFiles')  # 返回一个列表
    if len(files):
        media_root = settings.MEDIA_ROOT
        path = 'pictures/{}/'.format(dataset_id)
        full_path = media_root + path
        print('full_path', full_path)
        if not os.path.exists(full_path):
            print("not exist")
            os.makedirs(full_path)
        for file in files:
            with open(full_path + file.name, 'wb') as pic:
                for c in file.chunks():
                    pic.write(c)
            obj = Picture(url='media/' + path + file.name, datasetId_id=dataset_id, name=file.name)
            obj.save()
        pictures = Picture.objects.filter(datasetId_id=dataset_id)
        dataset = Dataset.objects.get(id=dataset_id)
        dataset.coverUrl = pictures[0].url
        dataset.imgCount += len(files)
        dataset.save()
        context = {'pictures': pictures, 'pictureCount': "共" + str(len(pictures)) + "个",  'dataset_id': dataset_id}
        return render(request, 'login/data.html', context)
    context = {'pictureCount': "共0个", 'dataset_id': dataset_id}
    return render(request, 'login/data.html', context)

def deleteDataset(request, id):
    obj = Dataset.objects.get(id=id)
    obj.delete()
    return datasets(request)


def deletePicture(request, id, datasetId):  #就是因为没有修改图片数量，导致后面一系列的bug
    obj = Picture.objects.get(id=id)
    url = obj.url
    path = 'static/' + url
    os.remove(path)
    obj.delete()

    dataset2 = Dataset.objects.get(id=datasetId)
    imgCount = len(Picture.objects.filter(datasetId_id=datasetId))
    dataset2.imgCount=imgCount
    dataset2.save()
    return dataset(request, datasetId)