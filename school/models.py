from django.db.models import Max, Model, IntegerField, DateField, CharField, EmailField, TextField, ForeignKey
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
)

CLASS_YEARS = (
    ('N', 'Nursery'),
    ('K1', 'Kindergarten 1'),
    ('K2', 'Kindergarten 2'),
    ('Y1', 'Year 1'),
    ('Y2', 'Year 2'),
    ('Y3', 'Year 3'),
    ('Y4', 'Year 4'),
    ('Y5', 'Year 5'),
    ('Y6', 'Year 6'),
    ('Y7', 'Year 7'),
)

class Student(Model):
    registration_order = IntegerField(blank=True)
    registration_date = DateField(default=datetime.now())
    first_name = CharField(max_length=30, default=None,)
    middle_name = CharField(max_length=30, default='', null=True, blank=True)
    last_name = CharField(max_length=30, default=None,)
    gender = CharField(max_length=1, choices=GENDERS,)
    birth_date = DateField()
    nationality = CharField(max_length=20, default='', blank =True )
    first_language = CharField(max_length=20, default='', blank =True )
    second_language = CharField(max_length=20, default='', blank =True )
    father_name = CharField(max_length=40, default='', blank =True )
    father_nationality = CharField(max_length=20, default='', blank =True )
    father_email = EmailField(max_length=40, default='', blank =True )
    father_home_address = TextField(max_length=100, default='', blank =True )
    father_telephone = CharField(max_length=20, default='', blank =True )
    mother_name = CharField(max_length=40, default='', blank =True )
    mother_nationality = CharField(max_length=20, default='', blank =True )
    mother_email = EmailField(max_length=40, default='', blank =True )
    mother_home_address = TextField(max_length=100, default='', blank =True )
    mother_telephone = CharField(max_length=20, default='', blank =True )
    emergency_contact_person_name = CharField(max_length=40, default='', blank =True )
    emergency_contact_person_telephone = CharField(max_length=20, default='', blank =True )
    class_room = ForeignKey('ClassRoom', related_name='students')

    class Meta:
        verbose_name = 'Student'
        ordering = ['first_name','middle_name','last_name']

    def _full_name(self):
        return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)

    def _student_id(self):
        # format is YYmmddXXXX
        return "%s%04d" % (self.registration_date.strftime('%y%m%d'),
                           self.registration_order)

    def save(self, *args, **kwargs):
        today_applicants = Student.objects.filter(registration_date=datetime.today())
        results = today_applicants.aggregate(Max('registration_order'))
        current = results['registration_order__max']
        self.registration_order = (current or 0) + 1
        super(Student, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.full_name

    def export_to_csv(self):
        return '<a href="/school/student/csv/%s/">export to excel</a>' % (self.id)
        #return '<a href="{%url school.views.invoice_detail self.id %}">view invoice detail</a>'
    export_to_csv.allow_tags = True

    student_id = property(_student_id)
    full_name = property(_full_name)

class ClassRoom(Model):
    year = CharField(max_length=3, choices=CLASS_YEARS, null=False )
    date_opened = DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Classroom'

    def __unicode__(self):
        return u'%s' % self.year

    def academic_year(self):
        return self.date_opened.year
