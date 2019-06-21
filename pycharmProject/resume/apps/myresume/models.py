from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField
from resume.settings import MEDIA_ROOT

User = get_user_model()


# 让上传的文件路径动态地与user的名字有关
def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, 'userProfile', instance.username, filename])


class UserResume(models.Model):
    CATEGORY_TYPE = (
        (0, "中文"),
        (1, "英语"),
        (2, "日语")
    )

    user = models.ForeignKey(User, verbose_name="用户", related_name="resume", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="简历名称", help_text="简历名称")  # 名称
    language = models.IntegerField(choices=CATEGORY_TYPE, default=0, null=True, blank=True, verbose_name="语言")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    updatetime = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    username = models.CharField(null=True, blank=True, max_length=20, verbose_name="姓名", help_text="姓名")  # 姓名
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name="邮箱")
    # choice Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    age = models.IntegerField(default=0, null=True, blank=True, verbose_name="年龄")
    portrait = models.ImageField(blank=True, null=True, upload_to=upload_to, verbose_name='用户头像')

    class Meta:
        verbose_name = "用户简历"
        verbose_name_plural = verbose_name
        # unique_together = ('user', 'language')

    def __str__(self):
        return self.name


class SkillCategory(models.Model):
    """
    技能类别,当存在多级分类关系时，其实不需要设计多个model，只要设计一个model让他自关联就可以了
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
        verbose_name = "技能类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Expectation(models.Model):
    '''
    期望职业
    '''
    DUTY_TIME = (
        (1, "一个月之内"),
        (2, "两个月之内"),
        (3, "一周之内")
    )

    job = models.CharField(max_length=30, null=True, blank=True, verbose_name="职位")
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="城市")
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="省")
    salary_min = models.FloatField(default=0, null=True, blank=True, verbose_name="最低薪资")
    salary_max = models.FloatField(default=0, null=True, blank=True, verbose_name="最高薪资")

    duty_time = models.IntegerField(default=1, choices=DUTY_TIME, verbose_name="到岗时间",
                                    help_text=u"到岗时间: 1(一个月之内),2(两个月之内),3(一周之内)")
    resume_id = models.OneToOneField(UserResume, verbose_name="简历ID", related_name="expectation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "期望职业"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.job


class Education(models.Model):
    '''
    教育背景
    '''
    enrollment_date = models.DateField(default=date.today, verbose_name="入学日期")
    graduate_date = models.DateField(default=date.today, verbose_name="毕业日期")
    dateP = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name="日期区间")

    graduate_school = models.CharField(max_length=50, default="苏州科技大学", null=True, blank=True, verbose_name="毕业院校")
    subjects = models.CharField(max_length=200, default="", null=True, blank=True, verbose_name="主修课程")
    emphasize = models.CharField(max_length=200, default="", null=True, blank=True, verbose_name="突出内容")

    resume_id = models.ForeignKey(UserResume, verbose_name="简历ID", related_name="education", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "教育背景"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.graduate_school


class WorkExperience(models.Model):
    '''
    工作经验
    '''
    start_time = models.DateField(default=date.today, verbose_name="起始日期")
    end_time = models.DateField(default=date.today, verbose_name="结束日期")
    company = models.CharField(default="公司名称", max_length=30, null=True, blank=True, verbose_name="任职公司")
    profession = models.CharField(max_length=30, null=True, blank=True, verbose_name="岗位名称")
    department = models.CharField(max_length=30, null=True, blank=True, verbose_name="部门")
    duty = models.TextField(null=True, blank=True, verbose_name="岗位职责")
    resume_id = models.ForeignKey(UserResume, verbose_name="简历ID", related_name="work", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "工作经验"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.company


class ProjectExperience(models.Model):
    """
    项目经验
    """
    start_time = models.DateField(default=date.today, verbose_name="起始日期")
    end_time = models.DateField(default=date.today, verbose_name="结束日期")
    project_name = models.CharField(default='项目名称',max_length=30, null=True, blank=True, verbose_name="项目名称")
    project_skills = models.CharField(max_length=200, null=True, blank=True, verbose_name="项目技术")
    tasks = UEditorField(verbose_name=u"项目职责", imagePath="project/images/", width=1000, height=300,
                         filePath="project/files", default="")
    resume_id = models.ForeignKey(UserResume, verbose_name="简历ID", related_name="project", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "项目经验"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.project_name


class Skills(models.Model):
    """
    技能特长
    """
    LEVEL_CHOICES = (
        (1, "了解"),
        (2, "熟练"),
        (3, "精通"),
        (4, "大牛"),
    )
    category = models.ForeignKey(SkillCategory, verbose_name="技能类别", related_name="skills", on_delete=models.CASCADE)
    skill_tag = models.CharField(max_length=200, null=True, blank=True, verbose_name="技能标签")
    skill_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="技能描述")
    skill_level = models.IntegerField(default=1, choices=LEVEL_CHOICES, verbose_name="熟练程度",
                                      help_text=u"技能熟练度: 1(了解),2(熟练),3(精通),4(大牛)")
    resume_id = models.ForeignKey(UserResume, verbose_name="简历ID", related_name="skills", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "技能特长"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.skill_desc


class SelfAppraise(models.Model):
    """
    自我评价
    """
    self_desc = models.TextField(max_length=300, null=True, blank=True, verbose_name="自我评价")
    resume_id = models.OneToOneField(UserResume, verbose_name="简历ID", related_name="appraise", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "自我评价"  # admin中显示的表名称
        verbose_name_plural = verbose_name  # admin中显示的表的复数名称

    def __str__(self):  # 相当于java中的tostring
        return self.resume_id.name
