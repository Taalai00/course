from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(14),
                                                       MaxValueValidator(70)],
                                           null=True,blank=True)
    ROLE_CHOICES = (
        ('student', 'student'),
        ('teacher', 'teacher'),
    )
    user_role = models.CharField(max_length=64, choices=ROLE_CHOICES)
    user_image = models.ImageField(upload_to= 'profiles_img/', null=True,blank=True)
    bio = models. TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.first_name}- {self.last_name}-{self.user_role}'


class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    category= models.ForeignKey(Category, on_delete= models.CASCADE, related_name='course_list')
    LEVEL_CHOICES = (
        ('начальный', 'начальный'),
        ('средний', 'средний'),
        ('продвинутый', 'продвинутый'),
    )
    level= models.CharField(max_length= 64, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_bu = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
            return f'{self.course_name}'


class Lesson(models.Model):
        title = models.CharField(max_length=200)
        video_url = models.FileField(upload_to='lesson_video')
        content = models.TextField()
        course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')

        def __str__(self):
            return self.title

class Assignment(models.Model):
        title = models.CharField(max_length=100)
        description = models.TextField()
        due_date = models.DateField()
        course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment')
        students = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

        def __str__(self):
            return self.title


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    DIFFICULTY_LEVEL_CHOICES = (
        ('легкий', 'легкий'),
        ('средний', 'средний'),
        ('трудный','трудный'),
    )
    difficulty_level = models.CharField(max_length=200, choices= DIFFICULTY_LEVEL_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question_text


class Exam(models.Model):
        title = models. CharField(max_length=200)
        course = models.ForeignKey(Course, on_delete= models.CASCADE, related_name='exam')
        question = models.ForeignKey(Question, on_delete= models.CASCADE)
        passing_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
        duration = models.DurationField(40)


class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE, related_name='certificate')
    issued_id = models. CharField(max_length=50)
    certificate_url = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.student}-{self.course}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    course = models. ForeignKey(Course, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user}-{self.rating}'

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.course} -- {self.quantity}'

    def get_total_price(self):
        return self.course.price * self.quantity