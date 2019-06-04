from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

from rest_framework import permissions
from rest_framework import authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from consumers.models import VerifyCode
from consumers.serializers import SMSSerializer, ConsumerRegSerializer, ConsumerDetailSerializer
from utils.yunpian import YunPian
from pymarket import settings
# Create your views here.

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证，用于验证登录请求 loign
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username,password)
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
       Create a model instance. 验证码
    """
    serializer_class = SMSSerializer

    def generate_code(self):
        '''
        生成四位随机验证码
        '''
        seeds = '1234567890'
        codes = []
        for num in range(4):
            codes.append(choice(seeds))
        return "".join(codes)

    # 重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 如果验证不通过，直接抛异常

        yun_pian = YunPian(settings.APIKEY)
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code,mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                "mobile":sms_status["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            # 发送成功保存验证码
            code_record = VerifyCode.objects.create(code=code,mobile = mobile)
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class ConsumerViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册时候的验证
    """
    serializer_class = ConsumerRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConsumerDetailSerializer
        elif self.action == "create":
            return ConsumerRegSerializer

        return ConsumerDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    # 也可以这样加密保存密码
    # def create(self, validated_data):
    #     user = super(ConsumerRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 这一步会序列化对象，所有fields中的字段都会被序列号，而code已经被删除了
        # ，所以code中加入了write_only=True，让他不要被序列化和返回前端
        # register的用户对象
        re_dict = serializer.data

        # 将token返回给前端
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 当创建和删除的时候都会用到该方法
    def get_object(self):
        return self.request.user

    # 重写次方法，返回user
    def perform_create(self, serializer):
        # 这里需要操作数据库，而密码需要加密，所以用到了信号量
        # 在每次post保存的时候，将密码加密
        return serializer.save()