import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
# from django.views.generic import ListView  (Django View的拓展)
from goods.models import Goods


class GoodsListView(View):
    def get(self,request):
        '''
        通过djangoview实现商品列表页
        :param request:
        :return:
        '''
        # 查询前十条商品
        goods_list = Goods.objects.all()[:10]
        # 提取商品中的数据
        json_list = []
        # for good in goods_list:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['shop_price'] = good.shop_price
        #     json_dict['add_time'] = good.add_time.strftime("%Y-%m-%d")

        # for good in goods_list:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        #return HttpResponse(json.dumps(json_list),content_type="application/json")

        # 序列化为json字符串
        json_data = serializers.serialize("json",goods_list)
        json_data = json.loads(json_data)
        return JsonResponse(json_data,safe=False)