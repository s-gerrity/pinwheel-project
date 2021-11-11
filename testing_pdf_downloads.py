import download_form_pdfs
import unittest
from io import StringIO
from unittest.mock import patch



################ TESTS ##########

def answerReturn():
    ans = input('enter yes or no')
    print(ans)
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'


class MyTestCase(unittest.TestCase):
    def runTest(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            answerReturn()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)
    
    def testNo(self):
        self.runTest('you entered no', 'you entered no')

    def testYes(self):
        self.runTest('you entered yes', 'you entered yes')

if __name__ == '__main__':
    unittest.main()



# def run_test(testValue, expectedResult, description):
#     print(description)
#     if testValue == expectedResult:
#         print('    ✅ Test passed')
#     else:
#         print('    ❌ Test failed!')


# sample_tax_form_name = "Form W-2"
# not_found_start_year = 1935
# not_found_end_year = 1937
# found_start_year = 2017
# found_end_year = 2020
# found_page_two_start_year = 2012
# found_page_two_end_year = 2016
# beginning_available_end_year = 1954


# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, not_found_start_year, not_found_end_year), 'There are no PDF downloads for those years', 'Input years are neither available for the form')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_start_year, found_end_year), 'Downloads completed', 'Input years both available and on one page')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_page_two_start_year, found_end_year), 'Downloads completed', 'Start year on diff page, all pdf"s available')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_page_two_start_year, found_page_two_end_year), 'Downloads completed', 'Start and end years both available and on page two')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, not_found_start_year, beginning_available_end_year), 'Downloads completed', 'Only one year available')

