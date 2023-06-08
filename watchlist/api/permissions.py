from rest_framework import permissions

'''
Custom Permissions
'''


class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            '''
            if GET, then apply readonly
            if POST,UPDATE,PATCH,DELETE then check permissions & then apply
            class Permissions.
            '''
            
            return True
        else:
            return bool(request.user and request.user.is_staff)

class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request,view, obj):
        if request.method in permissions.SAFE_METHODS:
            # SAFE_METHODS = GET, Retrievals.
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff
        
            