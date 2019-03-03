from django.db import models

class UserInfo(models.Model):
    """用户表"""
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    img = models.ImageField(upload_to='media/upload_imgs')
    user_user = models.ManyToManyField(
        to='UserInfo',
        through='User2User',
        through_fields=('from_user','to_user')
    )
    class Meta:
        verbose_name_plural = '用户表'
    def __str__(self):
        return self.username

class User2User(models.Model):
    from_user = models.ForeignKey(UserInfo,related_name='fromUser',verbose_name='被关注者',on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserInfo,related_name='toUser',verbose_name='粉丝',on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='互粉表'
        unique_together=[('from_user','to_user'),]

class Blog(models.Model):
    """博客表"""
    bid = models.AutoField(primary_key=True)
    surfix = models.CharField(max_length=32,verbose_name='昵称前缀')
    theme = models.CharField(max_length=32,verbose_name='主题')
    title = models.CharField(max_length=32,verbose_name='标题')
    summary = models.CharField(max_length=32,verbose_name='简介')
    uid = models.ForeignKey(UserInfo,on_delete=models.CASCADE,unique=True)
    class Meta:
        verbose_name_plural = '博客表'

    def __str__(self):
        return self.surfix

class Category(models.Model):
    """分类表"""
    caption = models.CharField(max_length=32,verbose_name='分类名称')
    bid = models.ForeignKey(Blog,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '分类表'
    def __str__(self):
        return self.caption

class Tag(models.Model):
    """标签表"""
    caption = models.CharField(max_length=32)
    bid = models.ForeignKey(Blog,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '标签表'
    def __str__(self):
        return self.caption

class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='标题')
    summary = models.CharField(max_length=100,verbose_name='简介')
    detail = models.CharField(max_length=500,verbose_name='详细')
    ctime = models.DateTimeField(null=True,blank=True)
    blog = models.ForeignKey(Blog,verbose_name='所属博客',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,verbose_name='文章类型',on_delete=models.CASCADE)

    type_choices=[(1,"Python"),(2,"Linux"),(3,"JavaScript"),(4,"PHP")]      #主站的分类，通过索引查找相关信息
    article_type_id = models.IntegerField(choices=type_choices,default=None,verbose_name='主站分类')

    tags = models.ManyToManyField(
        to=Tag,
        through='Article2Tag',
        through_fields=('article','tag')
    )
    class Meta:
        verbose_name_plural='文章表'
    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    """文章与标签多对多关系表"""
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='文章与标签关系表'
