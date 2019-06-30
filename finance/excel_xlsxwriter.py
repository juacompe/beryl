# -*- coding: utf-8 -*-
import xlsxwriter

def create_sample_receipt():
    logo = '/Users/juacompe/Projects/github.com/juacompe/beryl/media/rcis_logo.png'
    filename = "/tmp/receipt.xlsx"
    s = Spreadsheet(filename, logo)
    s.close()

class Spreadsheet(object):
    def __init__(self, filename, logo):
        self.workbook = xlsxwriter.Workbook(filename)
        self.logo = logo
        self.styles = {}
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
        self.write_body()
        self.create_footer()

    def close(self):
        self.workbook.close()

    def write_body(self):
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
        self.worksheet.insert_image('A1', self.logo, {'x_scale': 1, 'y_scale': 0.86})

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
        self.worksheet.write('D7', 'for invoice (optional): ', fmt)
        self.worksheet.write('A%s'%(self.no_row+0), 'No.')
        self.worksheet.write('A%s'%(self.no_row+1), 'Date.')

    def create_class(self):
        fmt = self.workbook.add_format()
        fmt.set_align('right')
        fmt.set_font_name('Arial')
        fmt.set_bold()
        self.worksheet.write('D%s'%(self.desc_row-1), 'Class :', fmt)

    def create_table(self):
        fmt = self.workbook.add_format()
        self.set_table_header(fmt)
        self.worksheet.merge_range('A%s:D%s' % (self.desc_row, self.desc_row), 'Description', fmt)
        self.worksheet.write('E%s'%self.desc_row, u'฿  Amount', fmt)
        def desc(row):
            self.worksheet.merge_range('A%s:D%s'%(row, row), '', fmt)
        def amount(row):
            self.worksheet.write('E%s'%row, '', fmt)
        map(desc,range(self.desc_row+1, 34))
        map(amount,range(self.desc_row+1, 35))
        total = self.workbook.add_format()
        self.set_table_header(total)
        self.worksheet.merge_range('A34:D34', 'TOTAL   (Baht)', total)

    def set_table_header(self, fmt):
        fmt.set_font_name('Arial')
        fmt.set_bold()
        fmt.set_font_size(15)
        fmt.set_align('center')
        fmt.set_top(1)
        fmt.set_bottom(1)
        fmt.set_left(1)
        fmt.set_right(1)

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
