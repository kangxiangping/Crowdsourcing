"""OnlineCrowd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('export/', include('export.urls')),
    path('project/', include('project.urls')),
    path('dataset/', include('dataset.urls')), #在此命名空间也要注册，url中的就是此处的地址 ，一定要加上/，不然没法匹配后面的，
    path('', include('login.urls')),
    path('admin/', admin.site.urls),


]
