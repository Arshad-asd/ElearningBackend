from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
#<-----------------------------------------------------Bascis credentials account manage-- Start ------------------------------------------------->                                  

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = Role.ADMIN
        user.save(using=self._db)
        return user

class Role(models.TextChoices):
    STUDENT = 'student', 'Student'
    TUTOR = 'tutor', 'Tutor'
    ADMIN = 'admin', 'Admin'

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)  # Add the phone number field here
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    display_pic = models.ImageField(upload_to='user/', null=True, blank=True, default='user/user.png')
    subscription_plan = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    # Additional fields
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    skills = models.CharField(max_length=200, null=True, blank=True)
    subjects = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey('course.Category', on_delete=models.SET_NULL, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


#<-----------------------------------------------------Bascis credentials account manage-- End ------------------------------------------------->                                  



