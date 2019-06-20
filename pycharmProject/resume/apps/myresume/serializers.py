from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from myresume.models import SkillCategory, UserResume, Expectation, Education, Skills, ProjectExperience, SelfAppraise, \
    WorkExperience
from user.serializers import UserDetailSerializer


class SkillCategorySerializer3(serializers.ModelSerializer):
    '''
    三级分类
    '''

    class Meta:
        model = SkillCategory
        fields = "__all__"  # 包含所有字段


class SkillCategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    sub_cat = SkillCategorySerializer3(many=True)

    class Meta:
        model = SkillCategory
        fields = "__all__"  # 包含所有字段


class SkillCategorySerializer(serializers.ModelSerializer):
    '''
    一级分类
    '''
    sub_cat = SkillCategorySerializer2(many=True)

    class Meta:
        model = SkillCategory
        fields = "__all__"  # 包含所有字段


class UserResumeSerializer(serializers.ModelSerializer):
    # user = UserDetailSerializer(many=False)
    # 获取当前用户,并且隐藏了该字段，不会序列号返回给前端
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserResume
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserResume.objects.all(),
        #         fields=('user', 'language'),
        #         message="已经添加"
        #     )
        # ]
        fields = "__all__"  # 包含所有字段


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expectation
        fields = "__all__"  # 包含所有字段


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"  # 包含所有字段


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"  # 包含所有字段


class ProjectExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectExperience
        fields = "__all__"  # 包含所有字段


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"  # 包含所有字段


class SelfAppraiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfAppraise
        fields = "__all__"  # 包含所有字段
