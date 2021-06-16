from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('check_register/', views.check_register, name='check_register'),
    path('check_login/', views.check_login, name='check_login'),
    path('header/', views.header, name='header'),
    path('personal/', views.personal, name='personal'),
    path('collaborators/', views.collaborators, name='collaborators'),
    path('deleteUser/<int:id>/', views.deleteUser, name='deleteUser'),
    path('logout/', views.logout, name='logout'),
]