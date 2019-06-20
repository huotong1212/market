from datetime import timedelta, datetime, date
import re

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from resume import settings
from user.models import Authority, Role, User, VerifyCode


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    负责返回用户详情页的信息
    '''
    # mobile = serializers.CharField(read_only=True)
    # email = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ("username", "birthday", "mobile", "gender", "email", "portrait")


class UserRegSerializer(serializers.ModelSerializer):
    '''
    负责用户注册时的初始化验证操作
    '''
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
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
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )
    email = serializers.CharField(required=True, max_length=20, label="邮箱",
                                  error_messages={
                                      "blank": "请输入邮箱",
                                      "required": "请输入邮箱",
                                      "max_length": "邮箱格式错误",
                                  },
                                  help_text="邮箱")

    mobile = serializers.CharField(required=True, max_length=11, label="手机号", help_text="手机号")

    birthday = serializers.DateField(format='%Y-%m-%d', label='出身日期', help_text="出身日期", )

    def validate_birthday(self, birthday):
        # print(birthday, type(birthday))
        # 请输入正确的年龄，必须大于13周岁
        print('birthday:', birthday + relativedelta(years=13))
        if birthday + relativedelta(years=13) > date.today():
            raise serializers.ValidationError("请输入正确的年龄，必须大于13周岁")

        return birthday

    def validate_code(self, code):

        # initial_data 初始化的时候前端传过来的数据
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate_email(self, email):
        '''
        验证邮箱
        :param email:
        :return:
        '''

        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("该邮箱已被注册")

        # 验证邮箱是否合法
        if not re.match(settings.REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱的格式错误')

        return email

    def validate(self, attrs):
        attrs["name"] = attrs["username"]  # 整体验证，如果是手机登录就把
        attrs['age'] = date.today().year - attrs['birthday'].year + 1  # 计算年龄
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password", "email", "birthday", "gender")


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
            raise serializers.ValidationError("手机号已被注册")

        # 验证手机号是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('请超过60s后再次发送')

        return mobile


class EmailSerializer(serializers.ModelSerializer):
    '''
    负责用户通过邮箱找回密码的验证操作
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    email = serializers.CharField(read_only=True)

    def validate_email(self, email):
        # 验证验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, email=email).count():
            raise serializers.ValidationError('请超过60s后再次发送')

    class Meta:
        model = User
        fields = ('email', 'user')
    # email = serializers.CharField(max_length=20)
    #
    # def validate_email(self, email):
    #     '''
    #     验证邮箱
    #     :param mobile:
    #     :return:
    #     '''
    #
    #     # 邮箱是否注册
    #     if User.objects.filter(email=email).count():
    #         raise serializers.ValidationError("邮箱已被注册")
    #
    #     # 验证邮箱是否合法
    #     if not re.match(settings.REGEX_EMAIL, email):
    #         raise serializers.ValidationError('邮箱非法')
    #
    #     # 验证验证码发送频率
    #     one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    #     if VerifyCode.objects.filter(add_time__gt=one_minute_ago, email=email).count():
    #         raise serializers.ValidationError('请超过60s后再次发送')
    #
    #     return email


class AuthoritySerializer(serializers.ModelSerializer):
    '''
    序列化用户权限数据
    '''

    class Meta:
        model = Authority
        fields = ("name", "desc")


class RoleSerializer(serializers.ModelSerializer):
    '''
    序列化角色数据
    '''
    authority = AuthoritySerializer(many=True)

    class Meta:
        model = Role
        fields = ("name", "desc", "authority")


class PermissionSerializer(serializers.ModelSerializer):
    '''
    负责返回用户序列化后的用户角色信息和其对应的权限数据
    '''

    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "roles")
