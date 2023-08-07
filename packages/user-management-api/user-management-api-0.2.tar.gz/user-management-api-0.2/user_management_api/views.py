from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from store.pagination import DefaultPagination
from .filters import UserFilter, GroupFilter
from .serializers import UserSerializer, UserCreateSerializer, PermissionSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from .serializers import GroupSerializer

User = get_user_model()



class IsAuthenticatedViewSet(viewsets.ViewSet):
    def list(self, request):
        is_authenticated = request.user.is_authenticated
        is_staff = request.user.is_staff
        return Response({
            'is_authenticated': is_authenticated,
            'is_staff': is_staff
        })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilter
    ordering_fields = ['is_active', 'is_staff']
    search_fields = ['first_name', 'last_name']


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = GroupFilter
    ordering_fields = ['name']
    search_fields = ['name']
    pagination_class = DefaultPagination


class PermissionViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = Permission.objects.prefetch_related('content_type').all()
    serializer_class = PermissionSerializer


