from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator 

# Create your models here.
class Tags(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = models.CharField(max_length=30)
    link = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.tags

# class Blogs(models.Model):
#     link = models.(Handlers, on_delete=models.CASCADE)
#     id_str = models.CharField(max_length=250)
#     name = models.CharField(max_length=250)
#     url_img = models.CharField(max_length=1000)
#     description = models.CharField(max_length=250)
#     num_followers = models.PositiveIntegerField(validators = [MaxValueValidator(9999999999)])
    
#     def __str__(self):
#         return self.name