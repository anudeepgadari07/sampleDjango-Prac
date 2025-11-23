from django.db import models
import datetime


# Create your models here.
class students(models.Model):
    Name = models.CharField(max_length = 100)
    Age = models.IntegerField()
    Email = models.EmailField(unique = True)

class users(models.Model):
    username = models.CharField(max_length = 100,unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 100)

class movieData(models.Model):
    MovieName = models.CharField(max_length = 100)
    ReleaseDate = models.DateField()
    Budget = models.CharField(max_length = 100)
    Rating = models.CharField(max_length = 100)