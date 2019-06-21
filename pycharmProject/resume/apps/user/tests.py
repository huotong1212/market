from datetime import timedelta,date

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.test import TestCase
import re
import datetime
# Create your tests here.

# reg = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
#
# result = re.match(reg,'824011142@qq.com')
#
# print(result)
print(date.today(),type(date.today()))
datatime = parse('2000-1-1')

date = datetime.date.fromisoformat('2010-06-11') #字符串转data
# strrtime date转为字符串
print(date,type(date))

# birthday = datetime.date("2019-06-11")
# today = datetime.date.today()
# print(today-date,type(today-date))
# print(today-relativedelta(years =10))
# print(today-relativedelta(years =10)>date)
# print(birthday)
# print(today-date,type(today-date))
# print((today.year-date.year),type((today.year-date.year)))
# print(datetime.date.year)

add_time = datetime.datetime(2019,6,19,13,44)
five_minutes_ago = datetime.datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
print(five_minutes_ago > add_time)
print(datetime.datetime.now()-add_time>timedelta(hours=0, minutes=5, seconds=0))