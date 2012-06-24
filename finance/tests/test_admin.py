from django.test import TestCase 

from django.test.client import Client
from django.contrib.auth.models import User
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from school.models import Student, ClassRoom
from datetime import datetime

class TestAdmin(TestCase):
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
        self.invoice = Invoice.objects.create(student=self.student,deadline=datetime.now())
        self.invoice_item = InvoiceItem.objects.create(invoice=self.invoice,amount=100,name='Pay for fee' )
        self.receipt = Receipt.objects.create(invoice=self.invoice)
        self.receipt_item = ReceiptItem.objects.create(receipt=self.receipt,amount=100,name='Pay for fee' )


    def tearDown(self):
        del self.client

    def test_list_invoices(self):
        response = self.client.get('/admin/finance/invoice/')
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_search_invoices(self):
        response = self.client.get('/admin/finance/invoice/?q=test')
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_select_invoice(self):
        response = self.client.get('/admin/finance/invoice/%s/' % self.invoice.id)
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_view_invoice_for_printing(self):
        response = self.client.get('/finance/invoice/1/')
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_list_receipts(self):
        response = self.client.get('/admin/finance/receipt/')
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_search_receipt(self):
        response = self.client.get('/admin/finance/receipt/?q=test')
        print 'status code = ', response.status_code
        self.failUnless(200 == response.status_code)

    def test_export_invoice_as_excel_link(self):
        response = self.client.get('/admin/finance/invoice/')
        self.failUnless(200 == response.status_code)
        assert '<a href="/finance/invoice/xls/1/">export as excel</a>' in response.content
        response = self.client.get('/finance/invoice/xls/1/')
        self.failUnless(200 == response.status_code)
        #could be printed after the first print
        response = self.client.get('/admin/finance/invoice/')
        self.failUnless(200 == response.status_code)
        assert '<a href="/finance/invoice/xls/1/">printed</a>' in response.content

    def test_export_receipt_as_excel_link(self):
        response = self.client.get('/admin/finance/receipt/')
        self.failUnless(200 == response.status_code)
        assert '<a href="/finance/receipt/xls/1/">export as excel</a>' in response.content
        response = self.client.get('/finance/receipt/xls/1/')
        self.failUnless(200 == response.status_code)
        #could be printed after the first print
##        response = self.client.get('/admin/finance/receipt/')
##        self.failUnless(200 == response.status_code)
##        assert '<a href="/finance/receipt/xls/1/">printed</a>' in response.content
