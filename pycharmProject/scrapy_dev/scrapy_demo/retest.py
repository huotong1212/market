
import re

url = "?start=20&limit=20&sort=new_score&status=P&percent_type="

res = re.match('^\?.*status=P',url)
print(res.group())

# https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv619&productId=5912071&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
# https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv619&productId=5912071&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&rid=0&fold=1