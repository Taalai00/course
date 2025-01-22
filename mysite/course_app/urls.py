from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('', CourseListAPIView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
    path('course_list/', CourseListOwnerAPIView.as_view(), name ='course_list_owner'),
    path('course_list/<int:pk>/', CourseDetailUpdateDeleteOwnerAPIView.as_view(), name='edit'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course_create'),

    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    path('review/', CourseReviewAPIView.as_view(), name='review_create'),

    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson_list/', LessonListOwnerAPIView.as_view(), name='lesson_list_owner'),
    path('lesson_list/<int:pk>/', LessonDetailUpdateDestroyOwnerAPIView.as_view(), name='lesson_edit_owner'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),

    path('assignment/', AssignmentListAPIView.as_view(), name='assignment'),
    path('assignment/create/', AssignmentCreateAPIView.as_view(), name='assignment_create'),
    path('assignment_list/', AssignmentListOwnerAPIView.as_view(), name='assignment_list'),
    path('assignment_list/<int:pk>/', AssignmentDetailUpdateDestroyOwnerAPIView.as_view(), name='assignment_list_edit'),

    path('exam/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/create/', ExamCreateAPIView.as_view(), name='exam_create'),
    path('exam_list/', ExamListOwnerAPIView.as_view(), name='exam_list'),
    path('exam_list/<int:pk>/', ExamDetailUpdateDestroyOwnerAPIView.as_view(), name='exam_list_edit'),

    path('certificates/', CertificateListAPIView.as_view(), name='certificate_list'),
    path('certificates/create/', CertificateCreateAPIView.as_view(), name='certificates_create'),

    path('question/', QuestionListAPIView.as_view(), name='question_list'),
    path('question/create/', QuestionCreateAPIView.as_view(), name='question_create'),

    path('carts/', CartListAPIView.as_view(), name='cart_list'),
    path('carts/<int:pk>/', CartItemDetailAPiView.as_view(), name='cart_item_detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]