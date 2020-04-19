from django_redis import get_redis_connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha


class ImageCode(View):

    def get(self, request, uuid):
        print(request.method)
        # 接受请求
        # 验证
        # 处理
        # 获取图片验证码,文本，唯一标示码，图片
        text, image = captcha.generate_captcha()
        print(text,image)
        # 链接redis
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 60*5, text)
        # 响应
        return HttpResponse(image, content_type='image/jpg')

