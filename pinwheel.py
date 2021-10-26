
import requests
import json
from bs4 import BeautifulSoup

# Take in a list of tax form names

# Search the website for the tax forms

# Return: JSON of the "Product Number", the "Title", and the maximum and minimum 
# years the form is available for download.

# Return: download all PDFs available within the years range specified. The 
# downloaded PDFs should be downloaded to a subdirectory under your script's main 
# directory with the name of the form, and the file name should be the "Form Name - Year"

# click (cli)
# optional arg parse - stnd py package (cli)

# parse website with bs3
# to dl pdf file use python requests, remember to use flags

tax_forms_to_check = ["Form W-2", "Form 1095-C"]


# TODO: pagenation

def locate_data_on_page(soup):

    # this creats an "iterable" to loop through all results
    results = soup.find("div", class_="picklistTable")

    form_data = results.find_all("tr", class_=["even", "odd"])

    return form_data


def collect_tax_form_details(form_data, form_to_check):
    dict_for_data = {}

    for form in form_data:
        product_number = form.find("td", class_="LeftCellSpacer")

        if product_number.text.strip() == form_to_check:
            dict_for_data['Product Number'] = product_number.text.strip()
            form_title = form.find("td", class_="MiddleCellSpacer")

            # collect applicable years in a list to sort the min and max later
            dict_for_data['Title'] = form_title.text.strip()

    return dict_for_data

def collect_tax_years(form_data, form_to_check):
    all_form_years = {'Years': []}

    for form in form_data:
            product_number = form.find("td", class_="LeftCellSpacer")

            if product_number.text.strip() == form_to_check:
                form_year = form.find("td", class_="EndCellSpacer")
                all_form_years['Years'].append(form_year.text.strip())


    return all_form_years


def get_min_max_years(all_form_years, dict_for_data):

    dict_for_data['Minimum Year'] = min(all_form_years['Years'])
    dict_for_data['Maximum Year'] = max(all_form_years["Years"])

    return dict_for_data


def append_to_main_list_as_json(dict_with_form_data, tax_form_info):

    tax_form_info.append(dict_with_form_data)

    return tax_form_info


def get_tax_info(tax_forms_to_check):
    tax_form_info = []

    for form_to_check in tax_forms_to_check:
        url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_to_check.lower() + "&criteria=formNumber&resultsPerPage=25&isDescending=false"

        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        form_data = locate_data_on_page(soup)
        dict_for_data = collect_tax_form_details(form_data, form_to_check)
        all_form_years = collect_tax_years(form_data, form_to_check)
        dict_with_form_data = get_min_max_years(all_form_years, dict_for_data)
        tax_form_info = append_to_main_list_as_json(dict_with_form_data, tax_form_info)

    print(json.dumps(tax_form_info, indent = 4))
    
    return print("All forms have been checked")


get_tax_info(tax_forms_to_check)