from random import choice

from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, authentication, status, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from resume import settings
from user.models import User, VerifyCode, Role
from user.serializers import PermissionSerializer, SMSSerializer, UserDetailSerializer, UserRegSerializer, \
    EmailSerializer
from utils.ailiSmS import AliSms
from utils.emailSenter import EmailManager
from utils.yunpian import YunPian


class PermissionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer
    queryset = User.objects.all()

    # 当Update和Retrieve和Delete的时候都会用到该方法
    def get_object(self):
        return self.request.user


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

        # yun_pian = YunPian(settings.APIKEY)
        alisms = AliSms(settings.ACCESS_KEYID, settings.ACCESS_KEYID_SECRET)
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        # sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        print("验证码是："+code)
        sms_status = alisms.sendSMS(mobile,code)

        if sms_status['Code'] != "OK":
            return Response({
                "mobile": sms_status["Message"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 发送成功保存验证码
            code_record = VerifyCode.objects.create(code=code, mobile=mobile)
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

class EmailCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
       Create a model instance. 验证码
    """
    serializer_class = EmailSerializer

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

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

        email = self.request.user.email
        code = self.generate_code()
        mail_cfgs = settings.MAIL_CFGS

        mail_cfgs['msg_to'].append(email)
        mail_cfgs['msg_content'] = f"您的验证码是【{code}】"

        manager = EmailManager(**mail_cfgs)
        email_status = manager.send()

        print("验证码是："+code)

        if email_status != "success":
            return Response({
                "email": "邮箱地址错误"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 发送成功保存验证码
            code_record = VerifyCode.objects.create(code=code, email=email)
            return Response({
                "email": email
            }, status=status.HTTP_201_CREATED)



class UserViewSet(CacheResponseMixin,CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册,更新，获取个人信息
    """
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action in ["retrieve","update"]:
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

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

        # 绑定用户表和角色表的对应关系，设置该用户为普通用户
        role = Role.objects.get(name="普通用户")
        user.roles.add(role)

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

    # 当Update和Retrieve和Delete的时候都会用到该方法
    def get_object(self):
        return self.request.user

    # 重写次方法，返回user
    def perform_create(self, serializer):
        # 这里需要操作数据库，而密码需要加密，所以用到了信号量
        # 在每次post保存的时候，将密码加密
        # print(serializer.validated_data)
        return serializer.save()