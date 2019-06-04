from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import  UserFav,UserRemark,UserAddress
from goods.serializer import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods','id')


class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前用户,并且隐藏了该字段，不会序列号返回给前端
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    '''
    用户收藏
    '''
    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        # 返回id，便于后续删除跟新操作
        fields = ('user','goods','id')

class UserRemarkSerializer(serializers.ModelSerializer):
    # 获取当前用户,并且隐藏了该字段，不会序列号返回给前端
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only=True 这个值只返回给前端不让前端提交
    # write_only=True 这个值只会提交，不会返回给前端
    # format 设置日期格式
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserRemark
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")

class UserAdressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")

        # fields = "__all__"
