from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# from记录规范，系统包最上面，第三方包第二层，自定义包最下面

# Create your models here.


class ConsumerProfile(AbstractUser):
    '''
    用户
    '''
    # blank Admin中是否允许用户输入为空
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    # choice Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")

    class Meta:
        verbose_name = "用户"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.username


class VerifyCode(models.Model):
    '''
    用于记录验证码，也可以保存在redis中或者内存中
    '''
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    # 一般还有添加的字段有addtime,updatetime,isdeleted，这里只添加addtime

    # 不能写成datetime.now() 不然记录的是模型初始化的时间，而非添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.code


class Role(models.Model):
    """
    用户角色表
    """
    name = models.CharField(max_length=20, verbose_name="角色名称")
    user = models.ManyToManyField("ConsumerProfile",related_name = "roles",blank=True,null=True)
    desc = models.CharField(max_length=200,verbose_name="角色描述",blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户角色"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.name


class Authority(models.Model):
    """
    用户权限
    """
    name = models.CharField(max_length=20, verbose_name="权限名称")
    role = models.ManyToManyField("Role",related_name = "authority",blank=True,null=True)
    desc = models.CharField(max_length=200,verbose_name="权限描述",blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户权限"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.name
