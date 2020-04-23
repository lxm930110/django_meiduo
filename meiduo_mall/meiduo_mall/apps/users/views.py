from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django_redis import get_redis_connection
from meiduo_mall.utils.info import UserCenterMinxi
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

        # 处理 短信验证
        redis_msg_cli = get_redis_connection('msg_code')
        msg_code = redis_msg_cli.get(mobile)
        if msg_code is None:
            return HttpResponse('短信验证码已过期，请重新获取验证码')
        # 删除存在redis中的验证码防止二次使用
        redis_msg_cli.delete(mobile)
        redis_msg_cli.delete(mobile + '_flag')
        if msg_code.decode() != msg_code:
            return HttpResponse('短信验证码输入错误')

        # 添加用户信息到数据库，保存user比较特殊需要考虑密码加密性，所以需要使用create_user()方法
        try:
            user = User.objects.create_user(username=username,
                                     password=password,
                                     mobile=mobile)
        except Exception as e:
            return HttpResponse('存储数据库错误')

        # 保持会话状态
        login(request, user)
        # response.set_cookie(username,username,max_age=60*60*24*14)
        # 响应
        return redirect('/')

        # return HttpResponse


class UsernameView(View):
    def get(self, request, username):
        # 接受请求
        # 验证
        # 处理
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库查询出错'})
        # 响应
        return JsonResponse({'count': count, 'code': 0, 'errmsg': 'OK'})


class MobileView(View):
    def get(self, request, mobile):
        # 接受请求
        # 验证
        # 处理
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库查询出错'})
        # 响应
        return JsonResponse({'count': count, 'code': 0, 'errmsg': 'OK'})

# 登录页面
class LoginView(View):

    def get(self,request):

        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        next_url = request.GET.get('next', '/')
        if not all([username,password]):
            return HttpResponse('参数不完整')
        user = authenticate(request,username=username,password=password)
        if user is None:
            return HttpResponse('用户名或者密码错误')
        else:
            login(request, user)

            response = redirect(next_url)
            # 设置cookie用于显示用户登录状态
            response.set_cookie('username', username, max_age=60*60*24*14)
            return response

# 退出登录
class LogoutView(View):
    def get(self,request):
        # 调用Logout方法退出登录
        logout(request)
        response = redirect('/login')
        # 删除保存在cookie中的username
        response.delete_cookie('username')
        return response

# 登录到个人中心使用Minxi扩展类
class UserCenterInfoView(UserCenterMinxi, View):

    def get(self,request):

        return render(request,'user_center_info.html')


        # user = request.user.is_authenticated
        # if user is True:
        #     return render(request,'user_center_info.html')
        # else:
        #     return redirect('/login')





