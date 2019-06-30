from django.test import TestCase
from finance.excel_xlsxwriter import Spreadsheet

class TestSpreadsheet(TestCase):
    def test_create(self):
        create_sample_receipt()

def create_sample_receipt():
    logo = '/Users/juacompe/Projects/github.com/juacompe/beryl/media/rcis_logo.png'
    timestamp = '2019-06-30 11:47:32.832423'
    receipt_id = 2
    print Spreadsheet.get_file_name(receipt_id, timestamp)
    filename = "/tmp/receipt.xlsx"
    s = Spreadsheet(filename, logo)
    s.set_invoice_number(1)
    s.set_receipt_id(receipt_id)
    s.set_date(timestamp)
    s.set_items([
        MockItem('Fees',  58000),
        MockItem('Instructional Materials', 12000),
    ])
    s.set_total(70000)
    s.create()

class MockItem(object):
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
