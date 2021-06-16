
from django.urls import path

from . import views

app_name = 'dataset'
urlpatterns = [
    path('<int:dataset_id>/', views.dataset, name='dataset'),
    path('', views.datasets, name='datasets'),
    path('createDataset/', views.createDataset, name='createDataset'),
    path('uploadImg/<int:dataset_id>/', views.uploadImg, name='uploadImg'),
    path('deleteDataset/<int:id>/', views.deleteDataset, name='deleteDataset'),
    path('deletePicture/<int:id>/<int:datasetId>', views.deletePicture, name='deletePicture'),


]