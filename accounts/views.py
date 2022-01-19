from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.serializers import EmailSerializer, UserSerializer, PasswordSerializer
from accounts.permissions import IsAdminOrSelf

from vendor.serializers import VendorSerializer;
from vendor.models import Vendor;

User = get_user_model()

class UserViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`, 
    and `destroy`  actions.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # viewset custom action to change password
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        '''
        Change Password view
        '''
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': ['Wrong Password.']},
                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def change_email(self, request, pk=None):
        '''
        Change Email id
        '''
        user = self.get_object()
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            user.email = serializer.validated_data['email']
            user.save()
            return Response({'message': 'email changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['GET'])
    def get_own_vendor(self, request, pk=None):
        '''
        Get own vendor detail (if exist)
        '''
        user = self.get_object()
        queryset = Vendor.objects.get(owner=user);
        print(queryset)
        serializer = VendorSerializer(queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({"error": ["User has no vendor"]}, status=status.HTTP_400_BAD_REQUEST)
        

            

    @action(detail=False, methods=['POST'])
    def email_exists(self, request, *args, **kwargs):
        '''
        Check Email id exists or not.
        This action returns true if email not exist.
        '''
        serializer = EmailSerializer(data=request.data)

        # If email already exists then is_valid() raises Error
        # We return True if is_valid() raises an error 
        if serializer.is_valid():
            return Response(False)
        return Response(True)


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]

