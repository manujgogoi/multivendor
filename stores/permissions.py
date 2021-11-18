from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Only Admin (is_staff=True) users have write access
    Others can `list` and `view`
    '''

    message = 'Adding or updating is not allowed.'

    def has_permission(self, request, view):    
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False

class ImagePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        vendor = request.user.vendor if hasattr(request.user, 'vendor') else None 
        if vendor is not None:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True    

        if request.user.is_staff or request.user.is_superuser:
            return True 
        
        return False

    def has_object_permission(self, request, view, obj):
        vendor = request.user.vendor if hasattr(request.user, 'vendor') else None

        if request.method in permissions.SAFE_METHODS:
            return True 

        if request.user.is_staff or request.user.is_superuser:
            return True 

        if vendor is not None:
            if obj.product.vendor == vendor:
                return True
                
        return False

class SpecificationPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        vendor = request.user.vendor if hasattr(request.user, 'vendor') else None 
        if vendor is not None:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True    

        if request.user.is_staff or request.user.is_superuser:
            return True 
        
        return False

    def has_object_permission(self, request, view, obj):
        vendor = request.user.vendor if hasattr(request.user, 'vendor') else None

        if request.method in permissions.SAFE_METHODS:
            return True 

        if request.user.is_staff or request.user.is_superuser:
            return True 

        if vendor is not None:
            if obj.product.vendor == vendor:
                return True
                
        return False