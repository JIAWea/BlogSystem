from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.forms import fields,widgets
from django.core.validators import RegexValidator       #正则表达式
from django.core.exceptions import ValidationError      #def clean()方法
from repository.models import *
#登录表单
class loginForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','name':'username','placeholder':'账号'}))
    pwd = fields.CharField(
        required=True,
        widget=widgets.PasswordInput(attrs={'class':'form-control','name':'pwd','placeholder':'密码'},))
    code = forms.CharField(required=True,
        widget=widgets.PasswordInput(attrs={'class': 'form-control code-style', 'name': 'code', 'placeholder': '验证码'}, ))

    def clean_code(self):
        if self.request.POST.get('code').upper() != self.request.session['check_code'].upper():
            raise ValidationError(message='验证码错误', code='invalid')

#注册表单
class registerForm(forms.Form):
    username = forms.CharField(
        required=True,min_length=2,max_length=8,
        widget=widgets.TextInput(attrs={'class':'form-control','name':'username','placeholder':'username'}),
        error_messages={'required':'账号不能为空','invalid':'格式错误','min_length': "密码长度不能小于2个字符",
                                'max_length': "密码长度不能大于8个字符"}
    )
    pwd = forms.CharField(
        required=True,min_length=12,max_length=32,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'pwd', 'placeholder': 'password'}),
        validators=[RegexValidator('^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$','只能为数字')],
        error_messages={'required': '密码不能为空',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"})
    confirmPwd = forms.CharField(
        required=True,min_length=6,max_length=20,
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'name': 'pwd', 'placeholder': 'password'}),
        error_messages={'required': '密码不能为空', 'invalid': '格式错误'}
    )
    email = fields.EmailField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'email'}),
        error_messages={'required': '邮件不能为空','invalid':'格式错误'}
    )
    code = forms.CharField(required=True,
        widget=widgets.PasswordInput(attrs={'class': 'form-control code-style', 'name': 'code', 'placeholder': '验证码'}, ))

    # 确认密码是否一致
    def clean(self):
        m1 = self.cleaned_data.get('pwd')
        m2 = self.cleaned_data.get('confirmPwd')
        # print(m1,m2)
        if m1 == m2:
            return self.cleaned_data
        else:
            raise ValidationError('密码不一致')




#注册页面
def register(request):
    if request.method == 'GET':
        obj = registerForm()
        return render(request, 'register.html', {'obj':obj})
    else:
        obj = registerForm(request.POST)
        check_code = request.session['check_code']
        code = request.POST.get('code')
        if check_code.upper() != code.upper():
            msg = '验证码错误！'
            return render(request,'register.html',{'obj':obj,'msg':msg})
        if obj.is_valid():
            return redirect('login.html')
        else:
            return render(request, 'register.html', {'obj':obj})




#登录页面
def login(request):
    if request.method == 'GET':
        obj = loginForm(request)
        return render(request, 'login.html', {'obj':obj})
    else:
        obj = loginForm(request,request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        if obj.is_valid():
            user_info = UserInfo.objects.filter(username=username,pwd=pwd).first()
            blog_id = Blog.objects.filter(uid_id=user_info.uid).first()
            request.session['username'] = username
            request.session['pwd'] = pwd
            request.session['blog_id'] = blog_id.bid
            # user_info = UserInfo.objects.filter(username=username,pwd=pwd).first()
            # request.session['user_info'] = user_info
            print('blog_id',request.session['blog_id'])
            if user_info:
                return redirect('/')
            else:
                # return redirect('/')
                return render(request,'login.html',{'obj':obj})        #账号密码错误

        else:
            return render(request, 'login.html', {'obj':obj})




def logout(request):
    request.session.clear()
    return redirect('/')




def checkCode(request):
    return render(request, 'code_test.html')




from io import BytesIO
from utils.check_code import create_validate_code
def codetest(request):
    f = BytesIO()
    img, code = create_validate_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    # request.session['CheckCode'] = code
    return HttpResponse(f.getvalue())