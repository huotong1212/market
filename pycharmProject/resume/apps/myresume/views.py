from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status

from rest_framework.authentication import SessionAuthentication

# Create your views here.
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from myresume.filters import ResumeFilter
from myresume.models import UserResume, SkillCategory, Expectation, Education, WorkExperience, ProjectExperience, \
    Skills, SelfAppraise
from myresume.serializers import UserResumeSerializer, SkillCategorySerializer, ExpectationSerializer, \
    EducationSerializer, WorkExperienceSerializer, ProjectExperienceSerializer, SkillsSerializer, SelfAppraiseSerializer
from utils.permissions import IsOwnerOrReadOnly, IsResumeOwnerOrReadOnly


class UserResumeViewSet(ModelViewSet):
    queryset = UserResume.objects.all()
    # 精确过滤：根据字段过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'language', )

    # 条件筛选
    filter_class = ResumeFilter

    # 搜索功能 ^表示name必须匹配开头
    search_fields = ('name', )

    # 排序
    ordering_fields = ('name', 'language','add_time')

    permission_classes = (IsAuthenticated, IsResumeOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = UserResumeSerializer

    # def destroy(self, request, *args, **kwargs):
    #     print(request.data)
    #     data = request.data
    #     if 'type' in data.keys():
    #         Skills.objects.filter(resume_id=data.get('resumeId'),category=data.get('category')).delete()
    #     else:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


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

    def get_queryset(self):
        return Expectation.objects.filter(resume_id__user=self.request.user)


class ExpectationViewSet(ModelViewSet):
    serializer_class = ExpectationSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Expectation.objects.filter(resume_id__user=self.request.user)


class EducationViewSet(ModelViewSet):
    serializer_class = EducationSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Education.objects.filter(resume_id__user=self.request.user)


class WorkExperienceViewSet(ModelViewSet):
    serializer_class = WorkExperienceSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return WorkExperience.objects.filter(resume_id__user=self.request.user)


class ProjectExperienceViewSet(ModelViewSet):
    serializer_class = ProjectExperienceSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return ProjectExperience.objects.filter(resume_id__user=self.request.user)


class SkillsViewSet(ModelViewSet):
    serializer_class = SkillsSerializer

    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Skills.objects.filter(resume_id__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        if 'category' in data.keys():
            Skills.objects.filter(resume_id=data.get('resumeId'),category=data.get('category')).delete()
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SelfAppraiseViewSet(ModelViewSet):
    serializer_class = SelfAppraiseSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return SelfAppraise.objects.filter(resume_id__user=self.request.user)
