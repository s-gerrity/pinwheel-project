# start by only pulling the product num and title, then returning JSON

import requests
import json
from bs4 import BeautifulSoup

# list of all tax forms we need to pull
tax_form_names = ["Form W-2", "Form 1095-C"]
json_form_data = {
    "Product Number": "Form 1095-C",
    "Title": "Employer-Provided Health Insurance Offer and Coverage",
    "Minimum Year": "2014",
    "Maximum Year": "2020"
}


###### MAIN FUNCTION


def download_tax_form_pdfs(json_form_data):
#     # TODO: iterate through pages somehow

        url_form_name = json_form_data["Product Number"].lower()
        # print(url_form_name)
        
        new_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + url_form_name + "&criteria=formNumber&resultsPerPage=25&isDescending=false"
        # print(new_URL)

        page = requests.get(new_URL)

        # # object that takes page.content, which is the HTML content you scraped, as its input
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup)

        links = soup.find_all('a')
        for link in links:
            link_url = link["href"]
            if 'pdf' in link_url:
                with open('tax_form_pdfs/' + json_form_data["Product Number"] + ' - ' + json_form_data["Product Number"] + '.pdf') as f:
                    f.write(page.content)
        # i = 0
        # for link in links[:23]:
        #     if ('.pdf' in link.get('href', [])):
        #         i += 1
        #         print("Downloading file: ", i)
  
        # # # Get response object for link
        #         response = requests.get(link.get('href'))
        #         print(link.get('href'))
        #         pdf = open("pdf"+str(i)+".pdf", 'wb')
        #         pdf.write(response.content)
        #         pdf.close()
        #         print("File ", i, " downloaded")
                # with open('tax_form_pdfs/' + product_number + ' - ' + form_year + '.pdf') as f:
                #     f.write(response.content)
  
        # print("All PDF files downloaded")
        # print(links.text.strip())
        # filelink = link for link in links: if ('.pdf' in link.get('href')): print(link.get('href')) filelink = link.get('href') 
        # print(filelink)
        # break



download_tax_form_pdfs(json_form_data)


# sample download file urls
# https://www.irs.gov/pub/irs-prior/fw2p--1990.pdf
# https://www.irs.gov/pub/irs-prior/f1099c--2021.pdf

