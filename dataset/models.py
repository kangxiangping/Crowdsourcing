from login.models import User
from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Dataset(models.Model):
    class Meta:
        db_table = 'dataset'  # 默认表名： 应用名_模型类名小写
    id = models.AutoField(primary_key=True)
    coverUrl = models.CharField(max_length=100, unique=True, null=False)
    creator = models.ForeignKey(User,  on_delete=models.CASCADE)
    gmtCreate = models.DateTimeField(default=timezone.now)
    imgCount = models.IntegerField()
    isUsed = models.IntegerField()
    name = models.CharField(max_length=100, null=False)


class Picture(models.Model):
    class Meta:
        db_table = 'picture'
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100, unique=True, null=False)
    datasetId = models.ForeignKey(Dataset,  on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)



