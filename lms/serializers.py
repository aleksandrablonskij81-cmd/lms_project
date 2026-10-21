from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока с валидацией ссылки на YouTube"""

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'preview', 'video_url', 'owner']
        read_only_fields = ['owner']
        extra_kwargs = {
            'video_url': {'validators': [validate_youtube_url]},
        }


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с количеством уроков, вложенными уроками и признаком подписки"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'lessons_count',
            'lessons',
            'owner',
            'is_subscribed',
        ]
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False