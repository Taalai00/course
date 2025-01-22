from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserProfileSerializer, CategoryListSerializer, CourseListSerializer, CartListSerializer,
                          CartItemSerializer, LessonSerializer, AssignmentSerializer, QuestionSerializer,
                          ExamSerializer, CertificateSerializer, CourseReviewSerializer, CategoryDetailSerializer,
                          CourseDetailSerializer, CourseSerializer, LessonCreateSerializer, AssignmentCreateSerializer,
                          ExamCreateSerializer, CertificateCreateSerializer, QuestionCreateSerializer, LoginSerializer, UserSerializer)
from .models import UserProfile, Category, Course, Lesson, Assignment, Question, Exam, Certificate, Review, CartItem, Cart
from rest_framework import viewsets, generics, status
from .permissions import CheckOwner, CheckUserReview, CheckCourseOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        try :
            serializer.is_valid(raise_exeption = True)
        except Exception:
            return Response({'detail': 'неверные учетные данные:'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['store_name']
    filterset_class = CourseFilter
    ordering_fields = ['price']

class CourseListOwnerAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(created_bu=self.request.user)

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CheckOwner]

class CourseDetailUpdateDeleteOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CheckOwner, CheckCourseOwner]

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListOwnerAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [CheckOwner]

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [CheckOwner]

class LessonDetailUpdateDestroyOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    permission_classes = [CheckOwner, CheckCourseOwner]

class AssignmentListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentListOwnerAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    permission_classes = [CheckOwner]

class AssignmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [CheckOwner]

class AssignmentDetailUpdateDestroyOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentCreateSerializer
    permission_classes = [CheckOwner, CheckCourseOwner]

class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = [CheckOwner]

class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamListOwnerAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    permission_classes = [CheckOwner]


class ExamCreateAPIView(generics.CreateAPIView):
    serializer_class = ExamCreateSerializer
    permission_classes = [CheckOwner]


class ExamDetailUpdateDestroyOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamCreateSerializer
    permission_classes = [CheckOwner, CheckCourseOwner]

class CertificateListAPIView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class CertificateCreateAPIView(generics.CreateAPIView):
    serializer_class = CertificateCreateSerializer
    permission_classes = [CheckOwner]

class CourseReviewAPIView(generics.CreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [CheckUserReview]

class CartListAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Cart.objects.filter(id=self.request.user.id)

class CartItemDetailAPiView(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



