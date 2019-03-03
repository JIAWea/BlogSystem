"""blogSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from backend import views

urlpatterns = [
    url('^index.html$',views.index),
    url('^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$',views.article),
    url('add_article.html$',views.add_article),
    url('edit_article-(?P<id>\d+).html$',views.edit_article),
    url('del_article-(?P<id>\d+).html$',views.del_article),
]
