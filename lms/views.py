from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrModerator]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']

    def perform_create(self, serializer):
        """Автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Проверка: только владелец или модератор"""
        obj = self.get_object()
        print(f"🔍 perform_update: obj.owner={obj.owner}, request.user={self.request.user}")
        if obj.owner != self.request.user and not self.request.user.groups.filter(name='Модератор').exists():
            raise PermissionDenied('Вы не можете редактировать чужой курс.')
        serializer.save()

    def perform_destroy(self, instance):
        """Проверка: только владелец или модератор"""
        print(f"🔍 perform_destroy: obj.owner={instance.owner}, request.user={self.request.user}")
        if instance.owner != self.request.user and not self.request.user.groups.filter(name='Модератор').exists():
            raise PermissionDenied('Вы не можете удалить чужой курс.')
        instance.delete()


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title']
    ordering = ['title']

    def perform_create(self, serializer):
        """Автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Проверка: только владелец или модератор"""
        obj = self.get_object()
        print(f"🔍 perform_update (lesson): obj.owner={obj.owner}, request.user={self.request.user}")
        if obj.owner != self.request.user and not self.request.user.groups.filter(name='Модератор').exists():
            raise PermissionDenied('Вы не можете редактировать чужой урок.')
        serializer.save()

    def perform_destroy(self, instance):
        """Проверка: только владелец или модератор"""
        print(f"🔍 perform_destroy (lesson): obj.owner={instance.owner}, request.user={self.request.user}")
        if instance.owner != self.request.user and not self.request.user.groups.filter(name='Модератор').exists():
            raise PermissionDenied('Вы не можете удалить чужой урок.')
        instance.delete()