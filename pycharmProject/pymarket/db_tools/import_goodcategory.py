

#独立使用django的model
import sys
import os

## 找到db_tools文件夹目录
pwd = os.path.dirname(os.path.realpath(__file__))
## 找到最外层文件夹
sys.path.append(pwd+"../")
## 设置环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pymarket.settings")

import django
# 启动django
django.setup()

# 一定要放在启动django之后
from goods.models import GoodCategory

from db_tools.data.category_data import row_data

# 根据层级目录导入django
for lev1_cat in row_data:
    lev1_intance = GoodCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()