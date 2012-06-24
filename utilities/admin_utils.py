#!/usr/bin/env python
import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from datetime import datetime

def export_model_to_csv(modeladmin, request, queryset ):
    """
    Generic csv export admin action.
    """
    #queryset = Student.objects.all()
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (unicode(opts).replace('.', '_'),str(datetime.now()).replace('.','_'))
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_model_to_csv.short_description = "export records"
