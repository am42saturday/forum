from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as BaseUser


class User(BaseUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = models.EmailField(blank=False)
        avatar = models.ImageField(upload_to='user avatar')
        rating = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Topic(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    last_activity_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='Topic.topic_user_likes+') # array of Users who liked topic
    user_dislikes = models.ManyToManyField(User, related_name='Topic.topic_user_dislikes+')  # array of Users who disliked topic

    def __str__(self):
        return self.title


class Comment(models.Model):
    is_active = models.BooleanField(default=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='Topic.comment_user_likes+')  # array of Users who liked topic
    user_dislikes = models.ManyToManyField(User, related_name='Topic.comment_user_dislikes+')  # array of Users who disliked topic

    def __str__(self):
        return self.text
