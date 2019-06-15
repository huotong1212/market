#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from xadmin import views

from .models import UserResume,SkillCategory,Expection,Education,WorkExperience,ProjectExperience,Skills,SelfAppraise


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "简历后台"
    site_footer = "myresume"
    # menu_style = "accordion"


class UserResumeAdmin(object):
    list_display = ['user', 'language', "add_time","updatetime"]

class SkillCategoryAdmin(object):
    list_display = ['name', 'code','desc',"category_type","parent_category","is_tab", "add_time"]

class ExpectionAdmin(object):
    list_display = ['job', 'city','salary', "duty_time","resume_id"]

class EducationAdmin(object):
    list_display = ['enrollment_date', 'graduate_date','graduate_school', "subjects","emphasize","resume_id"]

class WorkExperienceAdmin(object):
    list_display = ['start_time', 'end_time',"company",'profession', "department","duty","resume_id"]

class ProjectExperienceAdmin(object):
    list_display = ['start_time', 'end_time','project_name', "project_skills","tasks","resume_id"]

class SkillsAdmin(object):
    list_display = ['category', 'skill_desc',"skill_level","resume_id"]

class SelfAppraiseAdmin(object):
    list_display = ['self_desc', "resume_id"]


xadmin.site.register(UserResume,UserResumeAdmin)
xadmin.site.register(SkillCategory,SkillCategoryAdmin)
xadmin.site.register(Expection,ExpectionAdmin)
xadmin.site.register(Education,EducationAdmin)
xadmin.site.register(WorkExperience,WorkExperienceAdmin)
xadmin.site.register(ProjectExperience,ProjectExperienceAdmin)
xadmin.site.register(Skills,SkillsAdmin)
xadmin.site.register(SelfAppraise,SelfAppraiseAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)