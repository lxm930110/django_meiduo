from django_redis import get_redis_connection
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.sms import CCP
from random import randint
from celery_tasks.sms.tasks import send_sms


class ImageCodeView(View):

    def get(self, request, uuid):

        # 接受请求
        # 验证
        # 处理
        # 获取图片验证码,文本，唯一标示码，图片
        name,text, image = captcha.generate_captcha()
        print(text)
        print(image)

        # 链接redis
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 60*5, text)
        # 响应
        return HttpResponse(image, content_type='image/jpg')


class MsgCodeView(View):

    def get(self, request, mobile):
        # 接受请求
        # 获取图形验证码
        sor_image_code = request.GET.get('image_code')
        print(sor_image_code)
        # 获取uuid
        uuid = request.GET.get('image_code_id')
        # 链接到存储短信验证码redis
        redis_msg_cli = get_redis_connection('msg_code')

        # 防止恶意刷短信验证码
        if redis_msg_cli.get(mobile+'_flag') is not None:
            return JsonResponse({'code':400,'errmsg':'短信发送太频繁请稍后再发'})

        # 验证填写信息是否完整
        if not all([sor_image_code, uuid, mobile]):
            return JsonResponse({'code':400,'errmsg':'信息填写不完整'})
        # 链接到存储图形验证码redis
        redis_image_cli = get_redis_connection('image_code')
        # 获取存储在redis中的图形验证码
        image_code = redis_image_cli.get(uuid)
        print('测试一下：', image_code)
        # 判断图形验证码是否过期
        if image_code is None:
            return JsonResponse({'code':400,'errmsg':'图形验证码已过期，请重新获取'})
        # 使用一次立刻删除存储在redis中的图形验证码
        redis_image_cli.delete(uuid)
        # 判断图形验证是否正确
        print(image_code.decode().lower(),type(image_code.decode().lower()))
        if image_code.decode().lower() != sor_image_code.lower():
            return JsonResponse({'code':400,'errmsg':'图形验证码不正确，请点击重新获取'})
        # 随机获取6位数短信验证码
        msg_code = '%06d'% randint(0, 999999)
        print(msg_code)
        # 使用管道一次性往redis中存储短信验证码和短信验证码标记
        redis_line = redis_msg_cli.pipeline()

        redis_line.setex(mobile,60*5,msg_code)
        redis_line.setex(mobile +'_flag',60,1)
        redis_line.execute()
        # 给客户发送短信验证码
        # CCP().send_template_sms('18768469597', [msg_code, 5], 1)
        send_sms.delay(mobile, msg_code)
        # 响应
        return JsonResponse({'code':200,'errmsg':'OK'})

        # 验证
        # 处理
        # 获取图片验证码,文本，唯一标示码，图片
        # 响应
        # pass

