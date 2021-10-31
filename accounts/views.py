from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from accounts.serializers import UserSerializer
from accounts.permissions import IsStaffOrNone

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    This viewset automatically provides `list` and `retrieve` actions.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrNone,]


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
