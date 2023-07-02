from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserCreateUpdateSerializer
from rest_framework import status



"""  
Create a Custom Django User Model -CustomUser


"""

class UserAPI(APIView):
    """ User CRUD  API 
    
     Create user with post method  without any authenticate.
     All Data Get Only Admin and Single Data get admin and self User.
     All records update only Admin and  Self User update only own record.
     -Partial records Update only Admin and self User update only own partial records.
     Delete all user only superuser and self user  only delete himself
    
    """
    
    
    # Note - All Data Get Only Admin and Single DaTa get admin and self User
    def get(self, request, pk=None, format=None):
        try:
            id = pk
            if id is not None:
                try:
                    if request.user.is_superuser:
                        single_user = CustomUser.objects.get(id=id)
                    else:
                        single_user = CustomUser.objects.get(id=id, email=request.user)
                    serializer = CustomUserSerializer(single_user)
                    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    erre_msg = {"error": "You are not authorized"}
                    return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
            if request.user.is_superuser:

                all_user = CustomUser.objects.all()
                serializer = CustomUserSerializer(all_user, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                all_user = CustomUser.objects.filter(email=request.user)
                if all_user.exists():
                    serializer = CustomUserSerializer(all_user, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    error_msg = {"error": "You are not admin"}
                    return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_msg = {"error":e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
        
     # Note- Create User Without Any authentication
    def post(self, request, format=None):
        try:
            serializer = CustomUserCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'User Created'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("----------------",e)
            error_msg = {'Detail':e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Note- All update only Admin and Self User update only own record
    def put(self, request, pk, format=None):
        #import pdb;pdb.set_trace()
        try:
            id = pk
            if request.user.is_authenticated:
                try:
                    if request.user.is_superuser:
                        obj = CustomUser.objects.get(id=id)
                    else:
                        obj = CustomUser.objects.get(
                            id=id, email=request.user, is_active=True)
                    serializer = CustomUserSerializer(obj, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg': 'User Update Successfully'}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print("-------------------",e)
                    erre_msg = {"error": "internal server error "}
                    return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                erre_msg = {"error": "Login Required"}
                return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
        
            error_msg = {'Detail':e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Note -Partial Update only Admin and self User
    def patch(self, request, pk, format=None):
        try:
            id = pk
            if request.user.is_authenticated:
                try:
                    if request.user.is_superuser:
                        obj = CustomUser.objects.get(id=id)
                    else:
                        obj = CustomUser.objects.get(
                            id=id, email=request.user, is_active=True)
                    serializer = CustomUserCreateUpdateSerializer(
                        obj, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg': 'User Update Successfully'}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_201_CREATED)

                except Exception as e:
                    erre_msg = {"error": "You are not authorized"}
                    return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                erre_msg = {"error": "Login Required"}
                return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            error_msg = {'Detail':e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
        
    # Delete all user only superuser and self user  only delete himself

    def delete(self, request, pk, format=None):
        try:
            if request.user.is_authenticated:
                id = pk
                try:
                    if request.user.is_superuser:
                        obj = CustomUser.objects.get(id=id)
                    else:
                        obj = CustomUser.objects.get(
                            id=id, email=request.user, is_active=True)
                    obj.delete()
                    return Response({'msg': 'User Deleted'}, status=status.HTTP_200_OK)
                except Exception as e:
                    erre_msg = {"error": "You are not authorized"}
                    return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)

            else:
                erre_msg = {"error": "Login Required"}
                return Response(erre_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            
            error_msg = {'Detail':e}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

