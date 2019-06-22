from django.test import TestCase

# Create your tests here.

# print("dsadas%s"%(111))

# a = {'a':1,'b':2}
# b = a
# b['c'] = 3
# print('a--->',a)
# print('b--->',b)

# import base64
# # base64加密
# def jiami(str):
#     name = str
#     name = name.encode('utf-8')
#     a = base64.b64encode(name)
#     print(a)
#     # base64解密
# def jiemi(str):
#     b =  base64.b64decode(str)
#     c = b.decode('utf-8')
#     print(c)
#
# str = 'aaa344324我'
# mm = jiami(str)
# jiemi(mm)

# str = 'MO2tV6y084G4jjAxODA3MjcxMDI0MTQ='
# jiemi(str)

import binascii
from pyDes import des, CBC, PAD_PKCS5


def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = '20171117'
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return: 解密后的字符串
    """
    secret_key = '20171117'
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

if __name__ == "__main__":
    material = '1;周文军;12'.encode('utf-8') # 用户id,用户名,简历id
    str_en = des_encrypt(material)  # 加密
    print(str_en.decode('utf-8'))
    str_a = str_en.decode('utf-8')# 转成utf-8返回给前端


    str_x = str_a.encode('utf-8')# 接受前端，转成encode方便解密
    str_de = des_descrypt(str_x)
    print(str_de.decode('utf-8'))