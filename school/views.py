# Create your views here.
from datetime import datetime
from school.models import Student

import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

#still obsolete, should be moved to invoice to use for invoice/receipt
def export_as_csv(request, student_id):
    """
    Generic csv export admin action.
    """
    
    queryset = Student.objects.filter(id=student_id)
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s_%s_%s.csv' % (unicode(opts).replace('.', '_'),student_id,str(datetime.now()).replace('.','_'))
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

