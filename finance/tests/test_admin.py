from django.test import TestCase 
from django.test.client import Client
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from testutils import factory
from testutils.basetest import AdminTestCase

class TestAdmin(AdminTestCase):
    def setUp(self):
        self.login_as_admin()
        self.prepare_test_data()

    def prepare_test_data(self):
        invoice = self.invoice = factory.create_invoice()
        invoice_item = factory.create_invoice_item('Pay for fee', 100, invoice) 
        receipt = factory.create_receipt(invoice) 
        receipt_item = factory.create_receipt_item('Pay for fee', 100, receipt)

    def tearDown(self):
        del self.client

    def test_list_invoices(self):
        response = self.client.get('/admin/finance/invoice/')
        self.assertEqual(200, response.status_code)

    def test_search_invoices(self):
        response = self.client.get('/admin/finance/invoice/?q=test')
        self.assertEqual(200, response.status_code)

    def test_select_invoice(self):
        response = self.client.get('/admin/finance/invoice/%s/' % self.invoice.id)
        self.assertEqual(200, response.status_code)

    def test_view_invoice_for_printing(self):
        response = self.client.get('/finance/invoice/1/')
        self.assertEqual(200, response.status_code)

    def test_list_receipts(self):
        response = self.client.get('/admin/finance/receipt/')
        self.assertEqual(200, response.status_code)

    def test_search_receipt(self):
        response = self.client.get('/admin/finance/receipt/?q=test')
        self.assertEqual(200, response.status_code)

    def test_export_invoice_as_excel_link(self):
        export_link = '<a href="/finance/invoice/xls/1/">export as excel</a>'
        printed_link = '<a href="/finance/invoice/xls/1/">printed</a>'
        self.assert_invoice_list_contains_export_link(export_link)
        self.print_invoice()
        self.assert_invoice_list_contains_printed_link(export_link, printed_link)

    def assert_invoice_list_contains_export_link(self, export_link):
        response = self.client.get('/admin/finance/invoice/')
        self.assertContains(response, export_link)

    def print_invoice(self):
        response = self.client.get('/finance/invoice/xls/1/')

    def assert_invoice_list_contains_printed_link(self, export_link, printed_link):
        """
        Invoices are not encouraged to be printed twice.

        So after printed once, the export link is changed to printed link.
        """
        response = self.client.get('/admin/finance/invoice/')
        self.assertNotContains(response, export_link)
        self.assertContains(response, printed_link)

    def test_export_receipt_as_excel_link(self):
        export_link = '<a href="/finance/receipt/xls/1/">export as excel</a>'
        self.assert_receipt_list_contains_export_link(export_link)
        self.print_receipt()
        self.assert_receipt_list_still_contains_export_link(export_link)

    def assert_receipt_list_contains_export_link(self, export_link):
        response = self.client.get('/admin/finance/receipt/')
        self.assertContains(response, export_link)

    def print_receipt(self):
        response = self.client.get('/finance/receipt/xls/1/')
        self.assertEqual(200, response.status_code)

    def assert_receipt_list_still_contains_export_link(self, export_link):
        """
        Receipts, unlike invoices, can be printed twice.
        """
        self.assert_receipt_list_contains_export_link(export_link)

