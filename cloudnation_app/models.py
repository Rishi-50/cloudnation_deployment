from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email).lower()
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**extra_fields):
        user = self.create_user(email,password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True,null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }


class githubdetails(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    organization = models.CharField(max_length=255,blank=False,null=False)
    repo = models.CharField(max_length=255,blank=False,null=False)
    branch = models.CharField(max_length=255,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class appdetails(models.Model):
    REGIONS = [
        ('United States - Michigan', 'United States - Michigan'),
        ('India - Mumbai', 'India - Mumbai')
    ]

    FRAMEWORKS = [
        ('Vue.js', 'Vue.js'),
        ('React', 'React'),
        ('Express.js', 'Express.js'),
        ('Ruby on Rails', 'Ruby on Rails')
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=False,null=False)
    region = models.CharField(max_length=255,choices=REGIONS)
    framework = models.CharField(max_length=255,choices=FRAMEWORKS)


class appplans(models.Model):
    PLAN_TYPES = [
        ('Starter, 10 GB, 512 MB, 2, $0.0278, $20' , 'Starter, 10 GB, 512 MB, 2, $0.0278, $20'),
        ('Basic, 10 GB, 1 GB, 2, $0.0417, $30' , 'Basic, 10 GB, 1 GB, 2, $0.0417, $30'),
        ('Standard, 10 GB, 2 GB, 2, $0.0625, $45' , 'Standard, 10 GB, 2 GB, 2, $0.0625, $45'),
        ('Performance, 10 GB, 4 GB, 2, $0.0972, $70' , 'Performance, 10 GB, 4 GB, 2, $0.0972, $70'),
        ('Pro, 10 GB,8 GB, 2, $0.1597, $115' , 'Pro, 10 GB,8 GB, 2, $0.1597, $115')
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=255 , choices=PLAN_TYPES)


class databasedetails(models.Model):
    DB_TYPE = [
        ('Postgresql' , 'Postgresql'),
        ('Mysql' , 'Mysql')
    ]
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    db_type = models.CharField(max_length=255, choices=DB_TYPE)

    def __str__(self) -> str:
        return self.db_type
    

class dbplans(models.Model):
    PLAN_TYPES = [
        ('Starter, 10 GB, 512 MB, 2, $0.0278, $20' , 'Starter, 10 GB, 512 MB, 2, $0.0278, $20'),
        ('Basic, 10 GB, 1 GB, 2, $0.0417, $30' , 'Basic, 10 GB, 1 GB, 2, $0.0417, $30'),
        ('Standard, 10 GB, 2 GB, 2, $0.0625, $45' , 'Standard, 10 GB, 2 GB, 2, $0.0625, $45'),
        ('Performance, 10 GB, 4 GB, 2, $0.0972, $70' , 'Performance, 10 GB, 4 GB, 2, $0.0972, $70'),
        ('Pro, 10 GB,8 GB, 2, $0.1597, $115' , 'Pro, 10 GB,8 GB, 2, $0.1597, $115')
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=255 , choices=PLAN_TYPES)


class envvariables(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    key = models.CharField(max_length=255,blank=False,null=False)
    value = models.CharField(max_length=255,blank=False,null=False)