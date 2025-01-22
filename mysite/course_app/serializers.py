from .models import UserProfile, Category, Course, Lesson, Assignment, Question, Exam, Certificate, Review, Cart, CartItem
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_role']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'content']

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', ]

class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'difficulty_level', 'created_date']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['title', 'passing_score', 'duration']

class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['issued_id', 'certificate_url']

class CertificateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class CourseReviewSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Review
        fields = ['user', 'course', 'rating', 'comment']

class CourseReviewSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()

    class Meta:
        model = Review
        fields = '__all__'

class CartListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'created_date']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description', 'level', 'category']


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer()
    created_bu = UserProfileSimpleSerializer()
    lesson = LessonSerializer(many=True, read_only=True)
    assignment = AssignmentSerializer(many=True, read_only=True)
    question = QuestionSerializer(many=True, read_only=True)
    exam = ExamSerializer(many=True, read_only=True)
    certificate = CertificateSerializer(many=True, read_only=True)
    review = CourseReviewSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'level', 'category', 'price',
                  'created_bu', 'created_at', 'updated_at', 'lesson', 'assignment', 'question', 'exam', 'certificate', 'review']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    course_list = CourseListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name', 'course_list']

class CartItemSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    cart = CartListSerializer(read_only=True)
    get_total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['cart', 'course', 'quantity', 'get_total_price']

    def get_total_price(self,obj):
        return obj.get_total_price()