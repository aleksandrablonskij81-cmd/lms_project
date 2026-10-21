from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import (
    IsNotModerator,
    IsOwnerAndNotModerator,
    IsOwnerOrModerator,
    is_moderator,
)


class OwnedModelViewSetMixin:
    """Миксин: фильтрация по owner и права по action."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_moderator(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        permissions_by_action = {
            "create": [IsAuthenticated, IsNotModerator],
            "list": [IsAuthenticated],
            "retrieve": [IsAuthenticated, IsOwnerOrModerator],
            "update": [IsAuthenticated, IsOwnerOrModerator],
            "partial_update": [IsAuthenticated, IsOwnerOrModerator],
            "destroy": [IsAuthenticated, IsOwnerAndNotModerator],
        }
        permission_classes = permissions_by_action.get(
            self.action,
            [IsAuthenticated],
        )
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(OwnedModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']


class LessonViewSet(OwnedModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']