
import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

from consumers.models import VerifyCode
from pymarket import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class SMSSerializer(serializers.Serializer):
    '''
    负责用户通过手机获取验证码的验证操作
    '''
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''

        # 手机号是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号是否合法
        if not re.match(settings.REGEX_MOBILE,mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds =0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago,mobile=mobile).count():
            raise serializers.ValidationError('请超过60s后再次发送')

        return mobile

class ConsumerDetailSerializer(serializers.ModelSerializer):
    '''
    负责返回用户详情页的信息
    '''
    class Meta:
        model = User
        fields = ("name", "birthday", "mobile", "gender", "email")


class ConsumerRegSerializer(serializers.ModelSerializer):
    '''
    负责用户注册时的初始化验证操作
    '''
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        # initial_data 初始化的时候前端传过来的数据
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            print(five_mintes_ago > last_record.add_time)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]  # 整体验证，如果是手机登录就把
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")










