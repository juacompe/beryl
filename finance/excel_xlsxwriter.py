# -*- coding: utf-8 -*-
import xlsxwriter
import os, tempfile

class Spreadsheet(object):
    def __init__(self, filename, logo):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.logo = logo
        self.styles = {}

    def create(self):
        self.workbook.set_size(1000, 1200)
        self.styles['bold'] = self.workbook.add_format({'bold': True})
        self.worksheet = self.workbook.add_worksheet()
        self.no_row = 7
        self.receipt_row = self.no_row + 2
        self.desc_row = self.receipt_row + 4
        A4 = 9
        self.worksheet.set_paper(A4)
        self.worksheet.fit_to_pages(1, 1)
        self.worksheet.print_area('A1:E38')
        self.create_logo()
        self.create_style_school_name()
        self.create_style_sub_title()
        self.create_receipt()
        self.create_address()
        self.create_for_invoice()
        self.create_class()
        self.create_table()
        self.create_body()
        self.create_footer()
        self.close()

    def close(self):
        self.workbook.close()

    def set_invoice_number(self, i):
        self.invoice_number = i

    def set_receipt_id(self, i):
        self.receipt_id = i

    def set_date(self, d):
        self.timestamp = d

    def set_items(self, items):
        self.items = items

    def set_total(self, t):
        self.total = t

    @staticmethod
    def get_file_name(receipt_id, timestamp):
        return 'rep_' + str(receipt_id) + '_'+ str(timestamp).replace('.','_')

    @staticmethod
    def get_file_path(receipt_id, timestamp):
        filename = Spreadsheet.get_file_name(receipt_id, timestamp)
        return os.path.join(tempfile.mkdtemp(), filename)

    def get_binary_content(self):
        fh = open(self.filename, 'rb')
        resp = fh.read()
        fh.close()
        return resp

    def create_body(self):
        worksheet = self.worksheet
        worksheet.set_column('A:A', 6)
        worksheet.set_column('B:B', 19)
        worksheet.set_column('C:C', 59)
        worksheet.set_column('E:E', 19)
        worksheet.write('A%s'%(self.no_row+3), 'Receive with thanks from:')
        worksheet.write('A%s'%(self.no_row+4), 'Name of student:')
        worksheet.write('A%s'%(self.no_row+5), 'Address:')
        worksheet.write('A35', 'Thank you very much for your kind support.')
        worksheet.set_row(9, 40)
        worksheet.set_row(11, 40)
        worksheet.set_row(34, 40)
        worksheet.set_row(35, 40)

    def create_logo(self):
        self.worksheet.insert_image('A1', self.logo, {'x_scale': 0.95, 'y_scale': 0.81})

    def create_style_school_name(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_font_color('#006737')
        fmt.set_align('center')
        fmt.set_font_name('Times')
        self.worksheet.write('C2', 'RUAM RUDEE LEARNING CENTRE', fmt)

    def create_style_sub_title(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_align('center')
        fmt.set_font_size(15)
        fmt.set_font_name('Times')
        self.worksheet.write('C3', 'Nursery, Pre-School and Elementary', fmt)

    def create_address(self):
        address1 = '25 / 3-4 Ruam Rudee Soi 1, Ploenchit Road, Bangkok 10330'
        address2 = 'Tel: 0-2254-4380, 0-2255-4507 / Fax: 0-2650-9747'
        address3 = 'Email: info@rcis.ac.th  Website: www.rcis.ac.th'
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        fmt.set_align('center')
        self.worksheet.write('C4', address1, fmt)
        self.worksheet.write('C5', address2, fmt)
        self.worksheet.write('C6', address3, fmt)

    def create_receipt(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_underline()
        fmt.set_font_name('Arial')
        fmt.set_align('center')
        self.worksheet.write('C%s'%self.receipt_row, 'RECEIPT', fmt)

    def create_for_invoice(self):
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        # fmt.set_bg_color('#cccccc')
        fmt.set_align('right')
        left = self.workbook.add_format()
        left.set_font_name('Arial')
        left.set_align('left')
        self.worksheet.write('D%s'%(self.no_row+0), 'for invoice (optional): ', fmt)
        self.worksheet.write('E%s'%(self.no_row+0), self.invoice_number, left)
        self.worksheet.write('A%s'%(self.no_row+0), 'No.')
        self.worksheet.write('B%s'%(self.no_row+0), self.receipt_id, left)
        self.worksheet.write('A%s'%(self.no_row+1), 'Date.')
        self.worksheet.write('B%s'%(self.no_row+1), self.timestamp, left)

    def create_class(self):
        fmt = self.workbook.add_format()
        fmt.set_align('right')
        fmt.set_font_name('Arial')
        fmt.set_bold()
        self.worksheet.write('D%s'%(self.desc_row-1), 'Class :', fmt)

    def create_table(self):
        header = self.workbook.add_format()
        body = self.workbook.add_format()
        self.set_table_body(body)
        self.set_table_header(header)
        self.worksheet.merge_range('A%s:D%s' % (self.desc_row, self.desc_row), 'Description', header)
        self.worksheet.write('E%s'%self.desc_row, u'฿  Amount', header)
        def desc(row):
            self.worksheet.merge_range('A%s:D%s'%(self.desc_row+1+row, self.desc_row+1+row), self.get_name(row), body)
        def amount(row):
            self.worksheet.write('E%s'%(self.desc_row+1+row), self.get_amount(row), body)
        map(desc,range(0, 20))
        map(amount,range(0, 20))
        total = self.workbook.add_format()
        self.set_table_header(total)
        self.worksheet.merge_range('A34:D34', 'TOTAL   (Baht)', total)
        self.worksheet.write('E34', self.total, header)

    def get_name(self, row):
        try:
            return self.items[row].name
        except IndexError:
            return ''

    def get_amount(self, row):
        try:
            return self.items[row].amount
        except IndexError:
            return ''

    def set_table_body(self, fmt):
        fmt.set_font_name('Arial')
        fmt.set_font_size(12)
        fmt.set_num_format('#,##0.00')
        fmt.set_top(1)
        fmt.set_bottom(1)
        fmt.set_left(1)
        fmt.set_right(1)

    def set_table_header(self, fmt):
        self.set_table_body(fmt)
        fmt.set_bold()
        fmt.set_font_size(15)
        fmt.set_align('center')

    def create_footer(self):
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        fmt.set_align('right')
        underline = self.workbook.add_format()
        underline.set_bottom(1)
        self.worksheet.write('B36', 'cash/cheque#: ', fmt)
        self.worksheet.write('C36', '', underline)
        self.worksheet.write('D36', 'date: ', fmt)
        self.worksheet.write('E36', '', underline)
        self.worksheet.write('B37', 'Bank/Branch: ', fmt)
        self.worksheet.write('C37', '', underline)
        self.worksheet.write('B38', 'Receive by: ', fmt)
        self.worksheet.write('C38', '', underline)

class Invoice(object):
    @staticmethod
    def get_file_name(id, timestamp):
        return 'inv_' + str(id) + '_'+ str(timestamp).replace('.','_')

    def __init__(self, filename, logo):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.logo = logo
        self.styles = {}

    def create(self):
        self.workbook.set_size(1000, 1200)
        self.styles['bold'] = self.workbook.add_format({'bold': True})
        self.worksheet = self.workbook.add_worksheet()
        self.no_row = 7
        self.receipt_row = self.no_row + 2
        self.desc_row = self.receipt_row + 4
        A4 = 9
        self.worksheet.set_paper(A4)
        self.worksheet.fit_to_pages(1, 1)
        self.worksheet.print_area('A1:E38')
        self.create_logo()
        self.create_style_school_name()
        self.create_style_sub_title()
        self.create_title()
        #self.create_address()
        #self.create_for_invoice()
        #self.create_class()
        #self.create_table()
        #self.create_body()
        #self.create_footer()
        self.close()

    def close(self):
        self.workbook.close()

    def create_logo(self):
        self.worksheet.insert_image('A1', self.logo, {'x_scale': 0.95, 'y_scale': 0.81})

    def create_style_school_name(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_font_color('#006737')
        fmt.set_align('center')
        fmt.set_font_name('Times')
        self.worksheet.write('C2', 'RUAM RUDEE LEARNING CENTRE', fmt)

    def create_style_sub_title(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_align('center')
        fmt.set_font_size(15)
        fmt.set_font_name('Times')
        self.worksheet.write('C3', 'Nursery, Pre-School and Elementary', fmt)

    def create_title(self):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(20)
        fmt.set_underline()
        fmt.set_font_name('Arial')
        fmt.set_align('center')
        self.worksheet.write('C%s'%self.title_row, 'INVOICE', fmt)
