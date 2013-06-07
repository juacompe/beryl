from django.test import TestCase 
from django.test.client import Client
from testutils import factory
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem

class TestAdmin(TestCase):
    def setUp(self):
        self.login_as_admin()
        self.prepare_test_data()

    def login_as_admin(self):
        factory.create_superuser('admin', '1234')
        self.client.login(username='admin', password='1234')
        
    def prepare_test_data(self):
        invoice = self.invoice = factory.create_invoice()
        invoice_item = factory.create_invoice_item('Pay for fee', 100, invoice) 
        receipt = factory.create_receipt(invoice) 
        receipt_item = factory.create_receipt_item('Pay for fee', 100, receipt)

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
