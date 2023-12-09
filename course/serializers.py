
from rest_framework import serializers

from accounts.models import UserAccount
from .models import Category, Course, Feature, Lesson, LiveClass,SubCategory, Subscription
from .models import Plan


#<----------------------------------------------------Category-Start---------------------------------------------------------------->
#Admin side
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'image', 'is_active']



#<----------------------------------------------------Category-End----------------------------------------------------------->

#<----------------------------------------------------Subcategory-Start---------------------------------------------------------------->


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_ref.category_name')

    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name', 'category_name', 'is_active']

#<----------------------------------------------------Subcategory-End---------------------------------------------------------------->

#<----------------------------------------------------Course-Start---------------------------------------------------------------->

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email']

class CourseSerializer(serializers.ModelSerializer):
    category_ref = CategorySerializer(required=False)
    sub_category_ref = SubCategorySerializer(required=False)
    tutor_ref = UserAccountSerializer(required=False)

    class Meta:
        model = Course
        fields = '__all__'

class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'preview_video']
#<----------------------------------------------------Course-End---------------------------------------------------------------->

#<----------------------------------------------------Live-Start---------------------------------------------------------------->

class CreateLiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = ['id', 'title', 'start_time', 'date', 'status', 'access_code', 'course_ref', 'tutor_ref']

class TutorLiveListSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course_ref.course_name')
    start_time = serializers.DateTimeField(format="%I:%M %p")
    class Meta:
        model = LiveClass

        fields = ('id', 'title', 'start_time', 'date', 'status', 'access_code', 'course_ref', 'course_name')

class LiveClassSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%I:%M %p")
    class Meta:
        model = LiveClass
        fields = ['id', 'title', 'start_time', 'date', 'status', 'access_code', 'course_ref', 'tutor_ref']
#<----------------------------------------------------Live-End---------------------------------------------------------------->

#<----------------------------------------------------Lessons-Start---------------------------------------------------------------->
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'lesson_name', 'lesson_video', 'thumbnail_image', 'course_ref','tutor_ref']

class TutorLessonSerializer(serializers.ModelSerializer):
    
    course_ref = CourseSerializer(required=False)

    class Meta:
        model = Lesson
        fields = '__all__'
#<----------------------------------------------------Lessons-End---------------------------------------------------------------->

#<----------------------------------------------------Plan-Start---------------------------------------------------------------->

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'type', 'amount', 'is_active']

class FeatureSerializer(serializers.ModelSerializer):
    plan_name = serializers.ReadOnlyField(source='entry.type')  # Assuming 'entry' is a ForeignKey to Plan model with a 'name' field

    class Meta:
        model = Feature
        fields = ['id', 'entry', 'feature_text', 'plan_name']

#<----------------------------------------------------Plan-End---------------------------------------------------------------->

#<----------------------------------------------------Subscription-Start---------------------------------------------------------------->

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'expire_date': {'required': False},
        }

class SubscriptionListSerializer(serializers.ModelSerializer):
    user_ref = UserAccountSerializer()
    plan_ref = PlanSerializer() 

    class Meta:
        model = Subscription
        fields = '__all__'
#<----------------------------------------------------Subscription-End---------------------------------------------------------------->
