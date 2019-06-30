from xlwt import Workbook, XFStyle, Borders, Pattern, Font, easyxf
from xlrd import open_workbook
from xlwt import easyxf,Bitmap
from xlutils.copy import copy
import os, tempfile
from django.conf import settings

from finance.models import InvoiceItem
from finance.utils import number_to_currency

def create_excel_with(template, receipt, timestamp, write_fn):
    #you need to have text_export.xls in your current path. It's a dummy file for invoice template
    print '#################'
    print template
    rb = open_workbook(template,formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    filename_save = write_fn(template, receipt, timestamp, ws)
    #wb.save(filename_save)
    fd, fn = tempfile.mkstemp()
    os.close(fd)
    wb.save(fn)
    fh = open(fn, 'rb')
    resp = fh.read()
    fh.close()
    return filename_save, resp

def write_invoice(template, invoice, timestamp, ws):
    style_amount, style_name = excel_style()
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
    item_in_excel(ws,items,template)
    #item.total
    ws.write(35,5,number_to_currency(invoice.get().total()),style_amount)
    filename_save = 'inv_'+ str(invoice.get().id) + '_'+ str(timestamp).replace('.','_')
    return filename_save

def write_receipt(template, receipt, timestamp, ws):
    style_amount, style_name = excel_style()
    #student_name
    #ws.write(8,2,receipt.student.full_name)
    #you need to have text_export.xls in your current path. It's a dummy file for invoice template
    #receipt.id
    ws.write(4,1,str(receipt.id))
    #refer to invoice
    ws.write(4,3,str(receipt.invoice.id))
    #date paid
    ws.write(5,1,str(timestamp))
    #item.total
    ws.write(35,5,number_to_currency(receipt.total()),style_amount)
    items = receipt.items.all()
    #write item in excel
    item_in_excel(ws,items,template)
    filename_save = 'rep_' + str(receipt.id) + '_'+ str(timestamp).replace('.','_')
    return filename_save

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
