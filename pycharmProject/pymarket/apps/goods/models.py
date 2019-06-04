from datetime import datetime

from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField


class GoodCategory(models.Model):
    """
    商品类别,当存在多级分类关系时，其实不需要设计多个model，只要设计一个model让他自关联就可以了
    """
    CATEGORY_TYPE = (
        (1, "一级分类"),
        (2, "二级分类"),
        (3, "三级分类")
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")  # 名称
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")  #
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")  # 描述
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # related_name=None,   反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
    parent_category = models.ForeignKey("self", related_name="sub_cat", null=True, blank=True,
                                        help_text="父类级别", verbose_name="父类级别", on_delete=models.CASCADE)  # 多级分类时自关联的外键

    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")  # 用于tab上展示的类别
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名，每个类别的商品品牌
    """
    name = models.CharField(default="", max_length=20, verbose_name="品牌名", help_text="品牌名")
    desc = models.CharField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    # upload_to 上传文件的保存路径在media下
    image = models.ImageField(max_length=200, upload_to="brands/images/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    # relate_name 反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
    # 这里是通过类别找品牌时，GoodCategory().brands.all()
    category = models.ForeignKey(GoodCategory, related_name="brands", null=True, blank=True,
                                 verbose_name="商品类别", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_brand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodCategory, verbose_name="商品类别", on_delete=models.CASCADE)
    good_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="销量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏量")
    goods_num = models.IntegerField(default=0, verbose_name="剩余库存")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    good_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    good_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=300,
                             filePath="goods/files", default="")
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_cover = models.ImageField(upload_to="goods/images", null=True, blank=True, verbose_name="封面")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodCategory, related_name='category',verbose_name="商品类目", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, related_name='goods', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class Banner(models.Model):
    """
    首页轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banner", verbose_name="首页轮播图")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页轮播商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords