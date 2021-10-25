# start by only pulling the product num and title, then returning JSON

import requests
import json
from bs4 import BeautifulSoup

# list of all tax forms we need to pull
tax_form_names = ["Form+W-2"]
dict_for_data = {}

##### HELPER FUNCTION

def collect_all_form_years(all_form_years_list, even_form_data, odd_form_data):
    for form in even_form_data:
        form_year = form.find("td", class_="EndCellSpacer")
        all_form_years.append(form_year.text.strip())
    for form in odd_form_data:
        form_year = form.find("td", class_="EndCellSpacer")
        all_form_years.append(form_year.text.strip())

    return all_form_years_list


# TODO: iterate through pages somehow
for item in tax_form_names:
    new_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=25&sortColumn=sortOrder&value=" + item + "&criteria=formNumber&resultsPerPage=25&isDescending=false"

    page = requests.get(new_URL)

    # object that takes page.content, which is the HTML content you scraped, as its input
    soup = BeautifulSoup(page.content, "html.parser")

    # this creats an "iterable" to loop through all results
    results = soup.find("div", class_="picklistTable")
    
    # print(results.prettify())

    # TODO: need to include class odd
    even_form_data = results.find_all("tr", class_="even")
    odd_form_data = results.find_all("tr", class_="odd")

    for form in even_form_data[:1]:
        # print(form.prettify(), end="\n"*2)
        product_number = form.find("td", class_="LeftCellSpacer")
        form_title = form.find("td", class_="MiddleCellSpacer")
        # print(product_number.text.strip())
        # print(form_title.text.strip())
        # print(form_year.text.strip())

        dict_for_data['Product Number'] = product_number.text.strip()
        dict_for_data['Title'] = form_title.text.strip()
    
    all_form_years = []

    all_form_years_list = collect_all_form_years(all_form_years, even_form_data, odd_form_data)
    print(all_form_years_list)

    dict_for_data['Minimum Year'] = min(all_form_years)
    dict_for_data['Maximum Year'] = max(all_form_years)

json_object = json.dumps(dict_for_data, indent = 4) 
print(json_object)






