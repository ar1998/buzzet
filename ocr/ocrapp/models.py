from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class photo(models.Model):
    im =  models.ImageField(upload_to='images/')
    #im_username=models.CharField(max_length=100)
class aadhar_verification_model(models.Model):
    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=50,unique=True)
    dob = models.CharField(max_length=50)
    #address = models.CharField(max_length=100)

class aadhar_registration_model(models.Model):
    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=50,unique=True)
    dob = models.CharField(max_length=50)
    #address = models.CharField(max_length=100)

class pan_verification_model(models.Model):
    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=50,unique=True)
    dob = models.CharField(max_length=50)
    #address = models.CharField(max_length=100)

class pan_registration_model(models.Model):
    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=50,unique=True)
    dob = models.CharField(max_length=50)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class feedback(models.Model):
    feedback_name = models.CharField(max_length = 50)
    feedback_comment = models.CharField(max_length = 100)

class community(models.Model):
    name = models.CharField(max_length = 50)
    tag = models.CharField(max_length=50)
    amount = models.IntegerField(default = 10000)
    purpose = models.CharField(max_length=100)
    descr = models.CharField(max_length=2000)
    exp_profit = models.IntegerField(default = 1)
    rating = models.FloatField(null=True, blank=True, default=2)

class sub(models.Model):
    name = models.CharField(max_length=50)
    sub_status = models.IntegerField(default = 0)