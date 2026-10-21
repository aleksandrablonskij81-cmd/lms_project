from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import (
    IsNotModerator,
    IsOwnerAndNotModerator,
    IsOwnerOrModerator,
    is_moderator,
)
from .paginators import CoursePagination, LessonPagination


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
    """ViewSet для курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']


class LessonViewSet(OwnedModelViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']


class SubscriptionAPIView(APIView):
    """Управление подпиской на курс (POST: toggle)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message})