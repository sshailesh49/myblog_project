from django.db import models
from users.models import CustomUser

# Create your models here.

class Blog(models.Model):
    """create blog model """
    
    title=models.CharField(max_length=100)
    description = models.TextField()
    content = models.CharField(max_length=150,blank=True,default="")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blogs')
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
         return self.title
    
    class Meta:
        ordering =['created_date']
        
        
        
class LikeBlog(models.Model):
    """create like models"""
    like = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="likes")
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="b_likes")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
         return str(self.like)
    
    class Meta:
        ordering=["created_date"]
        unique_together = ('blog', 'created_by',)
        
    
