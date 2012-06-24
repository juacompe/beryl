import unittest

from finance.models import *
from school.models import *
from datetime import datetime, timedelta

class TestReceipt(unittest.TestCase):
    def setUp(self):
        self.class_room = ClassRoom.objects.create(year='N')
        self.student = Student.objects.create(first_name='Myfirstname',
                               middle_name='Mymiddlename',
                               last_name='Mylastname',
                               gender ='N',
                               birth_date = '2008-01-01',
                               class_room = self.class_room)
        self.invoice = Invoice.objects.create(student=self.student,
                                              date_viewed=datetime(2010,5,13,8,27),
                                              date_paid=datetime(2010,11,22,16,27),
                                              deadline=datetime.now())
        self.invoice_item = InvoiceItem.objects.create(invoice=self.invoice,
                                                       amount=100,
                                                       name='Pay for fee' )
        self.invoice_item2 = InvoiceItem.objects.create(invoice=self.invoice,
                                                       amount=50000,
                                                       name='Pay for fun' )
    def test_is_not_due(self):
        # dues tomorrow and not yet paid
        self.invoice.deadline = datetime.now() + timedelta(1)
        self.assertFalse(self.invoice.is_due())
        # dues tomorrow and just paid
        invoice_to_receipt(self.invoice)
        self.assertFalse(self.invoice.is_due())

    def test_is_due(self):
        # dues yesterday and not yet paid
        self.invoice.deadline = datetime.now() - timedelta(1)
        self.failUnless(self.invoice.is_due())
        # dues yesterday and just paid
        invoice_to_receipt(self.invoice)
        self.failUnless(self.invoice.is_due())

    def test_receipt_to_invoice(self):
        print 'generating receipt for invoice = ', self.invoice
        receipt = invoice_to_receipt(self.invoice)
        print 'receipt = ', receipt
        self.assertTrue(receipt.id)
        self.assertEquals(receipt.invoice, self.invoice)
        self.assertEquals(receipt.total(), self.invoice.total())
        self.assertEquals(receipt.receipt_xls(),'<a href="/finance/receipt/xls/1/">export as excel</a>')
        print 'all receipt = ', receipt.items.all()
        receipt_item = receipt.items.all()[0]
        self.failUnless('Pay for' in receipt_item.name)
        self.failUnless(receipt_item.amount == 50000 or 100)
