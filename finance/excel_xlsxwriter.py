# -*- coding: utf-8 -*-
import xlsxwriter
#from django.conf import settings

def create_receipt():
    filename = "/tmp/receipt.xlsx"
    s = Spreadsheet(filename)
    s.close()

class Spreadsheet(object):
    def __init__(self, filename):
        self.workbook = xlsxwriter.Workbook(filename)
        self.styles = {}
        self.workbook.set_size(1000, 1200)
        self.styles['bold'] = self.workbook.add_format({'bold': True})
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_paper(9)
        self.create_logo()
        self.create_style_school_name()
        self.create_style_sub_title()
        self.create_receipt()
        self.create_address()
        self.create_for_invoice()
        self.create_class()
        self.create_table()
        self.write_body()

    def close(self):
        self.workbook.close()

    def write_body(self):
        worksheet = self.worksheet
        worksheet.set_column('A:A', 6)
        worksheet.set_column('B:B', 19)
        worksheet.set_column('C:C', 59)
        worksheet.set_column('E:E', 19)
        worksheet.write('A5', 'No.')
        worksheet.write('A6', 'Date.')
        worksheet.write('A8', 'Receive with thanks from:')
        worksheet.write('A9', 'Name of student:')
        worksheet.write('A10', 'Address:')
        worksheet.write('A35', 'Thank you very much for your kind support.')
        worksheet.write('B36', 'cash/cheque#: ')
        worksheet.write('D36', 'date: ')
        worksheet.write('B37', 'Bank/Branch: ')
        worksheet.write('B38', 'Receive by: ')

    def create_logo(self):
        # logo = settings.LOGO_PATH
        logo = '/Users/juacompe/Projects/github.com/juacompe/beryl/media/rcis_logo.png'
        self.worksheet.insert_image('A1', logo)

    def create_style_school_name(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_font_color('#006737')
        fmt.set_align('center')
        self.worksheet.write('C2', 'RUAM RUDEE LEARNING CENTRE', fmt)

    def create_style_sub_title(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_align('center')
        fmt.set_font_size(15)
        self.worksheet.write('C3', 'Nursery, Pre-School and Elementary', fmt)

    def create_address(self):
        address = """
        25 / 3-4 Ruam Rudee Soi 1, Ploenchit Road, Bangkok 10330
        Tel: 0-2254-4380, 0-2255-4507 / Fax: 0-2650-9747
        Email: info@rcis.ac.th  Website: www.rcis.ac.th
        """
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        fmt.set_align('center')
        self.worksheet.write('C4', address, fmt)

    def create_receipt(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_underline()
        fmt.set_font_name('Arial')
        fmt.set_align('center')
        self.worksheet.write('C7', 'RECEIPT', fmt)

    def create_for_invoice(self):
        fmt = self.workbook.add_format()
        fmt.set_align('right')
        fmt.set_font_name('Arial')
        self.worksheet.write('D5', 'for invoice (optional): ', fmt)

    def create_class(self):
        fmt = self.workbook.add_format()
        fmt.set_align('right')
        fmt.set_font_name('Arial')
        fmt.set_bold()
        self.worksheet.write('D11', 'Class :', fmt)

    def create_table(self):
        fmt = self.workbook.add_format()
        self.set_table_header(fmt)
        fmt.set_align('center')
        fmt.set_top(1)
        fmt.set_bottom(1)
        fmt.set_left(1)
        fmt.set_right(1)
        self.worksheet.merge_range('A12:D12', 'Description', fmt)
        self.worksheet.write('E12', u'฿  Amount', fmt)
        def desc(row):
            self.worksheet.merge_range('A%s:D%s'%(row, row), '', fmt)
        def amount(row):
            self.worksheet.write('E%s'%row, '', fmt)
        map(desc,range(13, 35))
        map(amount,range(13, 35))
        total = self.workbook.add_format()
        self.set_table_header(total)
        self.worksheet.write('B34', 'TOTAL   (Baht)', total)

    def set_table_header(self, fmt):
        fmt.set_font_name('Arial')
        fmt.set_bold()
        fmt.set_font_size(15)
