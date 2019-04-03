from django.db import models

# Create your models here.
class photo(models.Model):
    im =  models.ImageField(upload_to='images/')

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
