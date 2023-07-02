from rest_framework import serializers
from .models import Blog,LikeBlog
from users.models import CustomUser

class BlogSerializer(serializers.ModelSerializer):
    """  Its Use in  only Create Update And Delete  request
    """
    
    created_by = serializers.ReadOnlyField(source='created_by.email')
    
    class Meta:
        model = Blog
        fields = ['id', 'title','description','content' ,'is_active', 'created_by','is_private']
        
    def create(self, validated_data):
   
        blog=Blog.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            content=validated_data['content'],
            created_by=self.context['request'].user
            )
        return blog
    
    
class GetBlogSerializer(serializers.ModelSerializer):
    """ 
    Its use only for  blogs list and blog details
    """
    created_by = serializers.ReadOnlyField(source='created_by.email')
    count_like = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title','description','content' ,'is_active', 'created_by','is_private','count_like']
        
    def get_count_like(self, obj):
        return obj.b_likes.filter(like=True).count()
        
    

# __________-Like Serializer__________________

class LikeSerializer(serializers.ModelSerializer):
    
    """ its for like model 
    """
    
    
    created_by = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = LikeBlog
        fields = '__all__'
        
    def create(self, validated_data):
        likeblog=LikeBlog.objects.create(
            like=validated_data['like'],
            blog=validated_data['blog'],
            created_by=self.context['request'].user
            )
        return likeblog
        

