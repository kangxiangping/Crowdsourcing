# README

本项目是基于Django开发的众包平台。

## 软件环境

+ python 3.6.2
+ django 3.1.7
+ tensorflow 1.8.0
+ numpy 1.16.2
+ pandas 1.0.5
+ pymysql 1.0.2
+ cv2 4.5.2
+ scikit-learn 0.18.1
+ scipy 1.1.0
+ scikit-image 0.17.2
+ mysql 5.7.34

在虚拟环境中切换至requirements.txt所在的目录，执行如下命令即可安装所需要的的库

```python
pip install -r requirements.txt
```



## 如何运行代码

首先在OnlineCrowd/OnlineCrowd/settings.py中配置mysql数据库的连接，然后切换至manage.py所在的目录，首先执行

```python
python manage.py makemigrations
```

然后在执行

```python
python manage.py migrate
```

以上两条命令是用来生成数据库中的表，项目中提取图片特征使用的是VGG-19，所以需要下载保存模型参数的npy文件并放入至项目的 static/data文件夹中，链接如下：

[VGG-19.npy](https://mega.nz/#!xZ8glS6J!MAnE91ND_WyfZ_8mvkuSa2YcA7q-1ehfSm-Q1fxOvvs)

下载完毕后执行如下命令启动Django服务器

```python
python manage.py runserver
```

服务器启动成功之后，访问127.0.0.1:8000即可使用众包平台。