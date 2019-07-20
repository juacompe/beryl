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

from django.test import TestCase 
from django.test.client import Client
from django.contrib.auth.models import User
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from school.models import Student, ClassRoom
from finance.views import number_to_currency
from datetime import datetime

class TestInvoiceReceipt(TestCase):
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

    def test_number_to_currency(self):
        converted = number_to_currency(1000000)
        print converted
        self.failUnless('1,000,000.00' == converted)
