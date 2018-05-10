#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import Admin

#表单
class UserForm(forms.Form):
    user = forms.CharField(label='username')
    password = forms.CharField(label='password',widget=forms.PasswordInput())


#注册
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            user = uf.cleaned_data['user']
            password = uf.cleaned_data['password']
            #添加到数据库
            Admin.objects.create(user= user,password=password)
            return HttpResponse('register success!!',)

    else:
        uf = UserForm()
    return render(request, 'login/regist.html', {'uf':uf}, context_instance=RequestContext(request))

#登陆
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            user = uf.cleaned_data['user']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            admin = Admin.objects.filter(user__exact = user,password__exact = password)
            if admin:
                #比较成功，跳转index
                response = HttpResponseRedirect('/main/main')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('user',user,3600)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/login/login')
    else:
        uf = UserForm()
    return render(request, 'login/login.html', {'uf':uf}, context_instance=RequestContext(request))

#登陆成功
def main(request):
    user = request.COOKIES.get('user','')
    return render(request, 'main/main.html' ,{'user':user})


    # #清理cookie里保存username
    # response.delete_cookie('user')
