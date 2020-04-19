from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import User
import re

# Create your views here.
from django.views.generic.base import View


class RegisterView(View):

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        # 接受请求
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        msg_code = request.POST.get('msg_code')
        allow = request.POST.get('allow')

        # 验证
        # 验证填写信息是否完整
        if not all([username,password,password2,mobile,msg_code,allow]):
            return HttpResponse('填写信息不完整', status=403)
        # 验证用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponse('用户名错误长度5-20', status=403)
        # 验证用户名是否存在
        if User.objects.filter(username=username).count() > 0:
            return HttpResponse('用户名已存在', status=403)
        # 验证密码
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponse('密码错误长度8-20', status=403)
        if password != password2:
            return HttpResponse('密码前后不一致', status=403)
        # 验证手机
        if not re.match(r'^1[345789]\d{9}$', mobile):

            return HttpResponse('手机号格式错误', status=403)

        # 处理

        # 添加用户信息到数据库，保存user比较特殊需要考虑密码加密性，所以需要使用create_user()方法
        user = User.objects.create_user(username=username,
                                 password=password,
                                 mobile=mobile)
        # 保持会话状态
        login(request, user)

        # 响应
        return redirect('/')

        # return HttpResponse


class UsernameView(View):
    def get(self, request, username):
        # 接受请求
        # 验证
        # 处理
        count = User.objects.filter(username=username).count()
        # 响应
        return JsonResponse({'count': count, 'code': 0, 'errmsg': 'OK'})


class MobileView(View):
    def get(self, request, mobile):
        # 接受请求
        # 验证
        # 处理
        count = User.objects.filter(mobile=mobile).count()
        # 响应
        return JsonResponse({'count': count, 'code': 0, 'errmsg': 'OK'})


