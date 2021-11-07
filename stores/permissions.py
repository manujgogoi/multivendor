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


class IsVendorOrReadOnly(permissions.BasePermission):
    '''
    This is a custom permission testing class for vendor
    '''

    message = 'You are not a vendor.'

    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     elif request.vendor