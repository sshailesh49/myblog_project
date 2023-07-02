from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Blog, LikeBlog
from .serializers import BlogSerializer,LikeSerializer,GetBlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from django.db.models import Q
from .permission import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class BlogAPI(APIView):
    '''
     This API created for CRUD opration Blog models .
     
    '''
    
    authentication_classes =[BasicAuthentication]
    permission_classes =[IsAuthenticated]
    
    # List Blog
    def get(self, request, pk=None, format=None):
        '''
        Any user can access public and active blogs only.
        Owner user  access  all Blog which are created_by Self and Other user's public and active blogs only.
        
         
        Retrieval of both blog and its likes count.
        each block contain its like count value(use GetBlogSerializer )
 
        '''
        id = pk
        #import pdb;pdb.set_trace()
        try:
            if id is not None:
                one_blog = Blog.objects.get(Q(created_by=request.user,id=id)|Q(id=id,is_private=False,is_active=True))
                if one_blog:
                    serializer = GetBlogSerializer(one_blog)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    error_message = {"Error":"Blogs are not exists"}
                    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
                   
            
            all_blog = Blog.objects.filter(Q(created_by=request.user)|Q(is_private=False,is_active=True))
            if all_blog.exists():
                serializer = GetBlogSerializer(all_blog, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                error_message = {"Error":"Blogs are not exists"}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = {"Error": "Internal server error"}
            return Response(
                error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    # Create Blog
    
    def post(self,request):
        """
        Create Blog by User
        """
       # import pdb;pdb.set_trace()
        try:
            serializer=BlogSerializer(context = {"request": request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg={"message":"Blog successfull created"}
                return Response(msg,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            error_message={"message":e}
            print("----------",e)
            return Response(error_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
     # update blog 
    def put (self,request,pk):
        """ 
         update post By only owner[created_by]
        """
        id=pk
        try:
            obj=Blog.objects.get(id=id, created_by=request.user)
            serializer=BlogSerializer(obj,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                msg={"message":"Blog updated"}
                return Response(msg,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error_message={"message":e}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    # Delete Blog 
    def delete(self, request, pk):
            """ 
            A superuser can delete any Blog 
            but Owner (created_by) can delete self created blog.
            """
        
            id = pk
            try:
                if request.user.is_superuser:
                    obj = Blog.objects.get(id=id)
                else:
                    obj = Blog.objects.get(
                        id=id, created_by=request.user, is_active=True)
                obj.delete()
                return Response({'msg': 'Blog Deleted'}, status=status.HTTP_200_OK)
            except Exception as e:
                erre_msg = {"error": "You are not authorized"}
                return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)

        
  
  ###      _____________________________ LIKES API View __________________________-
  
  
class LikeAPI(APIView):
    """ 
    only Owner can access his like list,
    we use in custom permission and Is IsAuthenticated all methods 
    
    """
    
    authentication_classes =[BasicAuthentication]
    permission_classes =[IsAuthenticated,IsOwnerOrReadOnly]
    
    # List Like 
    def get(self,request,pk=None):
        try:
            all_like=LikeBlog.objects.filter(created_by=request.user)
            if all_like.exists():
                serializer =LikeSerializer(all_like,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                error_msg = {"error":"Your post don't have likes"}
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_msg = {"error":e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
     # create like   
    def post(self,request):
        
        """ 
        only access Authenticated user
        and send request veiw  to serilizer with the help of context
        context = {"request": request}
        
        """
        try:
            # import pdb;pdb.set_trace()
            serializer= LikeSerializer(context = {"request": request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg={'message':"Like created"}
                return Response(msg,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_msg= {"error":"Unique constraint failed"}
            return Response(error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
     
     # Update likes   
    def put(self,request,pk):
        """ 
        like can update only owner(created_by)
        and change state True/False
        """
        try:
            id=pk
            obj=LikeBlog.objects.get(id=id,created_by=request.user)
            if obj :
                serializer= LikeSerializer(obj,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    msg={'message':"Like Updated"}
                    return Response(msg,status=status.HTTP_201_CREATED)
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            else:
                msg={"message":"Like ID not exists"}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_msg = {"error":"Not autorized User"}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
        
    # Delete Like    
    def delete(self,request,pk):
        """ Delete likes only Blog Owner (created_by )"""
        try:
            id=pk
            obj=LikeBlog.objects.get(id=id,blog__created_by=request.user)
            obj.delete()
            msg={'message':"Like deleted"}
            return Response(msg,status=status.HTTP_201_CREATED)
        except Exception as e:
            error_msg = {"error":"Not autorized User"}
            return Response(error_msg , status=status.HTTP_400_BAD_REQUEST)
        
            
        
                
        
                
            
            
        
            
        