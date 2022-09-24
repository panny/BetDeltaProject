"""hkjc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from api import views

urlpatterns = [
    path('field/', views.FieldView.as_view()),
    path('rank/', views.RankView.as_view()),
    path('rank_record/', views.RankRecordView.as_view()),
    path('horse/', views.HorseView.as_view()),
    path('horse_rank/', views.HorseRankView.as_view()),
    path('jockey/', views.JockeyView.as_view()),
    path('jockey_rank/', views.JockeyRankView.as_view()),
    path('jockey_record/', views.JockeyRecordView.as_view()),
    path('trainer/', views.TrainerView.as_view()),
    path('trainer_rank/', views.TrainerRankView.as_view()),
    path('trainer_record/', views.TrainerRecordView.as_view()),
    path('task/', views.TaskView.as_view()),
    path('manage/', views.TaskManagerView.as_view()),
    path('', views.IndexView.as_view()),
    path('index/', views.AdminView.as_view()),
    path('option/', views.OptionView.as_view()),
]
