from django.db import models

import json

# Create your models here.
class Tags(models.Model):
    tags = models.CharField(max_length=30, primary_key = True)
    link = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.tags

class Blogs(models.Model):

    title = models.TextField()
    link = models.TextField(primary_key = True)
    writer = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    read_time = models.CharField(max_length=80)
    num_responses = models.CharField(max_length = 1000)
    num_claps = models.CharField(max_length = 1000)
    tags = models.CharField(max_length=1000)
    
    def set_tags(self, x):
        self.tags = json.dumps(x)

    def __str__(self):
        return self.title


class Responses(models.Model):

    class Meta:
        unique_together = (('blog', 'responder', 'comment'),)

    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    responder = models.TextField()
    comment = models.TextField()

    def __str__(self):
        return self.responder

