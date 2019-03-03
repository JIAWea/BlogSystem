from django.shortcuts import render,redirect
from repository.models import *

#文章显示
def index(request):
    return render(request,'backend_index.html')



#文章管理
def article(request,**kwargs):
    # print(kwargs)
    blog_id=request.session['blog_id']      #就是登陆进来的博客账号id
    # kwargs['blog_id']=blog_id         #不能直接用kwargs的刚发，如果是0-0的话则不会全部文章，因为需要筛选条件为空，而不是0-0
    condition={}
    for k,v in kwargs.items():
        temp = int(v)
        kwargs[k]=temp
        if temp:
            condition[k]=temp

    condition['blog_id']=blog_id
    # print(condition)     #{'article_type_id': '1', 'category_id': '4', 'blog_id': 2}
    article_list = Article.objects.filter(**condition).order_by('-id')
    type_list = list(map(lambda x:{'nid':x[0],'title':x[1]},Article.type_choices))
    # print(type_list)
    category_list = Category.objects.filter(bid_id=blog_id)

    return render(request,'backend_article.html',
                  {'article_list':article_list,
                   'type_list':type_list,
                   'category_list':category_list,
                   'kwargs':kwargs,
                   })




#添加文章
from backend.Form.articleForm import *
def add_article(request):
    if request.method == 'GET':
        obj = articleForm(request)
        return render(request,'backend_add_article.html',{'obj':obj})
    else:
        obj = articleForm(request,request.POST)
        if obj.is_valid():
            print(obj.cleaned_data) #{'title': '123', 'summary': '123', 'detail': '123', 'article_type_id': 4, 'category_id': '5', 'tags': ['4']}
            tags = obj.cleaned_data.pop('tags') #['4','5'] ---> 把tags的数据分离出来
            obj.cleaned_data['blog_id'] = request.session['blog_id']

            article_obj = Article.objects.create(**obj.cleaned_data)      #添加文章数据

            tags_list = []          #下面添加文章标签关系表
            for tag_id in tags:
                tag_id = int(tag_id)
                tags_list.append(Article2Tag(article_id=article_obj.id,tag_id=tag_id))
            Article2Tag.objects.bulk_create(tags_list)

            return redirect('/backend/article-0-0.html')
        else:
            return render(request,'backend_add_article.html',{'obj':obj})



#修改文章
from django.core import serializers
def edit_article(request,id):
    if request.method == 'GET':
        # print('id++++++',id) #就是用户在backend_article页面传过来的文章id
        blog_id = request.session['blog_id']
        data = Article.objects.filter(id=id,blog_id=blog_id).first()
        tags = data.tags.values_list('id')      #<QuerySet [(4,), (5,)]>
        if tags:tags = list(zip(*tags))[0]      #转换为一个元祖(4,5)

        obj = articleForm(request,
                          {'title':data.title,
                           'summary':data.summary,
                           'detail':data.detail,
                           'article_type_id':data.article_type_id,
                           'category_id':data.category_id,
                           'tags':tags
                           })
        return render(request,'backend_edit_article.html',{'obj':obj,'id':id})
    else:
        obj = articleForm(request,request.POST)
        if obj.is_valid():
            blog_id = request.session['blog_id']
            data = Article.objects.filter(id=id, blog_id=blog_id).first()   #需要修改的文章
            # print(obj.cleaned_data) #{'title': '123', 'summary': '123', 'detail': '123', 'article_type_id': 4, 'category_id': '5', 'tags': ['4']}
            tags = obj.cleaned_data.pop('tags')
            article_obj = Article.objects.filter(id=id).update(**obj.cleaned_data)

            Article2Tag.objects.filter(article_id=data.id).delete()
            tags_list=[]

            for tag_id in tags:
                tag_id = int(tag_id)
                tags_list.append(Article2Tag(article_id=data.id,tag_id=tag_id))
            Article2Tag.objects.bulk_create(tags_list)
        return redirect('/backend/article-0-0.html')




#删除文章
def del_article(request,id):
    Article.objects.filter(id=id).delete()
    Article2Tag.objects.filter(article_id=id).delete()
    return redirect('/backend/article-0-0.html')