from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    #import pdb;pdb.set_trace()
    def has_object_permission(self, request, view, obj):
        print(obj)
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.uses