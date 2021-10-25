# start by only pulling the product num and title, then returning JSON

import requests
import json
from bs4 import BeautifulSoup

# list of all tax forms we need to pull
tax_form_names = ["Form W-2", "Form 1095-C"]
dict_for_data = {}

##### HELPER FUNCTION


# def find_num_of_pages_to_search():



###### MAIN FUNCTION




def data_for_forms(tax_form_names):
    # TODO: iterate through pages somehow
    for form_to_check in tax_form_names:
        new_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_to_check.lower() + "&criteria=formNumber&resultsPerPage=25&isDescending=false"

        page = requests.get(new_URL)

        # object that takes page.content, which is the HTML content you scraped, as its input
        soup = BeautifulSoup(page.content, "html.parser")

        # this creats an "iterable" to loop through all results
        results = soup.find("div", class_="picklistTable")
        
        # print(results.prettify())

        form_data = results.find_all("tr", class_=["even", "odd"])
        all_form_years = []

        for form in form_data:
            # print(form.prettify(), end="\n"*2)
            checker = False
            product_number = form.find("td", class_="LeftCellSpacer")

            if product_number.text.strip() == form_to_check and checker == False:
                dict_for_data['Product Number'] = product_number.text.strip()
                checker = True
                form_title = form.find("td", class_="MiddleCellSpacer")
                form_year = form.find("td", class_="EndCellSpacer")
                
                # collect applicable years in a list to sort the min and max later
                all_form_years.append(form_year.text.strip())
                dict_for_data['Title'] = form_title.text.strip()        
    
        dict_for_data['Minimum Year'] = min(all_form_years)
        dict_for_data['Maximum Year'] = max(all_form_years)

        json_object = json.dumps(dict_for_data, indent = 4) 
        print(json_object)




data_for_forms(tax_form_names)

