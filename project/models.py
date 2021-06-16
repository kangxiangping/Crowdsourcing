from django.db import models
from dataset.models import Dataset,Picture
from login.models import User
import django.utils.timezone as timezone
# Create your models here.

class Project(models.Model):
    class Meta:
        db_table = 'project'  # 默认表名： 应用名_模型类名小写
    id = models.AutoField(primary_key=True)
    deadline = models.DateField()
    name = models.CharField(max_length=20)
    taskCount = models.IntegerField(null=True)
    finishedCount = models.IntegerField(null=True) #表示总共的标注次数
    point = models.IntegerField()
    gmtCreate = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    datasetId = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    budget = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    imgUrl = models.CharField(max_length=100)
    workerNum = models.IntegerField(default=0)
    hasFinished = models.IntegerField(default=0)
    goldNum = models.IntegerField(default=0)
    batchNum = models.IntegerField(default=0)


class Task(models.Model):
    class Meta:
        db_table = 'task'
    id = models.AutoField(primary_key=True)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE)
    pictureId = models.ForeignKey(Picture, on_delete=models.CASCADE)
    truth = models.CharField(max_length=100)
    difficulty = models.FloatField(null=True)
    gold = models.IntegerField(default=0)




class Finished(models.Model):
    class Meta:
        db_table = 'finished'
    id = models.AutoField(primary_key=True)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE)
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    batch = models.IntegerField(default=0) #记录此项纪录是工人在第几批次完成的
    method = models.IntegerField(default=0) #记录是由哪一个分配方法得到的注释1,2,3，4


class Workers(models.Model):
    class Meta:
        db_table = 'Workers'
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE)
    batch = models.IntegerField(default=0)
    qw = models.FloatField(null=True)
    # acc = models.CharField(max_length=2000, default="")
    # acc_diff = models.CharField(max_length=2000, default="")

