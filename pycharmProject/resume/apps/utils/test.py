from email.header import Header
from email.utils import formataddr, parseaddr


def _format_addr(s):
    '''
    格式化一个邮件地址:如果包含中文，需要通过Header对象进行编码。
    :param s:
    :return:
    '''
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

msg_to= ['huotong177@163.com','401952124@qq.com','544782744@qq.com']
# msg_to = ';'.join(msg_to)
result = ";".join([_format_addr(u'To <%s>' % to) for to in msg_to])
print(result)

# msg_to= ['huotong177@163.com','401952124@qq.com','544782744@qq.com']
# # msg_to = ';'.join(msg_to)
# for to in msg_to:
#     result = _format_addr(to)
# result = ";".join([_format_addr(to) for to in msg_to])
# to_emails = "To " + result
# print(to_emails)

t1 = [1,2,3]
t2 = [2,3,4]
print(t1+t2)