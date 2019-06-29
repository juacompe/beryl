# Create your views here.

from django.http import HttpResponse
from finance.models import Invoice, InvoiceItem, Receipt, ReceiptItem
from datetime import datetime
from finance.models import Invoice

#excel
from xlrd import open_workbook
from xlwt import easyxf,Bitmap
from xlwt import Workbook, XFStyle, Borders, Pattern, Font, easyxf
from xlutils.copy import copy
import os, tempfile
from django.conf import settings
import locale

def number_to_currency(number):
    locale.setlocale(locale.LC_ALL, settings.LOCALE)
    #$
    converted = unicode(locale.currency(number,grouping=True),errors='ignore')
    return converted.replace('$','')

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
        #you need to have text_export.xls in your current path. It's a dummy file for invoice template
        print '#################'
        print settings.INV_TEMPLATE
        rb = open_workbook(settings.INV_TEMPLATE,formatting_info=True)
        rs = rb.sheet_by_index(0)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        #student_name
        ws.write(12,2,invoice.get().student.full_name)
        #classroom
        ws.write(12,5,invoice.get().student.class_room.year)
        #duedate
        ws.write(11,2,str(invoice.get().deadline))
        #term (from settings.py)
        ws.write(10,2,settings.TERM)
        #invoice_item
        items = InvoiceItem.objects.filter(invoice=invoice)
        #write item in excel
        item_in_excel(ws,items,settings.INV_TEMPLATE)
##        row = 14
##        for item in items:
##            #item.name
##            ws.write(row,0,unicode(item.name),style_name)
##            #item.amount
##            ws.write(row,5,item.amount,style_amount)
##            row = row + 1
        #item.total
        ws.write(35,5,number_to_currency(invoice.get().total()),style_amount)
        filename_save = 'inv_'+ str(invoice.get().id) + '_'+ str(datetime.now()).replace('.','_')
        #wb.save(filename_save)
        fd, fn = tempfile.mkstemp()
        os.close(fd)
        wb.save(fn)
        fh = open(fn, 'rb')
        resp = fh.read()
        fh.close()
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
        filename_save, resp = create_excel_with(settings.REP_TEMPLATE, receipt, timestamp)
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

def create_excel_with(template, receipt, timestamp):
    style_amount, style_name = excel_style()
    rb = open_workbook(template,formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    #student_name
    #ws.write(8,2,receipt.get().student.full_name)
    #you need to have text_export.xls in your current path. It's a dummy file for invoice template
    print '#################'
    print settings.REP_TEMPLATE
    #receipt.id
    ws.write(4,1,str(receipt.get().id))
    #refer to invoice
    ws.write(4,3,str(receipt.get().invoice.id))
    #date paid
    ws.write(5,1,str(timestamp))
    #item.total
    ws.write(35,5,number_to_currency(receipt.get().total()),style_amount)
    items = ReceiptItem.objects.filter(receipt=receipt)
    #write item in excel
    item_in_excel(ws,items,settings.REP_TEMPLATE)
    filename_save = 'rep_' + str(receipt.get().id) + '_'+ str(datetime.now()).replace('.','_')
    #wb.save(filename_save)
    fd, fn = tempfile.mkstemp()
    os.close(fd)
    wb.save(fn)
    fh = open(fn, 'rb')
    resp = fh.read()
    fh.close()
    return filename_save, resp

def excel_style():
    borders_amount = Borders()
    borders_amount.right = Borders.THIN
    borders_amount.top = Borders.THIN
    borders_amount.bottom = Borders.THIN

    borders_name = Borders()
    borders_name.left = Borders.THIN
    borders_name.right = Borders.THIN
    borders_name.top = Borders.THIN
    borders_name.bottom = Borders.THIN

    style_amount = XFStyle()
    style_amount.borders = borders_amount

    style_name = XFStyle()
    style_name.borders = borders_name
    return style_amount, style_name

def insert_school_logo(ws):
    ws.col(1).width = 20 * 256
    ws.insert_bitmap(settings.LOGO_PATH, 0, 1, 0.9, 0.65, 0.9, 0.65)
    return ws

def item_in_excel(ws,items,template):
    style_amount, style_name = excel_style()
    ws = insert_school_logo(ws)
    row = 14
    for item in items:
        #item.name
        ws.write(row,0,unicode(item.name),style_name)
        #item.amount
        ws.write(row,5,number_to_currency(item.amount),style_amount)
        row = row + 1