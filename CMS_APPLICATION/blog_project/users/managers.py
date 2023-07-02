from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    """custom user model manager where email
    is a unique and work as username field """
    
    def create_user(self,email,password,**extra_fields):
        """create and save  user and password   """
        if not email:
            raise ValueError("user must have an email address")
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        """create and save Super User"""
        
        extra_fields.setdefault("is_staff" ,True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff is True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError ("superuser must have is_superuser is True")
        return self.create_user(email,password,**extra_fields)