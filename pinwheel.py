
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

tax_form_names = ["Form W-2", "Form 1095-C"]
dict_for_data = {}

# TODO: break function into smaller functions
# make soup, grab data, loop through data to label key: value pairs, mix and max, 
# turn into json, pagenation

def data_for_forms(tax_form_names):
    # TODO: iterate through pages somehow
    for form_to_check in tax_form_names:
        print(form_to_check, "form_to_check")
        new_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_to_check.lower() + "&criteria=formNumber&resultsPerPage=25&isDescending=false"

        page = requests.get(new_URL)

        # object that takes page.content, which is the HTML content you scraped, as its input
        soup = BeautifulSoup(page.content, "html.parser")

        # this creats an "iterable" to loop through all results
        results = soup.find("div", class_="picklistTable")
        
        form_data = results.find_all("tr", class_=["even", "odd"])
        all_form_years = []

        for form in form_data:
            product_number = form.find("td", class_="LeftCellSpacer")

            if product_number.text.strip() == form_to_check:
                dict_for_data['Product Number'] = product_number.text.strip()
                form_title = form.find("td", class_="MiddleCellSpacer")
                form_year = form.find("td", class_="EndCellSpacer")
                
                # collect applicable years in a list to sort the min and max later
                all_form_years.append(form_year.text.strip())
                dict_for_data['Title'] = form_title.text.strip()        
    
        dict_for_data['Minimum Year'] = min(all_form_years)
        dict_for_data['Maximum Year'] = max(all_form_years)

        json_object = json.dumps(dict_for_data, indent = 4) 
        return json_object




print(data_for_forms(tax_form_names))


# sample download file urls
# https://www.irs.gov/pub/irs-prior/fw2p--1990.pdf
# https://www.irs.gov/pub/irs-prior/f1099c--2021.pdf

