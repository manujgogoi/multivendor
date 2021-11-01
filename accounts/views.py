from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.serializers import UserSerializer, PasswordSerializer
from accounts.permissions import IsAdminAndSelfOrReadonly

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


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminAndSelfOrReadonly]
        return [permission() for permission in permission_classes]

