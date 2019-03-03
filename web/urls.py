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
from web.views import home
from web.views import account       #账户相关，登录注册

urlpatterns = [
    path('admin/', admin.site.urls),
    # url('^',views.idenx),                        #\w表示为可数字,字母,下划线,字符串  *表示前面的可有可无

    url('^login.html$', account.login),
    url(r'^logout.html$', account.logout),
    url('^register.html$', account.register),
    url('^checkcode.html$', account.checkCode),     #验证码测试
    url('^codetest.html', account.codetest),        #验证码测试

    url('^submitComment$',home.submitComment),

    url('^all/(?P<article_type_id>(\d+)).html$', home.index, name='index'),  # 博客主站

    url(r'^(?P<surfix>\w+-*\w*)/(?P<nid>(\d+)).html$', home.home_article_detail),
    url(r'^(?P<surfix>\w+-*\w*)/(?P<condition>((tag)|(category)|(date)))/(?P<val>\w+-*\w*).html$', home.home_filter),
    url(r'^(?P<site>\w+-*\w*).html$', home.home_index),

    url('^', home.index),                           #博客主站


]
