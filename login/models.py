from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        db_table = 'user'  # 默认表名： 应用名_模型类名小写
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=20, null=False)
    nickname = models.CharField(max_length=20,  null=False)
    type = models.IntegerField()
    point = models.IntegerField()
    finishedCount = models.IntegerField()
    haveTest = models.IntegerField()
    assignedTasks = models.CharField(max_length=100, null=True)


