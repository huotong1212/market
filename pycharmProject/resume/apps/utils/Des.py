import binascii
from pyDes import des, CBC, PAD_PKCS5


class DesCode(object):
    def des_encrypt(self,s):
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


    def des_descrypt(self,s):
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