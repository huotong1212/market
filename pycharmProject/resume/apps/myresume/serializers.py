from rest_framework import serializers

from myresume.models import SkillCategory, UserResume, Expectation, Education, Skills, ProjectExperience, SelfAppraise, \
    WorkExperience


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

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = Expectation
        fields = "__all__"  # 包含所有字段


class EducationSerializer(serializers.ModelSerializer):
    # enrollment_date = serializers.DateField(allow_null=True,format="%Y-%m-%d")
    # graduate_date = serializers.DateField(allow_null=True,format="%Y-%m-%d")

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = Education
        fields = "__all__"  # 包含所有字段


class WorkExperienceSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = WorkExperience
        fields = "__all__"  # 包含所有字段


class ProjectExperienceSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = ProjectExperience
        fields = "__all__"  # 包含所有字段


class SkillsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = Skills
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Skills.objects.all(),
        #         fields=('id', 'resume_id'),  如果这里写了id，那么前端就要传递id
        #         message="每个简历只能对应一份自我评价"
        #     )
        # ]
        fields = "__all__"  # 包含所有字段


class SelfAppraiseSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['resume_id'].user == self.context['request'].user:
            return attrs
        else:
            raise serializers.ValidationError('不阔以操作他人的简历')

    class Meta:
        model = SelfAppraise
        fields = "__all__"  # 包含所有字段


class UserResumeShowSerializer(serializers.ModelSerializer):
    expectation = ExpectationSerializer(many=False)
    education = EducationSerializer(many=True)
    work = WorkExperienceSerializer(many=True)
    project = ProjectExperienceSerializer(many=True)
    skills = SkillsSerializer(many=True)
    appraise = SelfAppraiseSerializer(many=False)

    class Meta:
        model = UserResume
        fields = "__all__"  # 包含所有字段