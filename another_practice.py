# start by only pulling the product num and title, then returning JSON

import requests
import os
from bs4 import BeautifulSoup

# TODO: fix infinite loop pagination; add mk dir and download files
#pseudocode
# make a directory for the pdfs to be saved in
# make a list of the years needed for pdf dl's
# search the first page a pdf with the name and year
# if pdf found, add link to a list
# open a file in the new directory
# copy pdf wb into new file
# name file form/form - year.pdf 
# pop year off the list
# if list empty when page search ends
# check if there is another page to search
# if not, leave and end
# if there is, search page for years in list
# if no more pages, return output reporting this form - year not available


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


def check_if_next_page(soup):
    url = "https://apps.irs.gov"

    results = soup.find("th", class_="NumPageViewed")

    pagenation_links = results.find_all("a")

    for item in pagenation_links:

        if "Next" in item.text:
            new_url = url + item['href']

            return new_url
    
    return None



def download_pdfs_and_save(tax_form_name):
    #   TODO: pagination and download

    url = get_url(tax_form_name)
    
    list_of_pdf_links = get_downloads(url, start_year, end_year)

    # return list_of_pdf_links

def get_downloads(url, start_year, end_year):
    soup = scrape_page(url)
    list_of_pdf_links = get_links(soup, start_year, end_year)
    if_next = check_if_next_page(soup)
    if if_next != None:
        get_downloads(url, start_year, end_year)
    else:
        # return list_of_pdf_links

    # print(list_of_pdf_links)


        #         with open(tax_form_name + "/" + tax_form_name + " - " + str(i) + ".pdf", 'wb') as f:
        #             f.write(page.content)
        #             f.close()




    # print(tax_form_name + "/" + tax_form_name + " - 2020.pdf")


        
        

# print(download_pdfs_and_save(tax_form_name))
