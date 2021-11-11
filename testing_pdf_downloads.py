import download_form_pdfs
from test_base import set_keyboard_input, get_display_output 


################ TESTS ##########

valid_form_formatting = "Form W-2"
lowercase_form_input = "form w-2"
uppercase_form_input = "FORM W-2"
no_dash_form_input = "Form W2"
misspelled_form_input = "fomr w-2"
not_found_start_year = 1935
not_found_end_year = 1937
found_start_year = 2017
found_end_year = 2020
found_page_two_start_year = 2012
found_page_two_end_year = 2016
beginning_available_end_year = 1954

# def name_and_animal():
#     name = input('>> Tell me your name: ')
#     animal = input('>> What is your favorite animal? ')
    
#     print('Hi {}! You like the {}.'.format(name, animal))


# def test_1():
#     set_keyboard_input(['Stinky', 'Snake'])

#     name_and_animal()

#     output = get_display_output()

#     assert output == ['>> Tell me your name: ', 
#                       '>> What is your favorite animal? ',
#                       'Hi Stinky! You like the Snake.']

# def test_2():

#     set_keyboard_input(['sink', 'nail'])

#     name_and_animal()

#     output = get_display_output()

#     assert output == ['>> Tell me your name: ', 
#                       '>> What is your favorite animal? ',
#                       'Hi sink! You like the nail.']

        
def test_valid_years_and_formatting():
    """Test checks for valid years and valid spelling and formatting for
    form name."""

    set_keyboard_input([valid_form_formatting, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


def test_next_page_year_grouping():
    """Test checks for valid years that start on one page and require pagination
    to collect all PDFs. Valid spelling and formatting for form name."""

    set_keyboard_input([valid_form_formatting, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


def test_not_all_years_available():
    """Checks for years where only some have PDFs to download. Valid spelling and formatting for form name."""

    set_keyboard_input([valid_form_formatting, not_found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]

                    
def test_lowercase_form_input():
    """Form input is all lowercase. URL function will correct to lowercase as well. Valid
    years to download."""

    set_keyboard_input([lowercase_form_input, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


def test_uppercase_form_input():
    """Form input is all lowercase. URL function will correct to lowercase as well. Valid
    years to download."""

    set_keyboard_input([uppercase_form_input, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


def test_missing_dash_form_input():
    """Form input is all lowercase. URL function will correct to lowercase as well. Valid
    years to download."""

    set_keyboard_input([no_dash_form_input, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]


def test_misspelled_form_input():
    """Form input is all lowercase. URL function will correct to lowercase as well. Valid
    years to download."""

    set_keyboard_input([misspelled_form_input, found_start_year, found_end_year])

    print(download_form_pdfs.download_pdfs_and_save())

    output = get_display_output()

    assert output == [">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ",
                      ">> What year would you like the downloads to start at? ",
                      ">> Up until which year should be included? ",
                      "Downloads completed"]







# if __name__ == '__main__':
    # test_1()
    # test_2()



# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, not_found_start_year, not_found_end_year), 'There are no PDF downloads for those years', 'Input years are neither available for the form')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_start_year, found_end_year), 'Downloads completed', 'Input years both available and on one page')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_page_two_start_year, found_end_year), 'Downloads completed', 'Start year on diff page, all pdf"s available')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, found_page_two_start_year, found_page_two_end_year), 'Downloads completed', 'Start and end years both available and on page two')
# run_test(download_form_pdfs.download_pdfs_and_save(sample_tax_form_name, not_found_start_year, beginning_available_end_year), 'Downloads completed', 'Only one year available')

