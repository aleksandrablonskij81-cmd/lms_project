from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import Group
from users.models import CustomUser
from lms.models import Course, Lesson, Subscription


class CourseAPITest(TestCase):
    """Тесты для курсов"""

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='test12345'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com',
            password='test12345'
        )
        self.moderator = CustomUser.objects.create_user(
            email='moderator@example.com',
            password='test12345'
        )
        self.mod_group, _ = Group.objects.get_or_create(name='Модератор')
        self.moderator.groups.add(self.mod_group)

    def test_anonymous_get_401(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/courses/', {
            'title': 'Test Course',
            'description': 'Test description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_list_courses_only_own(self):
        Course.objects.create(title='My Course', description='Desc', owner=self.user)
        Course.objects.create(title='Other Course', description='Desc', owner=self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'My Course')

    def test_update_course_owner(self):
        course = Course.objects.create(
            title='Old',
            description='Desc',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/courses/{course.id}/', {
            'title': 'New',
            'description': 'New desc'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_other_user_404(self):
        course = Course.objects.create(
            title='Old',
            description='Desc',
            owner=self.user
        )
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(f'/api/courses/{course.id}/', {
            'title': 'Hacked',
            'description': 'Hacked'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_course_owner(self):
        course = Course.objects.create(
            title='To Delete',
            description='Desc',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_moderator_403(self):
        course = Course.objects.create(
            title='To Delete',
            description='Desc',
            owner=self.user
        )
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_sees_all_courses(self):
        Course.objects.create(title='My Course', description='Desc', owner=self.user)
        Course.objects.create(title='Other Course', description='Desc', owner=self.other_user)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_moderator_cannot_create_course(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post('/api/courses/', {
            'title': 'Moderator Course',
            'description': 'Not allowed'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonAPITest(TestCase):
    """Тесты для уроков"""

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='test12345'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com',
            password='test12345'
        )
        self.course = Course.objects.create(
            title='Test',
            description='Desc',
            owner=self.user
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', {
            'course': self.course.id,
            'title': 'Lesson 1',
            'description': 'Desc',
            'video_url': 'https://youtube.com/watch?v=test'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_create_lesson_forbidden_url(self):
        """Ссылка на сторонний ресурс — ошибка"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', {
            'course': self.course.id,
            'title': 'Lesson 1',
            'description': 'Desc',
            'video_url': 'https://evil.com/video'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson_owner(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='Old',
            description='Desc',
            video_url='https://youtube.com/watch?v=old',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/lessons/{lesson.id}/', {
            'course': self.course.id,
            'title': 'New',
            'description': 'New desc',
            'video_url': 'https://youtube.com/watch?v=new'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_other_user_404(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='Old',
            description='Desc',
            video_url='https://youtube.com/watch?v=old',
            owner=self.user
        )
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(f'/api/lessons/{lesson.id}/', {
            'course': self.course.id,
            'title': 'Hacked',
            'description': 'Hacked',
            'video_url': 'https://youtube.com/watch?v=hacked'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_lesson_owner(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='To Delete',
            description='Desc',
            video_url='https://youtube.com/watch?v=test',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_lessons_only_own(self):
        Lesson.objects.create(
            course=self.course,
            title='Lesson',
            description='Desc',
            video_url='https://youtube.com/watch?v=test',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class SubscriptionAPITest(TestCase):
    """Тесты для подписок"""

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='sub@example.com',
            password='test12345'
        )
        self.course = Course.objects.create(
            title='Test',
            description='Desc',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_anonymous_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)