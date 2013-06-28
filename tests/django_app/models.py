from .settings import *  # noqa

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    rating = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(User)


class Comment(models.Model):
    body = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)


# lint_ignore=C0110
