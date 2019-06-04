"""pymarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import coreapi
from django.conf.urls import url,include
import xadmin
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views


# from goods.views_base import GoodsListView
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, GoodsCategoryViewSet, BannerViewset, HotSearchsViewset, IndexCategoryViewset
from pymarket.settings import MEDIA_ROOT
from rest_framework.routers import DefaultRouter
from consumers.views import SmsCodeViewSet, ConsumerViewset

# Create a router and register our viewsets with it.
from trade.views import ShopCartViewset, OrderViewset
from user_operation.views import UserFavViewSet,UserRemarkViewset,UserAddressViewset

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")
# 配置category的url
router.register(r'categorys', GoodsCategoryViewSet, base_name="categorys")

#收藏
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")

#留言
router.register(r'messages', UserRemarkViewset, base_name="messages")

#收货地址
router.register(r'address', UserAddressViewset, base_name="address")

#购物车url
router.register(r'shopcarts', ShopCartViewset, base_name="shopcarts")

#订单相关url
router.register(r'orders', OrderViewset, base_name="orders")

#轮播图url
router.register(r'banners', BannerViewset, base_name="banners")

#热搜榜
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

#首页商品系列数据
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")


router.register(r'codes', SmsCodeViewSet, base_name ="codes")
router.register(r'users', ConsumerViewset, base_name="users")


# good_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    # url(r'goods/$',good_list,name="goods-list"),
    url('^', include(router.urls)),

    # 引入restframework自动生成的文档
    url(r'docs/',include_docs_urls(title="我的Django")),

    url(r'^api-auth/', include('rest_framework.urls')),

    # 该url用于在用户POST提交用户名密码之后返回对应的token
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),

    # 第三方登录
    url('', include('social_django.urls', namespace='social')),

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
]





















