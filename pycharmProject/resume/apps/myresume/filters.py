from django.db.models import Q
from rest_framework import generics
from django_filters import rest_framework as filters

from myresume.models import UserResume, Skills


class ResumeFilter(filters.FilterSet):
    '''
    简历的过滤类
    '''
    # contains 模糊查询（like） i忽略大小写
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = UserResume
        fields = ['name', 'language', 'add_time']


class SkillsFilter(filters.FilterSet):
    resume_id = filters.NumberFilter(field_name="resume_id", lookup_expr='exact')

    class Meta:
        model = Skills
        fields = ['resume_id', ]
