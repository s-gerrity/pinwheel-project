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

        # links = soup.find_all('a')
        # # for link in links:
        # #     link_url = link["href"]
        # #     if 'pdf' in link_url:
        # #         print(link_url)
        # i = 0
        # for link in links[:23]:
        #     if ('.pdf' in link.get('href', [])):
        #         i += 1
        #         print("Downloading file: ", i)
  
        # # Get response object for link
        #         response = requests.get(link.get('href'))
        #         print(link.get('href'))
        #         pdf = open("pdf"+str(i)+".pdf", 'wb')
        #         pdf.write(response.content)
        #         pdf.close()
        #         print("File ", i, " downloaded")
  
        # print("All PDF files downloaded")
        # print(links.text.strip())
        # filelink = link for link in links: if ('.pdf' in link.get('href')): print(link.get('href')) filelink = link.get('href') 
        # print(filelink)
        # break


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
        print(json_object)




data_for_forms(tax_form_names)


# sample download file urls
# https://www.irs.gov/pub/irs-prior/fw2p--1990.pdf
# https://www.irs.gov/pub/irs-prior/f1099c--2021.pdf

