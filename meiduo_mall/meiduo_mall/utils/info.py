from django.contrib.auth.decorators import login_required

class UserCenterMinxi(object):
    @classmethod
    def as_view(cls,*args,**kwargs):
        view = super().as_view(*args,**kwargs)
        return login_required(view)
