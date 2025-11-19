from django.db import models

# Create your models here.
class students(models.Model):
    Name = models.CharField(max_length = 100)
    Age = models.IntegerField()
    Email = models.EmailField(unique = True)

class users(models.Model):
    username = models.CharField(max_length = 100,unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 100)