import unittest

from django.test.client import Client
from django.contrib.auth.models import User
from django.core.management import call_command
from school.models import Student, ClassRoom

class TestAdmin(unittest.TestCase):
    def setUp(self):
        # create superuser
        User.objects.create_superuser(username='admin',
                                       email='admin@somewhere.com',
                                       password='1234')
        self.client = Client()
        self.client.login(username='admin', password='1234')
        
        self.class_room = ClassRoom.objects.create(year='N')
        self.student = Student.objects.create(first_name='Myfirstname',
                               middle_name='Mymiddlename',
                               last_name='Mylastname',
                               gender ='N',
                               birth_date = '2008-01-01',
                               class_room = self.class_room)

    def tearDown(self):
        del self.client

    def test_list_students(self):
        response = self.client.get('/admin/school/student/')
        self.failUnless(200 == response.status_code)

    def test_list_classrooms(self):
        response = self.client.get('/admin/school/classroom/')
        self.failUnless(200 == response.status_code)
        
    def test_search_students(self):
        response = self.client.get('/admin/school/student/?q=test')
        self.failUnless(200 == response.status_code)
    
    def test_select_classroom(self):
        response = self.client.get('/admin/school/classroom/%s/' % self.class_room.id)
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_add_classroom(self):
        """
        try to add new classroom with some students in it
        """
        call_command('loaddata', 'iconfig/fixtures/school/test_data/school.student.json')
        response = self.client.get('/admin/school/classroom/add/')
        self.failUnless(200 == response.status_code)
        post_data = {'year': 'Y1',
                     'students_in_class': ['31', '33','35','37', self.student.pk], 
                     '_save': 'Save',
                    }
        response = self.client.post('/admin/school/classroom/add/', post_data)
        print 'status code = ', response.status_code
        # status 200 could means error
        self.failUnless(302 == response.status_code)
        classroom = ClassRoom.objects.get(year='Y1')
        print 'students = ', classroom.students.all()
        self.assertEquals(5, classroom.students.count())
        
    def test_select_student(self):
        response = self.client.get('/admin/school/student/%s/' % self.student.id)
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)
