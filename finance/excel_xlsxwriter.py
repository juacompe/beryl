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
        self.line_row = 7
        self.before_table_row = 7
        self.title_row = self.before_table_row + 2
        self.desc_row = self.title_row + 8
        self.after_table_row = self.desc_row + 22
        A4 = 9
        self.worksheet.set_paper(A4)
        self.worksheet.fit_to_pages(1, 1)
        self.worksheet.set_column('A:A', 6)
        self.worksheet.set_column('B:B', 19)
        self.worksheet.set_column('C:C', 59)
        self.worksheet.set_column('E:E', 19)
        self.worksheet.print_area('A1:E%s' % self.get_last_row())
        self.create_logo()
        self.create_style_school_name()
        self.create_style_sub_title()
        self.create_title()
        self.create_address()
        self.create_content_before_table()
        self.create_class()
        self.create_content_before_table()
        self.create_table()
        self.create_content_after_table()
        self.create_footer()
        self.close()

    def create_logo(self):
        self.worksheet.insert_image('A1', self.logo, {'x_scale': 0.95, 'y_scale': 0.81})

    def create_style_school_name(self):
        self.worksheet.write('C1', 'RC INTERNATIONAL SCHOOL', self.create_style_school_with_size(20))
        self.worksheet.write('C2', 'RUAM RUDEE LEARNING CENTRE', self.create_style_school_with_size(18))

    def create_style_school_with_size(self, size):
        fmt = self.workbook.add_format()
        fmt.set_bold()
        fmt.set_font_size(size)
        fmt.set_font_color('#006737')
        fmt.set_align('center')
        fmt.set_font_name('Times')
        return fmt

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
        self.worksheet.write('C%s'%self.title_row, self.get_title(), fmt)

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
        double_bottom_lines = self.workbook.add_format()
        double_bottom_lines.set_bottom(6)
        self.worksheet.write('A%s'%self.line_row, '', double_bottom_lines)
        self.worksheet.write('B%s'%self.line_row, '', double_bottom_lines)
        self.worksheet.write('C%s'%self.line_row, '', double_bottom_lines)
        self.worksheet.write('D%s'%self.line_row, '', double_bottom_lines)
        self.worksheet.write('E%s'%self.line_row, '', double_bottom_lines)

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
        total_row = self.desc_row + 21
        self.set_table_header(total)
        self.worksheet.merge_range('A%s:D%s'%(total_row, total_row), 'TOTAL   (Baht)', total)
        self.worksheet.write('E%s'%total_row, self.total, header)

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

    def create_content_before_table(self):
        receive_with_thanks_row = self.before_table_row+3
        address_row = self.before_table_row+5
        self.worksheet.write('A%s'%receive_with_thanks_row, 'Receive with thanks from:')
        self.worksheet.set_row(receive_with_thanks_row-1, 40)
        self.worksheet.write('A%s'%(self.before_table_row+4), 'Name of student:')
        self.worksheet.write('A%s'%address_row, 'Address:')
        self.worksheet.set_row(address_row-1, 40)

    def create_content_after_table(self):
        self.worksheet.set_row(self.after_table_row-1, 40)
        self.worksheet.write('A%s'%self.after_table_row, 'Thank you very much for your kind support.')
        self.worksheet.set_row(self.after_table_row, 40)
        self.worksheet.write('A%s'%(self.after_table_row+1), 'Mrs.Chutamas Pattharamalai')
        self.worksheet.write('A%s'%(self.after_table_row+2), 'President')

    def close(self):
        self.workbook.close()

    def set_invoice_number(self, i):
        self.invoice_number = i

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

    def set_items(self, items):
        self.items = items

    def set_total(self, t):
        self.total = t


class ReceiptSheet(Spreadsheet):
    def set_receipt_id(self, i):
        self.receipt_id = i

    def set_date(self, d):
        self.timestamp = d

    @staticmethod
    def get_file_name(receipt_id, timestamp):
        return 'rep_' + str(receipt_id) + '_'+ str(timestamp).replace('.','_')

    @staticmethod
    def get_file_path(receipt_id, timestamp):
        filename = ReceiptSheet.get_file_name(receipt_id, timestamp)
        return os.path.join(tempfile.mkdtemp(), filename)

    def get_binary_content(self):
        fh = open(self.filename, 'rb')
        resp = fh.read()
        fh.close()
        return resp

    def get_title(self):
        return 'RECEIPT'

    def get_last_row(self):
        return self.after_table_row + 5

    def create_content_before_table(self):
        self.create_for_invoice()

    def create_for_invoice(self):
        no_row = self.before_table_row + 1 
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        # fmt.set_bg_color('#cccccc')
        fmt.set_align('right')
        left = self.workbook.add_format()
        left.set_font_name('Arial')
        left.set_align('left')
        self.worksheet.write('D%s'%(no_row+0), 'for invoice (optional): ', fmt)
        self.worksheet.write('E%s'%(no_row+0), self.invoice_number, left)
        self.worksheet.write('A%s'%(no_row+0), 'No.')
        self.worksheet.write('B%s'%(no_row+0), self.receipt_id, left)
        self.worksheet.write('A%s'%(no_row+1), 'Date.')
        self.worksheet.write('B%s'%(no_row+1), self.timestamp, left)

    def create_class(self):
        fmt = self.workbook.add_format()
        fmt.set_align('right')
        fmt.set_font_name('Arial')
        fmt.set_bold()
        self.worksheet.write('D%s'%(self.desc_row-1), 'Class :', fmt)

    def create_footer(self):
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        fmt.set_align('right')
        underline = self.workbook.add_format()
        underline.set_bottom(1)
        footer_row = self.after_table_row+3
        self.worksheet.write('B%s'%(footer_row), 'cash/cheque#: ', fmt)
        self.worksheet.set_row(footer_row-1, 40)
        self.worksheet.write('C%s'%(footer_row), '', underline)
        self.worksheet.write('D%s'%(footer_row), 'date: ', fmt)
        self.worksheet.write('E%s'%(footer_row), '', underline)
        self.worksheet.write('B%s'%(footer_row+1), 'Bank/Branch: ', fmt)
        self.worksheet.write('C%s'%(footer_row+1), '', underline)
        self.worksheet.write('B%s'%(footer_row+2), 'Receive by: ', fmt)
        self.worksheet.write('C%s'%(footer_row+2), '', underline)


