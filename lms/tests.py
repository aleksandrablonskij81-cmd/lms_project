from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from lms.models import Course, Lesson


class CourseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='test12345'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        response = self.client.post('/api/courses/', {
            'title': 'Test Course',
            'description': 'Test description'
        })
        self.assertEqual(response.status_code, 201)

    def test_list_courses(self):
        Course.objects.create(title='Course 1', description='Desc')
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        course = Course.objects.create(title='Old', description='Desc')
        response = self.client.put(f'/api/courses/{course.id}/', {
            'title': 'New',
            'description': 'New desc'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_course(self):
        course = Course.objects.create(title='To Delete', description='Desc')
        response = self.client.delete(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, 204)


class LessonAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='test12345'
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test', description='Desc')

    def test_create_lesson(self):
        response = self.client.post('/api/lessons/', {
            'course': self.course.id,
            'title': 'Lesson 1',
            'description': 'Desc',
            'video_url': 'https://youtube.com/watch?v=test'
        })
        self.assertEqual(response.status_code, 201)

    def test_list_lessons(self):
        Lesson.objects.create(
            course=self.course,
            title='Lesson',
            description='Desc',
            video_url='https://youtube.com/watch?v=test'
        )
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, 200)