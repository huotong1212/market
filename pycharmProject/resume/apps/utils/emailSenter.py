import mimetypes
import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os
from os.path import getsize


class EmailManager:
    '''
    SMTP是发送邮件的协议，Python内置对SMTP的支持，
    可以发送纯文本邮件、HTML邮件以及带附件的邮件。
    Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。
    '''

    def __init__(self, **kwargs):
        '''
         constructor
         :param kwargs:Variable paramete
        '''
        self.kwargs = kwargs
        self.smtp_server = 'smtp.qq.com'
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 附件大小


    def __get_cfg(self, key, throw=True):
        '''
          get the configuration file based on the key
          获取配置参数信息
          当读取的key对应的value为None或空值时抛出异常信息
          :param key:
          :param throw:
          :return:
          '''
        cfg = self.kwargs.get(key)
        if throw == True and (cfg is None or cfg == ''):
            raise Exception("The configuration can't be empty", 'utf-8')
        return cfg

    def __init_cfg(self):
        '''
        初始化配置参数信息
        :return:
        '''
        self.msg_from = self.__get_cfg('msg_from')
        self.password = self.__get_cfg('password')
        # self.msg_to = ';'.join(self.__get_cfg('msg_to'))
        self.msg_to = self.__get_cfg('msg_to')
        #self.msg_cc = ';'.join(self.__get_cfg('msg_cc'))
        self.msg_cc = self.__get_cfg('msg_cc')
        self.msg_subject = self.__get_cfg('msg_subject')
        self.msg_content = self.__get_cfg('msg_content')
        self.msg_date = self.__get_cfg('msg_date')
        # attachment
        self.attach_file = self.__get_cfg('attach_file', throw=False)


    def login_server(self):
        '''
        login server 登录SMTP服务器
        :return:
        '''
        # QQ邮箱采用的是SMTP_SSL的加密方式，所以要这样写
        # 普通邮箱 server = smtplib.SMTP(self.smtp_server, 25) 这样写
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.set_debuglevel(1)
        server.login(self.msg_from, self.password)
        return server

    def get_main_msg(self):
        '''
        suject content
        处理邮件的主要内容
        :return:msg
        '''
        msg = MIMEMultipart()
        # message content
        msg.attach(MIMEText(self.msg_content, 'plain', 'utf-8'))

        msg['From'] = self._format_addr('From <%s>' % self.msg_from)
        # msgTo = ','.join([to for to in self.msg_to])

        # msg['To'] = self._format_addr('To <%s>' % self.msg_to)
        msg['To'] = ";".join([self._format_addr(u'To <%s>' % to) for to in self.msg_to])
        msg['Subject'] = Header(self.msg_subject, 'utf-8')
        msg['Date'] = self.msg_date
        # msg['Cc'] = self._format_addr('To <%s>' % self.msg_cc)
        msg['To'] = ";".join([self._format_addr(u'To <%s>' % to) for to in self.msg_cc])


        # attachment content
        attach_file = self.get_attach_file()
        if attach_file is not None:
            msg.attach(attach_file)
        return msg

    def get_attach_file(self):
        '''
        获取附件的相关信息
        generate mail attachment content
        :return:
        '''
        if self.attach_file is not None and self.attach_file != '':
            try:
                if getsize(self.attach_file) > self.MAX_FILE_SIZE:
                    # 超出10M，抛出异常
                    raise Exception('The attachment is too large and the upload failed!!')
                with open(self.attach_file, 'rb') as file:
                    # mimetypes是python自带的标准库，可以根据文件的后缀名直接得到文件的MIME类型
                    ctype, encoding = mimetypes.guess_type(self.attach_file)

                    print('ctype:',ctype)
                    print('encoding:',encoding)


                    if ctype is None or encoding is not None:
                        ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    # MIMEBase表示邮件附件对象
                    mime = MIMEBase(maintype, subtype)
                    mime.set_payload(file.read())
                    # set header 设置信息头 filename设置附件名称
                    mime.add_header('Content-Disposition', 'attachment',
                                    filename=os.path.basename(self.attach_file))
                    mime.add_header('Content-ID', '<0>')
                    mime.add_header('X-Attachment-Id', '0')
                    # set the attachment encoding rules 设置编码规则
                    encoders.encode_base64(mime)
                    return mime
            except Exception as e:
                print('%s......' % e)
                return None
        else:
            return None

    def _format_addr(self, s):
        '''
        格式化一个邮件地址:如果包含中文，需要通过Header对象进行编码。
        :param s:
        :return:
        '''
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self):
        '''
        发送邮件
        抄送就是将邮件同时发送给收信人以外的人
        :return:
        '''
        try:
            # initialize the configuration file
            self.__init_cfg()
            # log on to the SMTP server and verify authorization
            server = self.login_server()
            # mail content
            msg = self.get_main_msg()
            # send mail
            # server.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print(1)
            print(set(self.msg_to + self.msg_cc))
            response = server.sendmail(self.msg_from, set(self.msg_to + self.msg_cc), msg.as_string())
            print(response)
            server.quit()
            return "success"
            print("Send succeed!!")
        except smtplib.SMTPException:
            print("Error:Can't send this email!!")
# '1271564669@qq.com',
if __name__ == "__main__":
    mail_cfgs = {'msg_from': '824011142@qq.com', # 发送者的邮箱
                 'password': 'vhqtyotzhhwvbcdc', # 发送者QQ邮箱授权码
                 'msg_to': ['1271564669@qq.com','401952124@qq.com','544782744@qq.com'], # 收件人
                 'msg_cc': ['401952124@qq.com','huotong177@163.com'], # 抄送人
                 'msg_subject': 'Python Auto Send Email', # 标题
                 'msg_content': '', # 正文
                 'attach_file': r'.\spider.jfif', # 附件
                 'msg_date': time.ctime() # 时间戳
                 }

    manager = EmailManager(**mail_cfgs)
    manager.send()