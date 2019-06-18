router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")