"""WebProject URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from blog import views


urlpatterns = [
    path('', views.main, name='main_page'),
    path('hot', views.main, name='hot_page'),

    path('singup/', views.create_accaunt, name="singup"),
    path('singup/create_accaunt', views.create_accaunt_add, name="create_accaunt_add"),

    path('user_settings', views.settings, name='settings'),
    path('user_settings/done', views.settings_done, name='settings_done'),

    path('tag/<slug:tag_slug>', views.main, name='tag_page'),
    path('question/<int:question_id>/', views.some_post, name='question_page'),
    path('question/<int:question_id>/leave_answer', views.leave_answer, name='leave_answer'),
    path('ask/', views.create_post, name='new_question_page'),
    path('ask/ask_question', views.ask_question, name='ask_question'),
   ]
