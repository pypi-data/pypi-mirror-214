import unittest
import os
from Library.main import OCR

class TestOCR(unittest.TestCase):
    def setUp(self):
        self.ocr = OCR()
        self.test_image_path = '/Users/woojaejo/Desktop/gaon/OCR/scantest.png'  # Update this path
        self.test_pdf_path = '/Users/woojaejo/Desktop/gaon/OCR/T4.pdf'  # Update this path

    def test_process_image(self):
        result = self.ocr.process(self.test_image_path)

        expected_result = '{"Employment Income": "504831", "Income Tax Deducted": "369.07", "CPPs Contribution": "209.91", "EI Earnings": "5047.45", "QPP Contributions": "", "Pensionable Earnings": "", "EI Premiums": "831.79", "Union Dues": "", "RPP Contribution": "", "Charitable Donations": "", "Pension Adjustment": "", "RPP or DPSP Registration Number": "", "PPIP Premiums": "", "PPIP Earnings": "", "Employers Name": "TD BANK 66 WELLINGTON ST W28TH FLTD E TORONTO ON M5K 1A2", "Employment account number": "", "SIN": "937 619 997", "Year": "2018", "Province": "ON", "Employment Code": "", "Employee Name": "lee", "Address": "58 ORCHARD VIEW BOULEVARD UNIT 413, TORONTO, ON M4R 0A2", "CPP/QPP": "", "EI": "", "PPIP": "", "Box-Case1": "40", "Amount1": "86", "Box-Case2": "", "Amount2": "", "Box-Case3": "", "Amount3": ""}'

        self.assertEqual(result, expected_result)

    def test_process_pdf(self):
        result = self.ocr.process(self.test_pdf_path)
        expected_result = '{"Employment Income": "504831", "Income Tax Deducted": "369.07", "CPPs Contribution": "209.91", "EI Earnings": "5047.45", "QPP Contributions": "", "Pensionable Earnings": "5048.31", "EI Premiums": "", "Union Dues": "", "RPP Contribution": "", "Charitable Donations": "", "Pension Adjustment": "", "RPP or DPSP Registration Number": "", "PPIP Premiums": "", "PPIP Earnings": "", "Employers Name": "D BANK 6 WELLINGTON ST W28TH FLTD E ORONTO ON M5K 1A2", "Employment account number": "", "SIN": "937 619 997", "Year": "", "Province": "DN", "Employment Code": "", "Employee Name": "EE  JUN", "Address": "8 ORCHARD VIEW BOULEVARD UNIT 413, TORONTO, ON M4R 0A2", "CPP/QPP": "", "EI": "", "PPIP": "", "Box-Case1": "", "Amount1": "", "Box-Case2": "", "Amount2": "", "Box-Case3": "", "Amount3": ""}'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
