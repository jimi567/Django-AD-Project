from django.urls import path
from . import views

urlpatterns = [

    #base
    path('', views.QuestionList.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='detail'),

]