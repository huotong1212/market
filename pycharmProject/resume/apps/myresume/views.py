from django_filters.rest_framework import DjangoFilterBackend
from django_redis import get_redis_connection

from rest_framework import filters, status

from rest_framework.authentication import SessionAuthentication

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.bulk_operations.mixins import ListUpdateModelMixin, ListDestroyModelMixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from myresume.filters import ResumeFilter, SkillsFilter
from myresume.models import UserResume, SkillCategory, Expectation, Education, WorkExperience, ProjectExperience, \
    Skills, SelfAppraise
from myresume.serializers import UserResumeSerializer, SkillCategorySerializer, ExpectationSerializer, \
    EducationSerializer, WorkExperienceSerializer, ProjectExperienceSerializer, SkillsSerializer, \
    SelfAppraiseSerializer, UserResumeShowSerializer

from utils.Des import DesCode
from utils.permissions import IsOwnerOrReadOnly, IsResumeOwnerOrReadOnly

from django_bulk_update.helper import bulk_update

def setInstance(instance, data):
    for key, value in data.items():
        print(key, value)
        if hasattr(instance, key):
            setattr(instance, key, value)
        return instance

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
    # Education.objects.bulk_update()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        resumeId = kwargs.pop('pk')
        try:
            # serializer = self.get_serializer(data=request.data, many=True)
            # serializer.is_valid(raise_exception=True)
            # data = serializer.validated_data
            # serializer.save() 此操作会创建
            instances = []
            for newInstance in request.data:
                instance = Education.objects.get(id=int(newInstance['id']))
                print(newInstance, type(newInstance))
                serializer = self.get_serializer(instance, data=newInstance, partial=partial)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                instances.append(setInstance(instance,serializer.validated_data))
                # print(dir(instance))
                # print(vars(instance))
                # print(data)
                # print(hasattr(instance,'id'))
                # print('--------')
                # self.perform_update(serializer)
            print(11111)
            # Education.objects.bulk_update(instances)
            bulk_update(instances)  # updates only name column
            re_dict = {'message': 'success'}
            return Response(re_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            re_dict = {'message': 'fail'}
            return Response(re_dict)

    def get_queryset(self):
        try:
            if self.action == 'list':
                query_params = self.request.query_params
                resumeId = query_params['resumeId']
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
                query_params = self.request.query_params
                resumeId = query_params['resumeId']
                return WorkExperience.objects.filter(resume_id=resumeId)
            else:
                return WorkExperience.objects.filter(resume_id__user=self.request.user)
        except Exception as e:

            return WorkExperience.objects.filter(resume_id__user=self.request.user)


class ProjectExperienceViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = ProjectExperienceSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

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
                query_params = self.request.query_params
                resumeId = query_params['resumeId']
                return ProjectExperience.objects.filter(resume_id=resumeId)
            else:
                return ProjectExperience.objects.filter(resume_id__user=self.request.user)
        except Exception as e:
            return ProjectExperience.objects.filter(resume_id__user=self.request.user)


class SkillsViewSet(ListDestroyModelMixin,ListUpdateModelMixin,ModelViewSet):
    # ListUpdateModelMixin批量操作可以成功，但是只能统一修改单一字段，并且必须要有操作权限
    # queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # lookup_field = "resume_id_id"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    search_fields = ('=resume_id__id',)
    filter_class = SkillsFilter

    # def get_queryset(self):
    # try:
    #     if self.action == 'list':
    #         query_params = self.request.query_params
    #         resumeId = query_params['resumeId']
    #         return Skills.objects.filter(resume_id=resumeId)
    #     else:
    #         return Skills.objects.filter(resume_id__user=self.request.user)
    # except Exception as e:
    #     return Skills.objects.filter(resume_id__user=self.request.user)
    #        return Skills.objects.filter(resume_id__user=self.request.user)

    def get_queryset(self):
        # 当在queryset中的查询需要用到用户时，需要在permission_classes设置IsAuthenticated登录可见
        # 否则在DRF登录时会报错 匿名用户无法转换为Int
        return Skills.objects.filter(resume_id__user=self.request.user)

    # def destroy(self, request, *args, **kwargs):
    #     # print(request.data)
    #     data = request.data
    #     if 'category' in data.keys():
    #         Skills.objects.filter(resume_id=data.get('resumeId'), category=data.get('category')).delete()
    #     else:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class SelfAppraiseViewSet(ModelViewSet):
    serializer_class = SelfAppraiseSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "resume_id_id"

    def get_queryset(self):
        return SelfAppraise.objects.filter(resume_id__user=self.request.user)


class UserResumeShowView(GenericAPIView):
    serializer_class = UserResumeShowSerializer

    def get(self, request, *args, **kwargs):
        try:
            query_params = request.query_params
            code = query_params['code']

            des = DesCode()
            str_x = code.encode('utf-8')  # 接受前端，encode专为字节方便解密
            str_x = des.des_descrypt(str_x).decode('utf-8')

            codelist = str_x.split(';')
            id, username, resumeId = int(codelist[0]), codelist[1], int(codelist[2])

            instance = UserResume.objects.filter(id=resumeId)[0]

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response({'code': 'code不存在'}, status=status.HTTP_404_NOT_FOUND)


class UserResumeAnthorView(GenericAPIView):
    serializer_class = UserResumeShowSerializer

    def get(self, request, *args, **kwargs):
        try:
            query_params = request.query_params

            code = query_params['code']

            des = DesCode()
            str_x = code.encode('utf-8')  # 接受前端，encode专为字节方便解密
            str_x = des.des_descrypt(str_x).decode('utf-8')

            codelist = str_x.split(';')
            id, username, resumeId = int(codelist[0]), codelist[1], int(codelist[2])

            languge = query_params['language']

            instance = UserResume.objects.filter(user_id=id, language=languge).order_by('updatetime')[0]

            serializer = self.get_serializer(instance)
            print(222, request.user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'resume': 'resume不存在'}, status=status.HTTP_404_NOT_FOUND)


class GenerateSecret(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request, format=None):
        username = request.user.username
        id = request.user.id
        resume_id = request.data['resumeId']

        secret = ';'.join([str(id), str(username), str(resume_id)])
        print(secret)
        des = DesCode()

        str_en = des.des_encrypt(secret.encode('utf-8'))  # 加密
        code = str_en.decode('utf-8')  # 转成utf-8返回给前端
        print(code)

        return Response({'code': code}, status=status.HTTP_200_OK)
