from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta :
        model =CustomUser
        fields = ['id','first_name','phone','email', 'is_staff', 'is_active']
        
    
    
    
    
class CustomUserCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta :
        model =CustomUser
        fields = ['id','first_name','phone','email','password']
        
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            phone=validated_data['phone'],
            # is_staff=validated_data['is_staff'],
            # is_active=validated_data['is_active'],
            # created_by = validated_data['created_by']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
       
            
        
    
    def update(self, instance, validated_data):
        instance.first_name= validated_data.get('first_name', instance.first_name)
        instance.phone= validated_data.get('phone', instance.phone)
        instance.is_staff= validated_data.get('is_staff', instance.is_staff)
        instance.is_active= validated_data.get('is_active', instance.is_active)
        instance.password = validated_data.get('password',instance.password)
        instance.set_password(instance.password)
        # instance.created_by = validated_data.get('created_by',instance.created_by)
            
        instance.save()
        return instance