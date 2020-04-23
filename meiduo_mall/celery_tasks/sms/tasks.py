from celery_tasks.main import celery_app

from meiduo_mall.libs.yuntongxun.sms import CCP

@celery_app.task(name='send_sms')
def send_sms(mobile, msg_code):
    # 将耗时的代码封装在一个方法中
    result= CCP().send_template_sms(mobile, [msg_code, 60*5], 1)

    return result

