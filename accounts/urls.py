from django.urls import path
from . import views
from .views import  TutorRegistrationView, UserDetialiView, UserRegistrationView,GetRoutesView ,LogoutView,UserProfileUpdateView,UserProfileView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView,UserListView,BlockUnblockUserView,TutorListView

from course.views import BlockUnblockCourseView, BlockUnblockPlanView, CSubCategoryListView, CategoryCreateView, CategoryListAPIView, CourseCreateAPIView, CourseDetailView, CourseListAPIView, CourseListView, CourseUpdateView, FeatureCreateView, FeatureDetailView, FeatureListView, FeatureUpdateView, LessonCreateView, LessonListView, LessonUpdateView, ListLiveClassesTodayView, LiveClassListCreateView, PlanCreateView, PlanListView, RazorpayOrderView, SubCategoryEditView,SubCategoryListView, SubscriptionCreateView, SubscriptionListView, TutorCoursesListView, TutorLessonsListView, TutorLiveListView, UpdateCategoryView,BlockUnblockCategoryView,SubCategoryAddView,BlockUnblockSubCategoryView, UpdateLiveClassStatusView, UserCategoryListAPIView, UserLiveClassListView, UserSubscriptionListView 

urlpatterns = [
    path('',views.GetRoutesView.as_view(),name='getRoutes'),

    #<----------------------------------------------------Login & Refresh-for-user,admin,tutor-Side-Start-------------------------------------------------------------------------->

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    #<----------------------------------------------------Login & Refresh-for-user,admin,tutor-Side-End-------------------------------------------------------------------------->

    #<----------------------------------------------------User-Sides-Start-------------------------------------------------------------------------->
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/update-profile/', UserProfileUpdateView.as_view(), name='user-registration'),
    path('user/user-profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path('user/detail-view/<int:id>/',UserDetialiView.as_view(),name='user-detail-view'),

   
    path('user/category-list/',UserCategoryListAPIView.as_view(),name="user-category-list"),
    path('user/subcategory-list/<int:category_id>/',CSubCategoryListView.as_view(),name="user-subcategory-list"),
    path('user/course-list/', CourseListAPIView.as_view(), name='course-list'),
    path('user/course-detail/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('user/plans/',PlanListView.as_view(),name="user-plans"),
    path('user/subscription/create/', SubscriptionCreateView.as_view(), name='create-subscription'),
    path('user/create-razorpay-order/', RazorpayOrderView.as_view(), name='create_razorpay_order'),
    path('user/subscriptions/', UserSubscriptionListView.as_view(), name='subscription-list'),
    path('user/lives-list/',UserLiveClassListView.as_view(),name="user-live-list"),
    path('user/courses/<int:course_id>/lessons/', LessonListView.as_view(), name='lesson-list'),

    #<-----------------------------------------------------User-Sides-End--------------------------------------------------------------------------------------->
    
    #<-----------------------------------------------------Admin-Sides-Start---------------------------------------------------------------------------------------->
    path('admin/logout/', LogoutView.as_view(), name='logout'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/block-unblock/<int:pk>/', BlockUnblockUserView.as_view(), name='block-unblock-user'),
    path('admin/tutors/', TutorListView.as_view(), name='tutor-list'),
    path('admin/tutor/block-unblock/<int:pk>/', BlockUnblockUserView.as_view(), name='block-unblock-user'),
    path('admin/create-categories/', CategoryCreateView.as_view(), name='category_create'),
    path('admin/categories/<int:category_id>/', UpdateCategoryView.as_view(), name='update_category'),
    path('admin/categories/block-unblock/<int:pk>/',BlockUnblockCategoryView.as_view(), name='category_block_ublock'),
    path('admin/categories/', CategoryListAPIView.as_view(), name='category-list'),

    path('admin/sub-categories/',SubCategoryListView.as_view(), name="sub-categories"),
    path('admin/create/sub-categories/',SubCategoryAddView.as_view(), name="sub-categories"),
    path('admin/sub-categories/block-unblock/<int:pk>/', BlockUnblockSubCategoryView.as_view(), name="sub_categories_block_ublock"),
    path('admin/update/sub-categories/<int:subcategory_id>/',SubCategoryEditView.as_view(),name="update_sub_categories"),
    path('admin/categories/<int:category_id>/subcategories/', CSubCategoryListView.as_view(), name='subcategory-list'),

    
    path('admin/plans/', PlanListView.as_view(), name='plan-list'),
    path('admin/create/plan/', PlanCreateView.as_view(), name='plan-create'),
    path('admin/block-unblock-plan/<int:pk>/',BlockUnblockPlanView.as_view(),name="block-unblock-plan"),
    
    path('admin/features-list/',FeatureListView.as_view(),name="features-list"),
    path('admin/view-features/<int:plan_id>/', FeatureDetailView.as_view(), name='feature-detail'),
    path('admin/create-feature/', FeatureCreateView.as_view(), name='create-feature'),
    path('admin/edit-features/<int:pk>/',FeatureUpdateView.as_view(),name='edit-features'),

    path('admin/course-list/',CourseListView.as_view(),name='course-list'),
    path('admin/course-create/', CourseCreateAPIView.as_view(), name='course-create'),

    path('admin/block-unblock-course/<int:pk>/',BlockUnblockCourseView.as_view(),name="block-unblock-course"),

    path('admin/subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),

    #<----------------------------------------------------Admin-Sides-End---------------------------------------------------------------------------------------------->
    
    #<----------------------------------------------------Tutor-Sides-Start---------------------------------------------------------------------------------------------->
    path('tutor/register/', TutorRegistrationView.as_view(), name='tutor_register'),
    path('tutor/update-profile/', UserProfileUpdateView.as_view(), name="update-user"),
    path('tutor/user-profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path('tutor/courses/', TutorCoursesListView.as_view(), name='tutor-courses-list'),
    path('tutor/edit-course/<int:course_id>/', CourseUpdateView.as_view(), name='course-update'),
    path('tutor/categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('tutor/create-live/',LiveClassListCreateView.as_view(),name='tutor-create-live'),
    path('tutor/lives-list/', TutorLiveListView.as_view(), name='tutor-live-list'),
    path('tutor/lives-shedules/', ListLiveClassesTodayView.as_view(), name='live-classes-today'),
    path('tutor/create-lessons/',LessonCreateView.as_view(),name="tutor-create-lesson"),
    path('tutor/lessons-list/',TutorLessonsListView.as_view(),name="tutor-lessons-list"),
    path('tutor/lessons-edit/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
    path('tutor/live-status-update/<int:pk>/', UpdateLiveClassStatusView.as_view(), name="live-status-update"),
    #<----------------------------------------------------Tutor-Sides-End---------------------------------------------------------------------------------------------->

]
