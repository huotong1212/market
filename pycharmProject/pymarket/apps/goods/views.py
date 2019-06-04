

# Create your views here.

from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.serializer import IndexCategorySerializer
from .filters import GoodsFilter
from .models import Goods,GoodCategory,Banner,HotSearchWords # 表示当前目录下的model.py
from .serializer import GoodsSerializer,GoodCategorySerializer,BannerSerializer,HotWordsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

# class GoodsListView(APIView):
#     """
#     List all goods
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[0:10]
#         serializer = GoodsSerializer(goods, many=True) #当goods是列表时，需要添加many=True
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs) # 做了进一步的封装，便于分页

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

class GoodsPagination(PageNumberPagination):
    page_size = 12  # 默认每页显示的数据条数
    page_size_query_param = 'page_size' # 获取url参数中设置的每页显示数据条数
    page_query_param = "page"  # 获取url中传入的页码key
    max_page_size = 60  # 最大支持的每页显示的数据条数

# class GoodsListView(generics.ListAPIView):
#     # ListAPIView继承了mixins.ListModelMixin,generics.GenericAPIView
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination
#
#     # 默认重写了上面的get方法

class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    商品列表页
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    
    # authentication_classes = (TokenAuthentication,)

    # def get_queryset(self):
    #     queryset = Goods.objects.all() # 只有for时才会执行
    #     price_min = self.request.query_params.get("price_min",0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset

    # 精确过滤：根据字段过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')

    # 搜索功能 ^表示name必须匹配开头
    search_fields = ('name', 'good_brief', 'good_desc')
    # 排序
    ordering_fields = ('shop_price','sold_num')
    # 条件筛选
    filter_class = GoodsFilter

    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list
        展示所有的商品类别信息，用于导航栏
    '''
    # 重要，只显示一级分类
    queryset = GoodCategory.objects.filter(category_type=1)
    serializer_class = GoodCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    # 只显示在tab页面上的一级分类下的数据
    queryset = GoodCategory.objects.filter(is_tab=True,name__in=['蔬菜水果','酒水饮料','粮油副食','生鲜食品'])
    serializer_class = IndexCategorySerializer





















