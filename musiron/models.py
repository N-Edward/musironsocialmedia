from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

# Create your models here.

#profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField( upload_to="profile/" )
    nickname = models.CharField(blank=True,max_length=255)
    location = models.CharField(blank=True,max_length=255)
    
    def __str__(self):
        return self.user.username
    
    #function that overrides defautlt save function
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        #compressing image size using pillow/PIL Image method
        ###
        #img = Image.open(self.image.path)
        #if img.height > 300 or img.width > 300:
        
        #    output_size = (300,300)
         #   img.thumbnail(output_size)
         #   img.save(self.image.path)
        ###
        #img = Image.open(self.image.path)
        #width, height = img.size
        #TARGET_WIDTH = 500
        #coefficient = width/500
        #new_height = height/ coefficient
        #img = img.resize((int(TARGET_WIDTH), int(new_height)),Image.ANTIALIAS)
        #img.save(self.image.path, quality = 50)
        ###
        


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    
    def __str__(self):
        return self.title
    
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    rate_choices = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    rate = models.IntegerField(choices=rate_choices)
    comment = models.TextField(max_length=400, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.post.title
    