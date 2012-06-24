import unittest
from django.db import IntegrityError
from school.models import Student, ClassRoom
from datetime import datetime
class TestStudent(unittest.TestCase):
    def setUp(self):
        self.classroom = ClassRoom.objects.create(year='N')

    def test_student_id(self):
        """
        The format of the student id is YYmmddXXXX while XXXX is a running 
        number of applying student on a particular day.

        For example, a student with student id 1009180023 is the 23rd student
        who applied on Sep 18, 2010.
        """
        s = Student()
        s.registration_order = 23
        s.registration_date = datetime(2010,9,18)
        self.assertEquals('1009180023', s.student_id) 

    def test_save_student_has_registration_order(self):
        # student requires at least first name, last name, birth date and classroom 
        s = Student()
        self.assertRaises(IntegrityError, s.save)
        s = Student(first_name='Harry',
                    last_name='Potter',
                    birth_date=datetime(2003,5,1),
                    class_room=self.classroom,
                   )
        s.save()
        # student can be saved
        self.assertTrue(s.id)
        # student registration order was generated
        self.assertEquals(1, s.registration_order)
        self.assertEquals(datetime.today().date(), s.registration_date.date())

        s = Student(first_name='Hermione',
                    last_name='Granger',
                    birth_date=datetime(2003,5,1),
                    class_room=self.classroom,
                   )
        s.save()
        self.assertEquals(2, s.registration_order)
        self.assertEquals(datetime.today().date(), s.registration_date.date())

