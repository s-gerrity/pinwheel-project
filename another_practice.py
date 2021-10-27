# start by only pulling the product num and title, then returning JSON

import requests
import os
from bs4 import BeautifulSoup


tax_form_name = "Form W-2"
start_year = 2018
end_year = 2020


def get_url(tax_form_name):
    form_name = tax_form_name.lower()

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_name + "&criteria=formNumber&resultsPerPage=25&isDescending=false"

    return url


def scrape_page(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_links(soup, start_year, end_year):
    list_of_pdf_links = []

    links = soup.find_all('a')
    for i in range(start_year, end_year+1):
        print(i)
    
        for link in links:
            link_url = link["href"]
            if 'pdf' in link_url and str(i) in link_url:
                list_of_pdf_links.append(link_url)
    return list_of_pdf_links


def download_pdfs_and_save(tax_form_name, start_year, end_year):
    #   TODO: pagination and download

    url = get_url(tax_form_name)
    soup = scrape_page(url)
    list_of_pdf_links = get_links(soup, start_year, end_year)

    # print(list_of_pdf_links)


        #         with open(tax_form_name + "/" + tax_form_name + " - " + str(i) + ".pdf", 'wb') as f:
        #             f.write(page.content)
        #             f.close()




    # print(tax_form_name + "/" + tax_form_name + " - 2020.pdf")


        
        

# download_pdfs_and_save(tax_form_name, start_year, end_year)
