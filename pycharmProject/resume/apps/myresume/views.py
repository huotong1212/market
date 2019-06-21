from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status

from rest_framework.authentication import SessionAuthentication

# Create your views here.
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from myresume.filters import ResumeFilter
from myresume.models import UserResume, SkillCategory, Expectation, Education, WorkExperience, ProjectExperience, \
    Skills, SelfAppraise
from myresume.serializers import UserResumeSerializer, SkillCategorySerializer, ExpectationSerializer, \
    EducationSerializer, WorkExperienceSerializer, ProjectExperienceSerializer, SkillsSerializer, SelfAppraiseSerializer
from utils.permissions import IsOwnerOrReadOnly, IsResumeOwnerOrReadOnly


class UserResumePagination(PageNumberPagination):
    page_size = 8  # 默认每页显示的数据条数
    page_size_query_param = 'page_size'  # 获取url参数中设置的每页显示数据条数
    page_query_param = "page"  # 获取url中传入的页码key
    max_page_size = 10  # 最大支持的每页显示的数据条数


class UserResumeViewSet(ModelViewSet):
    queryset = UserResume.objects.all()

    pagination_class = UserResumePagination

    # 精确过滤：根据字段过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'language',)

    # 条件筛选
    filter_class = ResumeFilter

    # 搜索功能 ^表示name必须匹配开头
    search_fields = ('name',)

    # 排序
    ordering_fields = ('name', 'language', 'add_time')

    permission_classes = (IsAuthenticated, IsResumeOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = UserResumeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        userResume = self.perform_create(serializer)
        Expectation.objects.create(resume_id=userResume)
        SelfAppraise.objects.create(resume_id=userResume)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return UserResume.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        data = request.data
        if 'type' in data.keys():
            UserResume.objects.filter(id__in=data.get('selectedId')).delete()
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SkillCategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = SkillCategory.objects.filter(category_type=1) \
        .prefetch_related("parent_category", "parent_category__parent_category")

    # 精确过滤：根据字段过滤
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'category_type')
    serializer_class = SkillCategorySerializer


class ExpectationViewSet(ModelViewSet):
    serializer_class = ExpectationSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'resume_id_id'

    def get_queryset(self):
        return Expectation.objects.filter(resume_id__user=self.request.user)


class EducationViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = EducationSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # lookup_field = 'resume_id_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        resumeId = kwargs.pop('pk')
        try:
            for newInstance in request.data:
                instance = Education.objects.get(id=int(newInstance['id']))
                print(newInstance, type(newInstance))
                serializer = self.get_serializer(instance, data=newInstance, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                re_dict = {'message': 'success'}
            return Response(re_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            re_dict = {'message': 'fail'}
            return Response(re_dict)

    def get_queryset(self):
        try:
            if self.action == 'list':
                resumeId = self.request.data['resumeId']
                return Education.objects.filter(resume_id=resumeId)
            else:
                return Education.objects.filter(resume_id__user=self.request.user)
        except Exception as e:
            # print(e)
            return Education.objects.filter(resume_id__user=self.request.user)


class WorkExperienceViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = WorkExperienceSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # def get_queryset(self):
    #     return WorkExperience.objects.filter(resume_id__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        resumeId = kwargs.pop('pk')
        try:
            for newInstance in request.data:
                instance = WorkExperience.objects.get(id=int(newInstance['id']))
                # print(newInstance, type(newInstance))
                serializer = self.get_serializer(instance, data=newInstance, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                re_dict = {'message': 'success'}
            return Response(re_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            re_dict = {'message': 'fail'}
            return Response(re_dict)

    def get_queryset(self):
        try:
            if self.action == 'list':
                resumeId = self.request.data['resumeId']
                return WorkExperience.objects.filter(resume_id=resumeId)
            else:
                return WorkExperience.objects.filter(resume_id__user=self.request.user)
        except Exception as e:

            return WorkExperience.objects.filter(resume_id__user=self.request.user)


class ProjectExperienceViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = ProjectExperienceSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # def get_queryset(self):
    #     return ProjectExperience.objects.filter(resume_id__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        resumeId = kwargs.pop('pk')
        try:
            for newInstance in request.data:
                instance = ProjectExperience.objects.get(id=int(newInstance['id']))
                # print(newInstance, type(newInstance))
                serializer = self.get_serializer(instance, data=newInstance, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                re_dict = {'message': 'success'}
            return Response(re_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            re_dict = {'message': 'fail'}
            return Response(re_dict)

    def get_queryset(self):
        try:
            if self.action == 'list':
                resumeId = self.request.data['resumeId']
                return ProjectExperience.objects.filter(resume_id=resumeId)
            else:
                return ProjectExperience.objects.filter(resume_id__user=self.request.user)
        except Exception as e:
            return ProjectExperience.objects.filter(resume_id__user=self.request.user)


class SkillsViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = SkillsSerializer

    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # def get_queryset(self):
    #     return Skills.objects.filter(resume_id__user=self.request.user)

    def get_queryset(self):
        try:
            if self.action == 'list':
                resumeId = self.request.data['resumeId']
                return Skills.objects.filter(resume_id=resumeId)
            else:
                return Skills.objects.filter(resume_id__user=self.request.user)
        except Exception as e:

            return Skills.objects.filter(resume_id__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # print(request.data)
        data = request.data
        if 'category' in data.keys():
            Skills.objects.filter(resume_id=data.get('resumeId'), category=data.get('category')).delete()
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SelfAppraiseViewSet(ModelViewSet):
    serializer_class = SelfAppraiseSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "resume_id_id"

    def get_queryset(self):
        return SelfAppraise.objects.filter(resume_id__user=self.request.user)
