
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from datetime import datetime, date
from accounts.models import UserAccount
from .models import Category, Course, Feature, Lesson, LiveClass, Plan,SubCategory, Subscription
from .serializers import AddCourseSerializer, CategorySerializer, CourseSerializer, FeatureSerializer, LessonSerializer, CreateLiveClassSerializer, LiveClassSerializer, PlanSerializer,SubCategorySerializer, SubscriptionListSerializer, SubscriptionSerializer, TutorLessonSerializer, TutorLiveListSerializer, UpdateCourseSerializer
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


from django.utils.decorators import method_decorator
from decouple import config  # Import config from python-decouple
import razorpay


#<----------------------------------------------------Category-Start---------------------------------------------------------------->

#Admin side
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#User side
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 4  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100
class UserCategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        # Access data using names
        category_name = request.POST.get('categoryName', '').strip()
        image = request.FILES.get('image', None)
        print(image,'image........................')

        # Check if the category name is unique
        if Category.objects.filter(category_name__iexact=category_name).exists():
            return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'category_name': category_name, 'image': image})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UpdateCategoryView(APIView):
    def put(self, request, category_id, *args, **kwargs):
        try:
            category = Category.objects.get(id=category_id)
         
            updated_category_data = {
                "category_name": request.data.get("category_name"),
                
            }
            img =request.data.get("image")

            if not isinstance(img, str): # this check the image path is string or not
                updated_category_data["image"] = img
                        
            serializer = CategorySerializer(category, data=updated_category_data, partial=True)
           

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class BlockUnblockCategoryView(UpdateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

#<----------------------------------------------------Category-End----------------------------------------------------------->


#<----------------------------------------------------Subcategory-Start---------------------------------------------------------------->

#Admin Side
class SubCategoryListView(APIView):
    def get(self, request):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubCategoryAddView(APIView):
    def post(self, request):

        # Extract 'category_name' directly from the request data
        category_name = request.data.get('category_name')

        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            # Check if the category with the given name already exists
            try:
                category = Category.objects.get(category_name=category_name)
            except Category.DoesNotExist:
                return Response({'error': f'Category "{category_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(category_ref=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubCategoryEditView(APIView):
    def get_object(self, subcategory_id):
        try:
            return SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return None

    def get(self, request, subcategory_id):
        subcategory = self.get_object(subcategory_id)
        if subcategory is not None:
            serializer = SubCategorySerializer(subcategory)
            return Response(serializer.data)
        else:
            return Response({'error': f'SubCategory with id {subcategory_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, subcategory_id):
        subcategory = self.get_object(subcategory_id)
        if subcategory is not None:
            serializer = SubCategorySerializer(subcategory, data=request.data)
            if serializer.is_valid():
                # Extract 'category_name' directly from the request data
                category_name = request.data.get('category_name')

                # Check if the category with the given name already exists
                try:
                    category = Category.objects.get(category_name=category_name)
                except Category.DoesNotExist:
                    return Response({'error': f'Category "{category_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                # Check if the subcategory name is unique within the given category
                if SubCategory.objects.filter(category_ref=category, sub_category_name=serializer.validated_data['sub_category_name']).exclude(id=subcategory_id).exists():
                    return Response({'error': f'SubCategory name must be unique within the category.'}, status=status.HTTP_400_BAD_REQUEST)

                serializer.save(category_ref=category)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f'SubCategory with id {subcategory_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

class BlockUnblockSubCategoryView(UpdateAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

#User side and admin side
class CSubCategoryListView(APIView): # subcategory list correspond category id 
    def get(self, request, category_id, format=None):
        try:
            subcategories = SubCategory.objects.filter(category_ref=category_id)
            serializer = SubCategorySerializer(subcategories, many=True)
            return Response(serializer.data)
        except SubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#<----------------------------------------------------Subcategory-End---------------------------------------------------------------->

#<----------------------------------------------------Course-Start---------------------------------------------------------------->

#User side

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'  # Use the 'id' field for looking up instances


#admin side
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

#User side
# class CourseListPagination(PageNumberPagination):
#     page_size = 4
#     page_size_query_param = 'page_size'
#     max_page_size = 100

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        sub_category_ref_id = self.request.query_params.get('sub_category_ref', None)
        
        if sub_category_ref_id:
            # Filter courses based on sub_category_ref_id
            queryset = Course.objects.filter(sub_category_ref=sub_category_ref_id)
        else:
            # If no sub_category_ref_id is provided, return all courses
            queryset = Course.objects.all()

        return queryset
    # pagination_class = CourseListPagination


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = AddCourseSerializer


class BlockUnblockCourseView(UpdateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)


#Tutor side course list
class TutorCoursesListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get_queryset(self):
        # Get the tutor's ID from the authenticated user
        tutor_id = self.request.user.id  # Assuming the tutor is the authenticated user
        return Course.objects.filter(tutor_ref_id=tutor_id, is_active=True)

class CourseUpdateView(APIView):
    def patch(self, request, course_id, *args, **kwargs):
        print(request.data,'request')
        try:
            course = Course.objects.get(id=course_id)
            updated_course_data = {
                "course_name": request.data.get("course_name"),
            }

            preview_video = request.data.get("preview_video")
            if preview_video is not None:
                if not isinstance(preview_video, str):
                    updated_course_data["preview_video"] = preview_video

            serializer = UpdateCourseSerializer(course, data=updated_course_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


#<----------------------------------------------------Course-Start---------------------------------------------------------------->

#<----------------------------------------------------Live-Start---------------------------------------------------------------->

class LiveClassListCreateView(generics.ListCreateAPIView):
    queryset = LiveClass.objects.all()
    serializer_class = CreateLiveClassSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def create(self, request, *args, **kwargs):
        # Automatically set the tutor_ref to the authenticated user
        request.data['tutor_ref'] = request.user.id
        print(request.data,'live dataaaaaaaaaaaaaaa')
        return super().create(request, *args, **kwargs)

class TutorLiveListView(generics.ListAPIView):
    serializer_class = TutorLiveListSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Get the tutor's live classes based on the authenticated user
        tutor_id = self.request.user.id
        return LiveClass.objects.filter(tutor_ref=tutor_id)

class ListLiveClassesTodayView(APIView):
    def get(self, request, *args, **kwargs):
        current_date = timezone.now().date()

        live_classes_today = LiveClass.objects.filter(date=current_date)

        serializer = TutorLiveListSerializer(live_classes_today, many=True)

        return Response(serializer.data)

class UpdateLiveClassStatusView(generics.UpdateAPIView):
    queryset = LiveClass.objects.all()
    serializer_class = LiveClassSerializer

    def partial_update(self, request, *args, **kwargs):
        # Override partial_update to update only the 'status' field
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=request.data.get('status', instance.status))
        return super().partial_update(request, *args, **kwargs)

#User side

class UserLiveClassListView(generics.ListAPIView):
   
    serializer_class = LiveClassSerializer
    def get_queryset(self):
        today_date = date.today()
        # Filter only those LiveClass objects with status other than 'completed'
        return LiveClass.objects.exclude(status='completed')

#<----------------------------------------------------Live-Start---------------------------------------------------------------->

#<----------------------------------------------------Lessons-Start---------------------------------------------------------------->

#Tutor side
class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the lessons based on the authenticated tutor
        tutor_id = self.request.user.id
        return Lesson.objects.filter(tutor_ref=tutor_id)


class TutorLessonsListView(generics.ListAPIView):
    serializer_class = TutorLessonSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Get the tutor's lessons classes based on the authenticated user
        tutor_id = self.request.user.id
        return Lesson.objects.filter(tutor_ref=tutor_id)


class LessonUpdateView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=pk)

            updated_lesson_data = {
                "lesson_name": request.data.get("lesson_name"),
                # Add other fields as needed
            }

            thumbnail_image = request.data.get("thumbnail_image")
            if not isinstance(thumbnail_image, str):
                updated_lesson_data["thumbnail_image"] = thumbnail_image

            lesson_video = request.data.get("lesson_video")
            if not isinstance(lesson_video, str):
                updated_lesson_data["lesson_video"] = lesson_video

            serializer = LessonSerializer(lesson, data=updated_lesson_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

#User side

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Lesson.objects.filter(course_ref__id=course_id)

 

#<----------------------------------------------------Lessons-End---------------------------------------------------------------->

#<----------------------------------------------------Plan-Start---------------------------------------------------------------->
class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    
class PlanCreateView(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data

        # Create a new plan object
        serializer = PlanSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockUnblockPlanView(UpdateAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

class FeatureListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureDetailView(generics.ListAPIView):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        plan_id = self.kwargs.get('plan_id')  # Assuming the plan_id is passed in the URL
        return Feature.objects.filter(entry_id=plan_id)


class FeatureCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate if plan_name is provided in the request data
        plan_name = request.data.get('plan_name')

        if not plan_name:
            return Response({'error': 'plan_name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a Plan with the given name exists
        try:
            plan = Plan.objects.get(type=plan_name)
        except Plan.DoesNotExist:
            return Response({'error': f'Plan with name "{plan_name}" does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # If Plan exists, proceed to create the Feature
        feature_data = {
            'entry': plan.id,
            'feature_text': request.data.get('feature_text')
        }

        serializer = FeatureSerializer(data=feature_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeatureUpdateView(RetrieveUpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
#<----------------------------------------------------Plan-End---------------------------------------------------------------->

#<----------------------------------------------------Subscription-Start---------------------------------------------------------------->

#Admin side
class SubscriptionListView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer



#User Side
def get_plan_type(plan_id):
    try:
        plan = Plan.objects.get(id=plan_id)
        return plan.type  
    except Plan.DoesNotExist:
        return None


from django.utils import timezone
from datetime import timedelta

def calculate_expire_date(plan_type):
    # Implement the logic to calculate expire_date based on plan type
    if plan_type == 'Basic':
        return timezone.now() + timedelta(days=30)
    elif plan_type == 'Medium':
        return timezone.now() + timedelta(days=365)
    else:
        # Handle the case where plan_type is not recognized
        raise ValueError(f"Unsupported plan type: {plan_type}")

class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data['plan_ref'].id
        amount = serializer.validated_data['amount']
        user_id = serializer.validated_data['user_ref'].id

        # Calculate expire_date based on plan type
        plan_type = get_plan_type(plan_id)
        expire_date = calculate_expire_date(plan_type)

        # Create the Subscription object
        subscription_data = {
            'user_ref': user_id,
            'plan_ref': plan_id,
            'amount': amount,
            'subscription_type': plan_type,
        }

        # Add expire_date to subscription_data only if it is not None
        if expire_date is not None:
            subscription_data['expire_date'] = expire_date

        # Update the UserAccount model with the current subscription plan
        user_account = get_object_or_404(UserAccount, id=user_id)
        user_account.subscription_plan = plan_type
        user_account.save()

        serializer = SubscriptionSerializer(data=subscription_data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


#user correspond subscription detail list

class UserSubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter subscriptions for the currently authenticated user
        return Subscription.objects.filter(user_ref=self.request.user)

#<----------------------------------------------------Subscription-End---------------------------------------------------------------->

#<----------------------------------------------------Payment-Gateway-Start---------------------------------------------------------------->

class RazorpayOrderView(APIView):

    # @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            plan_id = request.data.get('planId')
            amount = request.data.get('amount')


            # Initialize Razorpay client with environment variables
            client = razorpay.Client(auth=(config('RAZORPAY_KEY_ID'), config('RAZORPAY_KEY_SECRET')))
            # Create a Razorpay order
            order_params = {
                'amount': float(amount) * 100,  # Amount in paise
                'currency': 'INR',
                'receipt': 'receipt_id',  # Replace with a unique identifier for the order
                'payment_capture': 1,
                'notes': {
                    'plan_id': plan_id,
                    'key':config('RAZORPAY_KEY_ID'),
                },
            }
            print(order_params,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkk')

            order = client.order.create(data=order_params)

            return Response(order, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#<----------------------------------------------------Payment-Gateway-End---------------------------------------------------------------->
