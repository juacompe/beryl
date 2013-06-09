from django.conf.urls import *

urlpatterns = patterns('',
    # Example:
    # (r'^beryl/', include('beryl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^invoice/(?P<inv_id>\d+)/$', 'finance.views.invoice_detail'),
    (r'^invoice/xls/(?P<inv_id>\d+)/$', 'finance.views.export_invoice_as_excel'),
    (r'^receipt/xls/(?P<rep_id>\d+)/$', 'finance.views.export_receipt_as_excel'),
)
