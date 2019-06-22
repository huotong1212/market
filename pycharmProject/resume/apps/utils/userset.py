
import sys
import os
from datetime import datetime

from django.contrib.auth.hashers import make_password


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume.settings")

import django
django.setup()

from user.models import User

# consumer = ConsumerProfile(name="huotong",username="huotong",password="123456",email="824011142@qq.com",
#                            gender="male",mobile="18961272662",birthday=datetime.now())

# consumer = ConsumerProfile.objects.filter(name="huotong")[0]
# make_password()
# consumer.is_active = False
# consumer.save()

# from django.contrib.auth.models import User
# user = User.objects.create_user（username='',password='',email=''）

user = User.objects.get(username='tong')
user.set_password('123456')
user.save()