class InvoiceSheet(Spreadsheet):
    @staticmethod
    def get_file_name(id, timestamp):
        return 'inv_' + str(id) + '_'+ str(timestamp).replace('.','_')

    def get_title(self):
        return 'INVOICE' 

    def create_content_before_table(self):
        row = self.title_row + 1
        fmt = self.create_style_body('left')
        bold = self.create_style_body('left')
        bold.set_bold()
        self.worksheet.write('A%s'%(row), 'Dear Parent,', fmt)
        self.worksheet.write('A%s'%(row+1), "This is a break down of the payment of your child's school fees. ", fmt)
        self.worksheet.write('A%s'%(row+2), 'Please do not lose this form and return it together with the tuition fee on or before the due date.', bold)
        self.worksheet.write('A%s'%(row+3), 'School Term :', bold)
        self.term = 'Second Term   (Jan 06, 2011 to Apr 1, 2011)'
        self.worksheet.write('C%s'%(row+3), self.term, fmt)
        self.worksheet.write('A%s'%(row+4), 'Last Fee Due Date : ', bold)
        self.worksheet.write('C%s'%(row+4), self.deadline, fmt)
        self.worksheet.write('A%s'%(row+5), "Child's Name : ", bold)
        self.worksheet.write('C%s'%(row+5), self.child_name, fmt)
        self.worksheet.write('D%s'%(row+5), 'Class :', bold)
        self.worksheet.write('E%s'%(row+5), self.class_room, fmt)

    def create_class(self):
        pass

    def create_footer(self):
        head = self.create_style_footer_align('left')
        head.set_underline()
        fmt = self.create_style_footer_align('left')
        bullet = self.create_style_footer_align('right')
        bullet.set_align('top')
        footer_row = self.after_table_row+4
        self.worksheet.merge_range('A%s:E%s'%(footer_row, footer_row), 'Please take note of the following remarks:', head)
        self.worksheet.write('A%s'%(footer_row+1), '1.', bullet)
        self.worksheet.merge_range('B%s:E%s'%(footer_row+1, footer_row+1), "No refund or reductions can be made in any fees for child's illness, temporary absence from school or change of plans.", fmt)
        self.worksheet.write('A%s'%(footer_row+2), '2.', bullet)
        self.worksheet.merge_range('B%s:E%s'%(footer_row+2, footer_row+2), 'Please be notified that the penalty of 100 Baht per day will be charged for late payment.', fmt)
        self.worksheet.write('A%s'%(footer_row+3), '3.', bullet)
        self.worksheet.merge_range('B%s:E%s'%(footer_row+3, footer_row+3), 'Payment should be made in Thai Baht by cash or cheque payable to "RUAM RUDEE LEARNING CENTRE" or "RC INTERNATIONAL SCHOOL" crossed "ACCOUNT PAYEE ONLY" and the words "OR BEARER" deleted.', fmt)
        self.worksheet.set_row(footer_row+3-1, 25)
        self.worksheet.write('A%s'%(footer_row+4), '4.', bullet)
        self.worksheet.merge_range('B%s:E%s'%(footer_row+4, footer_row+4), 'A pupil is not officially enrolled until payment of fees.  As such, the pupil may be suspended from attending classes.', fmt)

    def create_style_footer_align(self, align):
        fmt = self.create_style_body(align)
        fmt.set_font_size(9)
        fmt.set_bold()
        fmt.set_text_wrap()
        return fmt

    def create_style_body(self, align):
        fmt = self.workbook.add_format()
        fmt.set_font_name('Arial')
        fmt.set_align(align)
        return fmt
        
    def get_last_row(self):
        return self.after_table_row + 10 

    def set_child_name(self, cn):
        self.child_name = cn

    def set_deadline(self, d):
        self.deadline = d

    def set_class_room(self, c):
        self.class_room = c
