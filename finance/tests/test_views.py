#-------------------------------------------------------------------------------
# Name:        test_views.py
# Purpose:
#
# Author:      natty
#
# Created:     12/11/2010
# Copyright:   (c) natty 2010
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from datetime import datetime
from django.test import TestCase 
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from finance.views import number_to_currency, excel_style
from school.models import Student, ClassRoom
from testutils import factory
from testutils.basetest import AdminTestCase

class TestAddNewReceipt(AdminTestCase):
    def setUp(self):
        self.login_as_admin()

    def test_get_new_receipt(self):
        response = self.client.get('/finance/receipt/new/')
        self.assertEqual(200, response.status_code)

    def test_get_new_receipt_without_login(self):
        self.client.logout()
        url = '/finance/receipt/new/'
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=%s' % url)


class TestInvoiceReceipt(AdminTestCase):
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

    def test_number_to_currency(self):
        converted = number_to_currency(1000000)
        print converted
        self.failUnless('1,000,000.00' == converted)

    def test_excel_style(self):
        style_amount, style_name = excel_style()
        print style_amount
        print style_name
        self.assertNotEqual('',style_amount)
        self.assertNotEqual('',style_name)
#<xlwt.Style.XFStyle object at 0x02A84E30>
#<xlwt.Style.XFStyle object at 0x02A84670>
