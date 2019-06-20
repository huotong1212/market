from django.db.models import Q
from rest_framework import serializers

from goods.models import IndexAd
from .models import Goods,GoodCategory,GoodsImage,Banner,HotSearchWords,GoodsCategoryBrand

class GoodCategorySerializer3(serializers.ModelSerializer):
    '''
    三级分类
    '''
    class Meta:
        model = GoodCategory
        fields = "__all__" # 包含所有字段


class GoodCategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    sub_cat = GoodCategorySerializer3(many=True)
    class Meta:
        model = GoodCategory
        fields = "__all__" # 包含所有字段

class GoodCategorySerializer(serializers.ModelSerializer):
    '''
    一级分类
    '''
    # sub_cat 是Category表中的自关联字段parent_category的relate_name,
    # 用于一对多反向引用时，点出二级分类，配置在多的那一方
    # 找出所有parent_category等于当前这个一级分类的parent_category的二级分类
    # many=True 表示会有多个
    sub_cat = GoodCategorySerializer2(many=True)
    class Meta:
        model = GoodCategory
        fields = "__all__"  # 包含所有字段

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )  # 包含所有字段

class GoodsSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True,max_length=100)
    # click_num = serializers.IntegerField(default=0)
    # market_price = serializers.FloatField(default=0.0)
    # goods_cover = serializers.ImageField()
    # add_time = serializers.DateTimeField()
    category = GoodCategorySerializer()
    images = GoodsImageSerializer(many=True) # 反向查询，一对多
    class Meta:
        model = Goods
        # fields = ('name','click_num','add_time') # 返回给前端的json中包含的字段
        fields = "__all__" # 包含所有字段

    def create(self, validated_data):
        """
        Create and return a new `Good` instance, given the validated data.
        """
        return Goods.objects.create(**validated_data)

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"

class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

class IndexCategorySerializer(serializers.ModelSerializer):
    # 拿到一个分类之后，反向查询这个分类下的所有品牌
    # brands是GoodsCategoryBrand表中关联分类的外键的rela_name,用作反向查询
    brands = BrandsSerializer(many=True)
    # 拿到对应级别下的所有商品信息
    goods = serializers.SerializerMethodField()
    # sub_cat 是Category表中的自关联字段parent_category的relate_name,
    # 用于一对多反向引用时，点出二级分类，配置在多的那一方
    # 找出所有parent_category等于当前这个一级分类的parent_category的二级分类
    # many=True 表示会有多个
    # 向下找，找到所有的下级分类，也就是二级分类
    sub_cat = GoodCategorySerializer2(many=True)
    # 广告栏展示的商品图
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        print(obj)
        print(type(obj))
        print('get_ad_goods', obj.id)
        goods_json = {}
        # 这里传过来的只有'蔬菜水果','酒水饮料','粮油副食','生鲜食品'
        # 而他们的序号已经在IndexAd表中添加过了，所有会找到队友的商品纪录
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 在serializer的方法中使用Serializer的时候，他会检察上下文中有没有包含request,
            # 如果有，那么在返回的图片url中会自动加上域名 http://....
            # 如果没有，那么返回的url只会加上路径 /media/goods/images/......
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    # 该方法的命名为get_加上要序列化的字段
    def get_goods(self, obj):
        print('get_goods', obj.id)
        # 找到对应级别下的所有商品信息
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

        # 不会就画图来方便理解
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)
                               |Q(category__parent_category__parent_category_id=obj.id))
        # 拿到指定的所有商品之后，通过serializer进行序列化

        # 在serializer的方法中使用Serializer的时候，他会检察上下文中有没有包含request,
        # 如果有，那么在返回的图片url中会自动加上域名 http://....
        # 如果没有，那么返回的url只会加上路径 /media/goods/images/......
        goods_serializer = GoodsSerializer(all_goods,many = True, context={'request': self.context['request']})
        # 注意，这里返回的必须是.data，而不是这个class实例，
        # 在ListModelMinx源码中可以找到相应的用法
        return goods_serializer.data

    class Meta:
        # 拿到商品分类表中的所有字段
        model = GoodCategory
        fields = "__all__"