from django.db import models
from django.contrib.auth.models import User



STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post_Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=False,default=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    img=models.ImageField(upload_to='images/',blank = True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.title
    def total_likes(self):
        return self.likes.count()

class Comment_Section(models.Model):
    post = models.ForeignKey(Post_Blog,on_delete= models.CASCADE)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)