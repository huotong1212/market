"""resume URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView

import xadmin
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

from myresume.views import UserResumeViewSet, SkillCategoryViewSet, ExpectationViewSet, EducationViewSet, \
    WorkExperienceViewSet, ProjectExperienceViewSet, SkillsViewSet, SelfAppraiseViewSet, GenerateSecret, \
    UserResumeShowView, UserResumeAnthorView
from resume.settings import MEDIA_ROOT
from user.views import PermissionViewSet, UserViewSet, SmsCodeViewSet, EmailCodeViewSet, ResetPasswordViewSet, \
    CheckEmailCodeView
# 导入辅助函数get_schema_view
from rest_framework.schemas import get_schema_view
# 导入两个类
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

router = DefaultRouter()

# 用戶简历
router.register(r'userResume', UserResumeViewSet, base_name="userResume")

# 技术分类
router.register(r'skillCategory', SkillCategoryViewSet, base_name="skillCategory")

# 期望薪资
router.register(r'expectation', ExpectationViewSet, base_name="expectation")

# 教育背景
router.register(r'education', EducationViewSet, base_name="education")

# 工作经验
router.register(r'workExperience', WorkExperienceViewSet, base_name="workExperience")

# 项目经验
router.register(r'projectExperience', ProjectExperienceViewSet, base_name="projectExperience")

# 技能特长
router.register(r'skills', SkillsViewSet, base_name="skills")

# 自我评价
router.register(r'selfAppraise', SelfAppraiseViewSet, base_name="selfAppraise")

# 用户权限
router.register(r'permission', PermissionViewSet, base_name="permission")

# 用户注册，获取个人信息
router.register(r'user', UserViewSet, base_name="user")

# 短信验证码
router.register(r'sms', SmsCodeViewSet, base_name="sms")

# 邮箱验证码
router.register(r'email', EmailCodeViewSet, base_name="email")

# 邮箱验证码
router.register(r'resetPas', ResetPasswordViewSet, base_name="resetPas")

# 利用辅助函数引入所导入的两个类
schema_view = get_schema_view(title='API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])
# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'checkPas/$', CheckEmailCodeView.as_view(), name="checkPas"),
    url(r'secret/$', GenerateSecret.as_view(), name="secret"),
    url(r'showResume/$', UserResumeShowView.as_view(), name="showResume"),
    url(r'another/$', UserResumeAnthorView.as_view(), name="another"),

    # url(r'userResume/',UserResume
    # ViewSet.as_view()),
    # 引入restframework自动生成的文档
    # url(r'docs/', include_docs_urls(title="我的简历")),
    url(r'^xadmin/', xadmin.site.urls),

    url('^', include(router.urls)),

    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),

    # 这个url是为了可以弹出rest_framework提供的登录页面，方便测试的时候操作
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^$', schema_view),
    url(r'^swagger_docs/', schema_view, name="swagger_docs"),

    # url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
]
