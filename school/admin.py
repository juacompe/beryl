from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField

from models import *
from utilities.admin_utils import export_model_to_csv

class StudentAdmin(admin.ModelAdmin):
    actions = [export_model_to_csv]
    list_display = ('student_id', 'full_name', 'gender', 'class_room', 'registration_date')
    list_filter = ('class_room', 'gender')
    search_fields = ('first_name', 'middle_name', 'last_name' )

    fieldsets = (
        (None, {
            'fields': (('first_name', 'middle_name', 'last_name'), 
                       ('gender', 'birth_date', 'nationality'),
                       ('first_language', 'second_language', 'class_room'),)
        }),
        ('Father information', {
            'fields': (('father_name', 'father_nationality'), 
                       ('father_email', 'father_telephone'),
                        'father_home_address',) 
        }),
        ('Mother information', {
            'fields': (('mother_name','mother_nationality'), 
                       ('mother_email', 'mother_telephone'),
                        'mother_home_address',)
        }),
    )

class ClassroomAdminForm(ModelForm):
    '''
    I got this class from Rowan's post in the link below
    http://stackoverflow.com/questions/1691299/can-django-admin-handle-a-one-to-many-relationship-via-related-name
    '''
    students_in_class = ModelMultipleChoiceField(
                            queryset=Student.objects.all(),
                            required=False,)
    
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(ClassroomAdminForm, self).__init__(*args, **kwargs)
        pk_list = self.instance.students.values_list('pk')
        if self.instance.pk is not None:
            self.initial['students_in_class'] = [values[0] for values in pk_list]

    def save(self, commit=True):
        instance = super(ClassroomAdminForm, self).save(commit)
        
        def save_m2m():
            '''
            when a form is saved w/o commit, the save function must add save_m2m
            method to the instance for futher use
            '''
            instance.students = self.cleaned_data['students_in_class']
            print 'in form, students = ', instance.students.all()

        if commit:
           save_m2m() # if commit, call save_m2m

        elif hasattr(self, 'save_m2m'):
           # in case there are existing m2m
           save_old_m2m = self.save_m2m

           def save_both():
               save_old_m2m()
               save_m2m()

           self.save_m2m = save_both
        else:
           self.save_m2m = save_m2m
        return instance

    save.alters_data = True


class ClassroomAdmin(admin.ModelAdmin):
    form = ClassroomAdminForm
    list_display = ('year',
                    'academic_year',
                   )
    list_filter = ('year',)


admin.site.register(Student, StudentAdmin)
admin.site.register(ClassRoom, ClassroomAdmin)
