# -*- coding: utf-8 -*-
__author__ = 'bobby'
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
# sender就是一个要操作的Model
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 判断这个操作是不是新建
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
