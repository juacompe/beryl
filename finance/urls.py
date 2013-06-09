from django.conf.urls import patterns, include, url

urlpatterns = patterns('finance.views',
    url(r'^invoice/(?P<inv_id>\d+)/$', 'invoice_detail'),
    url(r'^invoice/xls/(?P<inv_id>\d+)/$', 'export_invoice_as_excel'),
    url(r'^receipt/xls/(?P<rep_id>\d+)/$', 'export_receipt_as_excel'),
    url(r'^receipt/new/$', 'new_receipt', name='new_receipt'),
)
