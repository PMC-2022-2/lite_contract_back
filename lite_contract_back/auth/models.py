from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
# get the user models
User = get_user_model()
# Create your models here.

# Create Custom User models
class CustomUserManager(BaseUserManager):
    '''
    The custom user manager will have
    first_name
    last_name
    email
    password
    '''
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        validate_email(email)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    class User(AbstractBaseUser, PermissionsMixin):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        email = models.EmailField(max_length=50, unique=True)
        date_joined = models.DateTimeField(auto_now_add=True)
        last_login = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)
        is_admin = models.BooleanField(default=False)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['first_name', 'last_name']

        objects = CustomUserManager()

        def __str__(self):
            return self.email

        def get_username(self):
            return self.email

        def has_perm(self, perm, obj=None):
            return self.is_admin

        def has_module_perms(self, app_label):
            return True
# Create text choices for the user's Plan Type
class plan_type(models.TextChoices):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    ENTERPRISE = 'Enterprise'

# Create text choices for the user's PaymentPlan
class payment_plan(models.TextChoices):
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'



# Create PaymentPlan model
class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=50, choices=plan_type.choices, default=plan_type.BASIC)
    payment_plan = models.CharField(max_length=50, choices=payment_plan.choices, default=payment_plan.MONTHLY)



