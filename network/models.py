from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.humanize.templatetags import humanize


class User(AbstractUser):
    pass
    joined_date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to='images/')

    #def serialize(self):
       #return {
           # "id": self.id,
          #  "user": self.user,
            #"name": self.name,
            #"about": self.about,
            #"country": self.country,
           # "photo": self.photo,
        #}
    def __str__(self):
        return f"Profile of: {self.name} with username: {self.user} about: {self.about} of country: {self.country}"
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "posts")
    body = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes")

    class Meta:
        ordering = ['-timestamp']

    def post_time(self):
        return humanize.naturaltime(self.timestamp)

    #def serialize(self):
        #return {
            #"id": self.id,
            #"author": self.author,
            #"body": self.body,
            #"likes": [user.username for user in self.likes.all()],
           # "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        
        #}

    def __str__(self):
        return f"Posted by: {self.author} with post: {self.body} On: {self.timestamp} with: {self.likes.count()} likes"

    

class Relationship(models.Model):
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    follow_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow_by")

    def __str__(self):
        return f"{self.follow_by} follows: {self.follows}"

    def is_valid_friend(self):
        return self.follows != self.follow_by

    def is_not_valid_friend(self):
        return self.follows == self.follows or self.follow_by == self.follow_by
    