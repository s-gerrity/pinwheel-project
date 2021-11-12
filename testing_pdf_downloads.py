import download_form_pdfs
from test_base import set_keyboard_input, get_display_output 


################ TEST VARIABLES ##########

valid_form_formatting = "Form W-2"
lowercase_form_input = "form w-2"
uppercase_form_input = "FORM W-2"
no_dash_form_input = "Form W2"
misspelled_form_input = "fomr w-2"
not_found_start_year = 1935
not_found_end_year = 1937
start_year_valid = 2017
end_year_valid = 2020
found_page_two_start_year = 2012
found_page_two_end_year = 2016
beginning_available_end_year = 1954
nonsense_year_1 = 555
nonsense_year_2 = 78


############## TESTS FOR DOWNLOAD COMPLETED ###################


# def test_valid_years_and_formatting():
#     """Test checks for valid years and valid spelling and formatting for
#     form name."""

#     set_keyboard_input([valid_form_formatting, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]


# def test_next_page_year_grouping():
#     """Test checks for valid years that start on one page and require pagination
#     to collect all PDFs. Valid spelling and formatting for form name."""

#     set_keyboard_input([valid_form_formatting, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]


# def test_not_all_years_available():
#     """Checks for years where only some have PDFs to download. Valid spelling and formatting for form name."""

#     set_keyboard_input([valid_form_formatting, not_found_start_year, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]

                    
# def test_lowercase_form_input():
#     """Form input is all lowercase. URL function will correct to lowercase as well. Valid
#     years to download."""

#     set_keyboard_input([lowercase_form_input, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]


# def test_uppercase_form_input():
#     """Form input is all lowercase. URL function will correct to lowercase as well. Valid
#     years to download."""

#     set_keyboard_input([uppercase_form_input, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]


# def test_missing_dash_form_input():
#     """Form input is all lowercase. URL function will correct to lowercase as well. Valid
#     years to download."""

#     set_keyboard_input([no_dash_form_input, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "Downloads completed"]


#################### TESTS THAT PRODUCE ERRORS ##############


# def test_misspelled_form_input():
#     """Form input is all lowercase. URL function will correct to lowercase as well. Valid
#     years to download."""

#     set_keyboard_input([misspelled_form_input, start_year_valid, end_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "There are no results that match your entry. Please check for typos and that you are using the correct form name."]


# def test_years_invalid():
#     """Years incorrect; form name valid."""

#     set_keyboard_input([valid_form_formatting, nonsense_year_1, nonsense_year_2])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "There are no PDF downloads for those years. If you think this is an error, please check for typos."]

# def test_years_backward():
#     """Tests for first year input to be lower than second year input; form name valid."""

#     set_keyboard_input([valid_form_formatting, end_year_valid, start_year_valid])

#     print(download_form_pdfs.download_pdfs_and_save())

#     output = get_display_output()

#     assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
#                       ">> What year would you like the downloads to start at? ",
#                       ">> Up until which year should be included? ",
#                       "There are no PDF downloads for those years. If you think this is an error, please check for typos."]

#############

# pseudocode
# a bunch of functions that call the same helper function 
# helper contains the associated output


def output_test():

    # set_keyboard_input([valid_form_formatting, end_year_valid, start_year_valid])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "There are no PDF downloads for those years. If you think this is an error, please check for typos."]


def test_years_backward():
    """Tests for first year input to be lower than second year input; form name valid."""

    set_keyboard_input([valid_form_formatting, end_year_valid, start_year_valid])

    return output_test()
    
    
    # print(download_form_pdfs.download_pdfs_and_save())

    # output = get_display_output()

    # assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
    #                   ">> What year would you like the downloads to start at? ",
    #                   ">> Up until which year should be included? ",
    #                   "There are no PDF downloads for those years. If you think this is an error, please check for typos."]


