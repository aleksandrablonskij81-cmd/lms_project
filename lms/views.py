from rest_framework import viewsets
from rest_framework import generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# ===== КУРС: ViewSet (полный CRUD) =====
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# ===== УРОК: Generic-классы =====
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer