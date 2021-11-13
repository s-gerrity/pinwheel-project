import download_form_pdfs
from test_base import set_keyboard_input, get_display_output 


################ TEST VARIABLES ##########

valid_form_formatting = "Form W-2"
lowercase_form_input = "form w-2"
uppercase_form_input = "FORM W-2"
no_dash_form_input = "Form W2"
misspelled_form_input = "fomr w-2"
not_found_start_year = "1935"
not_found_end_year = "1937"
start_year_valid = "2017"
end_year_valid = "2020"
found_page_two_start_year = "2012"
found_page_two_end_year = "2016"
beginning_available_end_year = "1954"
nonsense_year_1 = "555"
nonsense_year_2 = "78"
year_string = "khjkasd"

# TODO: Test what happens when no entry added.
# TODO: Handle 2 digit year inputs 

########### TESTS TO CONFIRM ERRORS #############

######## HELPER FUNCTION YEARS LOGIC: NO PDFS FOUND FOR YEARS ################


def no_pdfs_output_test():
    """Output for when the user does not receive results from their query due to user error or because
    the IRS does not have PDFs available for those years."""

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "There are no PDF downloads for those years. If you think this is an error, please check for typos."]

############ TESTS FOR NO PDFS FOUND #################


def test_years_backward():
    """Tests first year input as lower than second year input; form name valid. Ex: year range 2020 - 2016
    instead of 2016 - 2020."""

    set_keyboard_input([valid_form_formatting, end_year_valid, start_year_valid])

    return no_pdfs_output_test()
    

def test_years_invalid():
    """Years are too short (Ex: 33) or nonexistent (Ex: 5543); form name valid."""

    set_keyboard_input([valid_form_formatting, nonsense_year_1, nonsense_year_2])

    return no_pdfs_output_test()



########## HELPER FUNCTION YEARS TYPE: YEARS INPUTS 4 NUMS IN A STRING #########


def year_not_nums_output_test():
    """Years input must be 4 nums that is taken in as a string."""

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Invalid year inputs. Must be 4 numbers for both entires."]


################ TESTS FOR YEARS NUMS IN STRING ##############


def test_years_string_of_nums_input():
    """First year entry are letter characters, second is nums in a string."""

    set_keyboard_input([valid_form_formatting, year_string, end_year_valid])

    return year_not_nums_output_test()


########### HELPER FUNCTION FORM TEST: NO RESULTS INVALID FORM INPUT ##############


def error_form_name_output_test():
    """Result for when the form name causes no results to produce from the site."""

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "There are no results that match your entry. Please check for typos and that you are using the correct form name."]


################ TESTS FOR FORM NAME INVALID ################


def test_misspelled_form_input():
    """Typo or misspelling in form name input will produce no results regardless if
    years are valid."""

    set_keyboard_input([misspelled_form_input, start_year_valid, end_year_valid])

    return error_form_name_output_test()



############ TESTS TO CONFIRM CORRECTNESS #############

############ HELPER FUNCTION FOR DOWNLOADS COMPLETE ###############



def download_complete_output_test():
    """When form name and years are entered correctly the utilities will download correctly,
    giving an output of 'Downloads completed"."""

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


########### TESTS FOR DOWNLOAD COMPLETE #############


def test_missing_dash_form_input():
    """Form input is all lowercase. URL function will correct to lowercase as well. Valid
    years to download."""

    set_keyboard_input([no_dash_form_input, start_year_valid, end_year_valid])

    return download_complete_output_test()


def test_valid_inputs():
    """Both form and years are valid."""

    set_keyboard_input([valid_form_formatting, start_year_valid, end_year_valid])

    return download_complete_output_test()


def test_next_page_year_grouping():
    """Test pagination. Valid inputs. URL shows 200 items per page."""

    set_keyboard_input([valid_form_formatting, start_year_valid, end_year_valid])

    return download_complete_output_test()


def test_not_all_years_available():
    """Checks for years where only some have PDFs to download. Form name input valid."""

    set_keyboard_input([valid_form_formatting, not_found_start_year, end_year_valid])

    return download_complete_output_test()

                    
def test_lowercase_form_input():
    """Form input is all lowercase. URL function will correct to lowercase. Valid
    years input."""

    set_keyboard_input([lowercase_form_input, start_year_valid, end_year_valid])

    return download_complete_output_test()


def test_uppercase_form_input():
    """Form input entered as uppercase. URL function will correct to lowercase. Valid
    years input."""

    set_keyboard_input([uppercase_form_input, start_year_valid, end_year_valid])

    return download_complete_output_test()



