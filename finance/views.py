from django.http import HttpResponse
from django.conf import settings
from finance.models import Invoice, InvoiceItem, Receipt
from datetime import datetime
from finance.models import Invoice
from finance.excel import excel_style, create_excel_with, write_receipt, write_invoice
from finance.utils import number_to_currency


def invoice_detail(request, inv_id):
    if request.method == 'GET':
        #student = Student.objects.filter(id=student_id)
        invoice = Invoice.objects.filter(id=inv_id)
        if invoice:
            items = InvoiceItem.objects.filter(invoice=invoice)
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
            </tr>''' % (inv_id, invoice.get().student.full_name, invoice.get().student.class_room.year,\
                        number_to_currency(invoice.get().total()) ) + invoice_item_html

            html = html + '''</tbody></table></body></html>'''
            invobj = Invoice.objects.get(id=inv_id)
            invobj.date_viewed = datetime.now()
            invobj.save()
        else:
            html = 'This invoice could not be found'
        return HttpResponse(html)

#need to be refactored if you use school as a service
def export_invoice_as_excel(request,inv_id):
    style_amount, style_name = excel_style()
    invoice = Invoice.objects.filter(id = inv_id)
    if invoice:
        timestamp = datetime.now()
        filename_save, resp = create_excel_with(settings.INV_TEMPLATE, invoice, timestamp, write_invoice)
        response = HttpResponse(resp, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (unicode(filename_save),)
        invobj = Invoice.objects.get(id=inv_id)
        invobj.date_viewed = datetime.now()
        invobj.save()
        print "status_code:" + str(response.status_code)
        return response
    else:
        print 'no invoice to export'
        return HttpResponse('This invoice could not be found')

#need to be refactored if you use school as a service
def export_receipt_as_excel(request,rep_id):
    timestamp = datetime.now()
    receipt = Receipt.objects.filter(id = rep_id)
    if receipt:
        filename_save, resp = create_excel_with(settings.REP_TEMPLATE, receipt, timestamp, write_receipt)
        response = HttpResponse(resp, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (unicode(filename_save),)

        repobj = Receipt.objects.get(id=rep_id)
        repobj.date_paid = timestamp
        repobj.save()
        print "status_code:" + str(response.status_code)
        return response
    else:
        print 'no receipt to export'
        return HttpResponse('This receipt could not be found')
