from django.contrib import admin

from models import *
from utilities.admin_utils import export_model_to_csv

class InvoiceItemInlines(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class ReceiptItemInlines(admin.TabularInline):
    model = ReceiptItem
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    actions = [export_model_to_csv]
    search_fields = ['student__first_name','student__middle_name','student__last_name','id']
    list_display = ('student',
                    'total',
                    'date_created',
                    'date_viewed',
                    'deadline',
                    'is_due',
                    'invoice_link',
                    'invoice_xls',
                   )

    fields = ('deadline', 'student')

    inlines = [InvoiceItemInlines,]

class ReceiptAdmin(admin.ModelAdmin):
    actions = [export_model_to_csv]
    search_fields = ['invoice__student__first_name',
                     'invoice__student__middle_name',
                     'invoice__student__last_name','id']
    list_display = ('invoice',
                    'total',
                    'date_paid',
                    'receipt_xls',
                   )

    field_sets = (
        (None, {
            'fields': (('date_viewed', 'date_paid', 'deadline'),)
        }),
    )

    inlines = [ReceiptItemInlines,]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Receipt, ReceiptAdmin)
