from django.db.models import Q
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Goods

class GoodsFilter(filters.FilterSet):
    '''
    商品的过滤类
    '''
    # field_name要配置的字段  lookup_expr 要满足的条件
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # contains 模糊查询（like） i忽略大小写
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    #
    top_category = filters.NumberFilter(field_name="top_category",method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        # category是外键 category_id找到对应的外键表的id(其实category_id是在数据库中保存的外键名)
        # category_id = 3 就是找类别为3的所有商品

        # parent_category_id是外键表自关联的外键，
        # category__parent_category_id=2就是找parent_category_id=2的所有category，
        # 然后再找属于这些category下面的所有goods
        # 或者说goods外键表中的parent_category_id=2等于二的goods

        # category__parent_category__parent_category_id=1
        # 就是找 goods所关联的category的所关联的parent_category中的parent_category_id为1的所有goods
        # goods对应的category是三级，可以通过这个category自身的parent_category_id找到所有的二级所对应的id
        # 或者通过parent_category找到所有的二级对象，而二级对象又可以通过parent_category_id找到所有的三级的id
        # 双下划线表示引出这个对象下所对应的某个值
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)
                               |Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'top_category', 'is_hot', 'is_new']
