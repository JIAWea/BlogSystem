from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository.models import *
from utils.pager import Pagination    #分页功能
from django.urls import reverse     #url别名
import os,uuid
#博客主站
def index(request,*args,**kwargs):
    article_type_list = Article.type_choices #菜单分类[(1, 'Python'), (2, 'Linux'), (3, 'JavaScript'), (4, 'PHP')]
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'
    article_list = Article.objects.filter(**kwargs).order_by('-id')  # 倒叙
    article_list_count = Article.objects.filter(**kwargs).count()   #有多少条数据
#分页开始
    current_page = request.GET.get('p')
    page_obj = Pagination(article_list_count, current_page)
    article_list = article_list[page_obj.start():page_obj.end()]
    page_str = page_obj.page_str(base_url)
#分页结束
    return render(request, 'index.html',
                  {
                      'article_type_list':article_type_list,    #主站的菜单分类
                      'article_type_id':article_type_id,
                      'article_list': article_list,             #筛选出来的文章
                      'page_str':page_str,
                   })

#个人博客主页
def home_index(request,site):
    blog = Blog.objects.filter(surfix=site).first()
    follower = User2User.objects.filter(from_user__blog__surfix=site).count()
    fans = User2User.objects.filter(to_user__blog__surfix=site).count()
    tags = Tag.objects.filter(bid__surfix=site)
    category = Category.objects.filter(bid__surfix=site)
    ctime = Article.objects.filter(blog_id=blog.bid).extra(
        select={"p_time":"strftime('%%Y-%%m',ctime)"}
    )
    article_list = Article.objects.filter(blog__surfix=site).all()

    return render(request,'home_personal.html',{
        'blog':blog,
        'follower':follower,
        'fans':fans,
        'tags':tags,
        'category':category,
        'ctime':ctime,
        'article_list':article_list
    })

def home_filter(request,surfix,condition,val):
    blog = Blog.objects.filter(surfix=surfix).first()
    follower = User2User.objects.filter(from_user__blog__surfix=surfix).count()
    fans = User2User.objects.filter(to_user__blog__surfix=surfix).count()
    tags = Tag.objects.filter(bid__surfix=surfix)
    category = Category.objects.filter(bid__surfix=surfix)
    ctime = Article.objects.filter(blog_id=blog.bid).extra(
        select={"p_time": "strftime('%%Y-%%m',ctime)"}
    )
    if condition == 'tag':
        article_list = Article.objects.filter(tags=val,blog_id=blog.bid)
        print(article_list)
    elif condition == 'category':
        article_list = Article.objects.filter(blog__surfix=surfix, category_id=val)
    elif condition == 'date':
        article_list = Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",ctime)=%s'],params=[val,]).all()

    return render(request,'home_personal.html',{
        'blog':blog,
        'follower': follower,
        'fans': fans,
        'tags': tags,
        'category': category,
        'ctime': ctime,
        'article_list': article_list,
    })

#个人博客文章详细
def home_article_detail(request,surfix,nid):

    blog = Blog.objects.filter(surfix=surfix).first()
    follower = User2User.objects.filter(from_user__blog__surfix=surfix).count()
    fans = User2User.objects.filter(to_user__blog__surfix=surfix).count()
    tags = Tag.objects.filter(bid__surfix=surfix)
    category = Category.objects.filter(bid__surfix=surfix)
    ctime = Article.objects.filter(blog_id=blog.bid).extra(
        select={"p_time": "strftime('%%Y-%%m',ctime)"}
    )
    article_list = Article.objects.filter(blog__surfix=surfix,id=nid).first()

    return render(request, 'home_article_detail.html', {
        'blog': blog,
        'follower': follower,
        'fans': fans,
        'tags': tags,
        'category': category,
        'ctime': ctime,
        'article_list': article_list
    })

#评论
def submitComment(request):
    respones={'status':True,'message':None}
    if request.FILES:
        img = request.FILES.get('imgFile')
        nid = str(uuid.uuid4())
        files_path = os.path.join('static/img',nid+img.name)

        f = open(files_path,'wb')
        for line in img.chunks():
            f.write(line)
        f.close()
        dic = {
            'error': 0,
            'url': '/static/img/'+ nid+img.name,
            'message': '错误了···'
        }
        return JsonResponse(dic)

    print(request.POST.get('comment'))
    respones['message']='评论成功'
    return JsonResponse(respones)