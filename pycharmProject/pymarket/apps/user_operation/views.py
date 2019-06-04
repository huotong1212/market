from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework import

# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserFavSerializer,UserFavDetailSerializer,UserRemarkSerializer,UserAdressSerializer
from .models import UserFav,UserRemark,UserAddress
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,
    mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    # ListModelMixin 展示所有查到的数据，以列表形式返回
    # RetrieveModelMixin 用来 userfav/2/ 时，可以查询到单个详情，实现当个实例的GET方法
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    # IsAuthenticated 判断是否登录 IsOwnerOrReadOnly 让用户只能对自己的收藏列表进行操作
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    # 设置JSONWebTokenAuthentication为局部，让用户访问Goods列表时不做登录限制
    # 设置SessionAuthentication，让已登录用户访问收藏列表时不会提示用户认证未提供,
    # 猜测，是用来保存token的，表示这个类已经验证过token了
    # 当请求的消息头没有带上token时就会返回"detail": "Authentication credentials were not provided."
    # 如果带了，就会直接返回结果
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"  # 因为goods是外键，所有加下划线

    # 重写get_queryset,只返回当前用户的收藏信息
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

class UserRemarkViewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """
    queryset = UserRemark.objects.all()
    serializer_class = UserRemarkSerializer

    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserRemark.objects.filter(user=self.request.user)

class UserAddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    # queryset = UserAddress.objects.all()
    serializer_class = UserAdressSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 我们希望让前端通过goods_id来查询数据，实际上在Serializer中我们也会将goods_id返回给前端
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


























