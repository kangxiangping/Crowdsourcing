from django.shortcuts import render, redirect
from . import models
from django.views.decorators.csrf import csrf_exempt
from project.models import Project
from project.models import Finished
# Create your views here.

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

@csrf_exempt #增加装饰器，作用是跳过 csrf 中间件的保护
def check_login(request):
    if request.method == "POST":
        userName = request.POST.get('username', None)
        passWord = request.POST.get('password', None)

        if userName and passWord:
            userName = userName.strip()
            try:
                user = models.User.objects.get(username=userName)
            except Exception as r:
                print(r)
                return render(request, 'login/register.html')
            if user.password == passWord:
                request.session['user'] = user
                request.session.set_expiry(0)
                return redirect('/')
                # render(request, 'login/index.html') #无法直接跳转，可能是被拦截了，但是好像没有拦截
    return render(request, 'login/login.html')

@csrf_exempt #增加装饰器，作用是跳过 csrf 中间件的保护
def check_register(request):
    if request.method == "POST":
        userName = request.POST.get('username', None)
        passWord = request.POST.get('password', None)
        nickName = request.POST.get('nickname', None)

        if userName and passWord and nickName:
            userName = userName.strip()
            try:
                user = models.User.objects.get(username=userName) #查询不到就会报错
            except Exception as r:
                print(r)
                obj = models.User(username=userName, password=passWord, nickname=nickName, type=0, point=0, finishedCount=0, haveTest=0)
                obj.save()
            return render(request, 'login/login.html')
    return render(request, 'login/register.html')

def index(request):
    user = request.session['user']
    projects = Project.objects.all()
    for project in projects:
        if project.creator_id == user.id: #应该显示已经完成了多少任务，只要有人标注过一个任务就算完成
            finished = Finished.objects.filter(projectId_id=project.id)
            taskID = [finish.taskid_id for finish in finished]
            project.finishedCount = len(set(taskID))
        else:
            finished = Finished.objects.filter(userid_id=user.id, projectId_id=project.id)
            project.finishedCount = len(finished)
    context = {'projects': projects, 'uid': user.id}
    return render(request, 'login/index.html', context) #这个是django里面找HTML的路径，不是html的方式

def header(request):
    user = request.session['user']
    context = {'user': user}
    return render(request, 'login/header.html', context=context)


def personal(request):
    user = request.session['user']
    u = models.User.objects.get(id=user.id)
    context = {'user': u}
    return render(request, 'login/personal.html', context)


def collaborators(request):
    users = models.User.objects.all()
    context = {'users':users}
    return render(request, 'login/collaborators.html', context=context)


def deleteUser(request, id):
    obj = models.User.objects.get(id=id)
    obj.delete()
    return collaborators(request)


def logout(request):
    request.session.flush()
    return login(request)