from django.urls import path
from . import views

urlpatterns = [

    #base
    path('', views.question_list, name='index'),
    path('<int:pk>/', views.question_detail, name='detail'),

    # question_views.py
    path('question/create/', views.question_list, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_detail, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_detail, name='question_delete'),
]