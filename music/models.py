from django.contrib.auth.models import Permission, User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, default=1)
    author = models.CharField(max_length=250)
    post_title = models.CharField(max_length=500)
    description = models.TextField()
    post_logo = models.FileField()

    def __str__(self):
        return self.post_title + ' - ' + self.author
