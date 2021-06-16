from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'export'
urlpatterns = [
    path('', views.export, name="export"),
    path('download/<int:project_id>/', views.download, name="download"),
    path('annotations/<int:project_id>/', views.annotations, name="annotations"),
    path('annotations_batch/<int:project_id>/', views.annotations_batch, name="annotations_batch"),
    path('quality/<int:project_id>/', views.quality, name="quality"),
    path('quality_diff/<int:project_id>/', views.quality_diff, name="quality_diff"),
    path('taskDiff/<int:project_id>/', views.taskDiff, name="taskDiff"),

]
