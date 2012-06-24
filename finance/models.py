from django.db import models
from datetime import datetime, timedelta

class Invoice(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_viewed = models.DateTimeField(null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=datetime.now()+timedelta(90))
    student = models.ForeignKey('school.Student', related_name='student')

    def __unicode__(self):
        return 'Invoice no. %s = %s' % (self.id,self.total())

    def total(self):
        return self.items.all().aggregate(models.Sum('amount')).get('amount__sum') or 0

    def is_due(self):
        paying_date = datetime.now()
        try:
            paying_date = self.receipt.date_paid
        except Receipt.DoesNotExist:
            pass
        return paying_date > self.deadline

    def invoice_link(self):
        if not self.date_viewed:
            #need to find another save function. Now it change all date_viewed value in database if using self.save()
            #self.save()
            return '<a href="/finance/invoice/%s/">view invoice detail</a>' % (self.id)
        else:
            return '<a href="/finance/invoice/%s/">printed</a>' % (self.id)
        #return '<a href="{%url school.views.invoice_detail self.id %}">view invoice detail</a>'
    invoice_link.allow_tags = True

    def invoice_xls(self):
        if not self.date_viewed:
            return '<a href="/finance/invoice/xls/%s/">export as excel</a>' % (self.id)
        else:
            return '<a href="/finance/invoice/xls/%s/">printed</a>' % (self.id)
        #return '<a href="{%url school.views.invoice_detail self.id %}">view invoice detail</a>'
    invoice_xls.allow_tags = True

class Item(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'Item %s (%s baht)' % (self.name,self.amount)
class InvoiceItem(Item):
    invoice = models.ForeignKey('Invoice', related_name='items')

def invoice_to_receipt(invoice):
    """
    clone items from the given invoice, set relation to it and persist
    """
    receipt = Receipt.objects.create(invoice=invoice)
    for item in invoice.items.all():
        receipt_item = receipt.items.create(name=item.name, amount=item.amount)
    receipt.save()
    return receipt


class Receipt(models.Model):
    date_paid = models.DateTimeField(auto_now_add=True)
    invoice = models.OneToOneField('Invoice', related_name='receipt', null=True, blank=True)

    def __unicode__(self):
        return 'Receipt no. %s = %s' % (self.id,self.total())

    def total(self):
        return self.items.all().aggregate(models.Sum('amount')).get('amount__sum') or 0

    def receipt_xls(self):
##        if not self.date_paid:
##            return '<a href="/finance/receipt/xls/%s/">export as excel</a>' % (self.id)
##        else:
##            return '<a href="/finance/receipt/xls/%s/">printed</a>' % (self.id)
        return '<a href="/finance/receipt/xls/%s/">export as excel</a>' % (self.id)
    receipt_xls.allow_tags = True

class ReceiptItem(Item):
    receipt = models.ForeignKey('Receipt', related_name='items')

