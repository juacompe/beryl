from datetime import datetime
from django.contrib.auth.models import User
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from school.models import Student, ClassRoom

NOW = datetime.now()

def create_superuser(username='admin', password='iamnottellingyou'):
    kwargs = dict(username=username, email='admin@somewhere.com', password=password)
    User.objects.create_superuser(**kwargs)
    
def create_class_room(year='N'):
    class_room, created = ClassRoom.objects.get_or_create(year='N')
    return class_room 
    
def create_student(class_room=None):
    class_room = class_room or create_class_room()
    kwargs = {
        'birth_date': '2008-01-01',
        'class_room': class_room,
        'first_name': 'Myfirstname',
        'gender': 'N',
        'last_name': 'Mylastname',
        'middle_name': 'Mymiddlename',
    }
    student, created = Student.objects.get_or_create(**kwargs)
    return student
    
def create_invoice(student=None):
    student = student or create_student()
    invoice, created = Invoice.objects.get_or_create(student=student, deadline=NOW)
    return invoice

def create_invoice_item(name, amount, invoice=None):
    invoice = invoice or create_invoice()
    kwargs = dict(invoice=invoice, amount=100, name='Pay for fee')
    invoice_item, created = InvoiceItem.objects.get_or_create(**kwargs)
    return invoice_item
    
def create_receipt(invoice=None):
    invoice = invoice or create_invoice()
    receipt, created = Receipt.objects.get_or_create(invoice=invoice)
    return receipt
    
def create_receipt_item(name, amount, receipt=None):
    receipt = receipt or create_receipt()
    kwargs = dict(receipt=receipt, amount=100, name='Pay for fee')
    receipt_item, created = ReceiptItem.objects.get_or_create(**kwargs)
    return receipt_item

