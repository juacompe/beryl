from datetime import datetime, timedelta
from django.test import TestCase
from finance.models import *
from school.models import *
from testutils import factory

class TestReceipt(TestCase):
    def setUp(self):
        kwargs = {
            'date_viewed': datetime(2010,5,13,8,27), 
            'date_paid': datetime(2010,11,22,16,27),
        }
        invoice = self.invoice = factory.create_invoice(**kwargs)
        invoice_item = factory.create_invoice_item('Pay for fee', 100, invoice) 
        invoice_item = factory.create_invoice_item('Pay for fun', 50000, invoice) 

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

    def test_invoice_to_receipt(self):
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

    def test_create_2_receipts_for_an_invoice(self):
        """
        Sometimes, a payment is received partially. Therefore, the system must
        record 2 receipts for an invoice.
        """
        receipt = factory.create_receipt(self.invoice)
        receipt_for_1st_payment = factory.create_receipt_item('Pay for fee', 100, receipt)
        receipt = Receipt.objects.create(invoice=self.invoice)
        receipt_for_2nd_payment = factory.create_receipt_item('Pay for fun', 50000, receipt)
        self.assertEqual(2, Receipt.objects.all().count())

