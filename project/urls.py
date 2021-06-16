from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.index, name='index'),
    path('step1/', views.step1, name='step1'),
    path('step2/', views.step2, name='step2'),
    path('step3/<int:project_id>/', views.step3, name='step3'),
    path('finish/<int:project_id>/', views.finish, name="finish"),
    path('begin/<int:project_id>/', views.begin, name="begin"),
    path('working/<int:project_id>/<int:index>/', views.working, name="working"),
    path('getAnswer/', views.getAnswer, name="getAnswer"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('finishProject/<int:id>/', views.finishProject, name="finishProject"),


]