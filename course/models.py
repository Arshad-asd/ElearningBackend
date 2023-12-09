from datetime import timedelta
from django.db import models
from django.utils import timezone

from accounts.models import UserAccount


#<-----------------------------------------------------Course manage-- Start ------------------------------------------------->                                  


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribed_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='category_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=255, unique=True)
    category_ref = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_category_name

class Course(models.Model):
    category_ref = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category_ref = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    tutor_ref = models.ForeignKey(UserAccount, on_delete=models.CASCADE) 
    course_name = models.CharField(max_length=255)
    preview_video = models.FileField(upload_to='course_previews/',default='path/to/dummy/video.mp4' )
    banner_image = models.ImageField(upload_to='course_banners/', default='path/to/default/banner.jpg')

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255)
    lesson_video = models.FileField(upload_to='lesson_videos/')
    thumbnail_image = models.ImageField(upload_to='course_banners/', default='path/to/default/banner.jpg')
    course_ref = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor_ref = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.lesson_name


class LiveClass(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    start_time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    access_code = models.CharField(max_length=10, unique=True)
    course_ref = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor_ref = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

#<-----------------------------------------------------Course manage-- End ------------------------------------------------->                                  



#<-----------------------------------------------------Plans manage-- Start ------------------------------------------------->                                  


class PlanType(models.TextChoices):
    BASIC = 'Basic', 'Basic'
    MEDIUM = 'Medium', 'Medium'
    PREMIUM = 'Premium', 'Premium'

class Plan(models.Model):
    type = models.CharField(max_length=15, choices=PlanType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
       return self.type


class Feature(models.Model):
    entry = models.ForeignKey(Plan, related_name='features', on_delete=models.CASCADE)
    feature_text = models.CharField(max_length=200)


#<-----------------------------------------------------Plans manage-- End ------------------------------------------------->                                  


#<-----------------------------------------------------Subscriptions manage-- Start ------------------------------------------------->                                  


class Subscription(models.Model):
    user_ref = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    plan_ref = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.CharField(max_length=15)  # You might want to use choices here
    purchase_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(default=timezone.now() + timedelta(days=365))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_ref.email}'s Subscription"

    class Meta:
        ordering = ['-purchase_date']

#<-----------------------------------------------------Subscriptions manage-- End ------------------------------------------------->                                  
