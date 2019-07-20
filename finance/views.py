from django.http import HttpResponse
from django.conf import settings
from finance.models import Invoice, Receipt
from datetime import datetime
from finance.models import Invoice
from finance.excel import excel_style, create_excel_with, write_receipt, write_invoice
from finance.excel_xlsxwriter import InvoiceSheet, ReceiptSheet
from finance.utils import number_to_currency


def invoice_detail(request, inv_id):
    if request.method == 'GET':
        #student = Student.objects.filter(id=student_id)
        invoice = Invoice.objects.get(id=inv_id)
        if invoice:
            items = invoice.items.all()
            invoice_item_html = ''
            for item in items:
                invoice_item_html = invoice_item_html + '''<tr>
                    <td>%s</td>
                    <td>%s</td>
                </tr>''' % (item.name,item.amount)
            html = '''<html><body><table>
            <tbody><tr>
                <td>Id</td>
                <td>%s</td>
            </tr>
            <tr>
                <td>Student</td>
                <td>%s</td>
            </tr>
            <tr>
                <td>Class</td>
                <td>%s</td>
            </tr>
            <tr>
                <td>Amount</td>
                <td>%s</td>
            </tr>
            <tr>
                <td>Items</td>
            </tr>''' % (inv_id, invoice.student.full_name, invoice.student.class_room.year,\
                        number_to_currency(invoice.total()) ) + invoice_item_html

            html = html + '''</tbody></table></body></html>'''
            invobj = Invoice.objects.get(id=inv_id)
            invobj.date_viewed = datetime.now()
            invobj.save()
        else:
            html = 'This invoice could not be found'
        return HttpResponse(html)

#need to be refactored if you use school as a service
def export_invoice_as_excel(request,inv_id):
    timestamp = datetime.now()
    try:
        invoice = Invoice.objects.get(id = inv_id)
        filename_save = InvoiceSheet.get_file_name(inv_id, timestamp)
        path = InvoiceSheet.get_file_path(inv_id, timestamp)
        s = InvoiceSheet(path, settings.LOGO_PATH)
        s.set_child_name(invoice.student.full_name)
        s.set_deadline(str(invoice.deadline))
        s.set_class_room(invoice.student.class_room.year)
        s.set_items(invoice.items.all())
        s.set_total(invoice.total())
        s.create()
        resp = s.get_binary_content()

        response = HttpResponse(resp, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (unicode(filename_save),)
        invobj = Invoice.objects.get(id=inv_id)
        invobj.date_viewed = datetime.now()
        invobj.save()
        print "status_code:" + str(response.status_code)
        return response
    except Invoice.DoesNotExist:
        print 'no invoice to export'
        return HttpResponse('This invoice could not be found')

#need to be refactored if you use school as a service
def export_receipt_as_excel(request,rep_id):
    timestamp = datetime.now()
    try:
        receipt = Receipt.objects.get(id = rep_id)
        filename_save = ReceiptSheet.get_file_name(receipt.id, timestamp)
        path = ReceiptSheet.get_file_path(receipt.id, timestamp)
        s = ReceiptSheet(path, settings.LOGO_PATH)
        s.set_invoice_number(receipt.invoice.id)
        s.set_receipt_id(receipt.id)
        s.set_date(timestamp)
        s.set_items(receipt.items.all())
        s.set_total(receipt.total())
        s.create()
        resp = s.get_binary_content()

        response = HttpResponse(resp, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (unicode(filename_save),)

        repobj = Receipt.objects.get(id=rep_id)
        repobj.date_paid = timestamp
        repobj.save()
        print "status_code:" + str(response.status_code)
        return response
    except Receipt.DoesNotExist:
        print 'no receipt to export'
        return HttpResponse('This receipt could not be found')
