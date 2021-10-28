# start by only pulling the product num and title, then returning JSON

import requests
import os
from bs4 import BeautifulSoup

# TODO: fix infinite loop pagination; add mk dir and download files
#pseudocode
# make a list of the years' links needed for pdf dl's
# if pdf found, add link to a list
# if list not empty - need to handle this case somehow
# make a directory for the pdfs to be saved in
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


def get_pdf_links(soup, start_year, end_year):
    list_of_pdf_links = []
    list_of_form_years = []

    links = soup.find_all('a')
    for i in range(start_year, end_year+1):
    
        for link in links:
            link_url = link["href"]
            if 'pdf' in link_url and str(i) in link_url:
                list_of_pdf_links.append(link_url)
                list_of_form_years.append(i)
    return list_of_pdf_links, list_of_form_years

def make_subdirectory_for_pdfs():
    subdirectory_for_pdfs = tax_form_name

    if not os.path.exists(subdirectory_for_pdfs):
        os.mkdir(subdirectory_for_pdfs)
        return subdirectory_for_pdfs
    else:    
        return subdirectory_for_pdfs


def save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_pdf_years):
    
    for i in range(len(list_of_pdf_years)):
        path = subdirectory_for_pdfs
        file_name = tax_form_name + " - " + str(list_of_pdf_years[i]) +".pdf"
        print(file_name)
        print()
        complete_name = os.path.join(path, file_name)
        print(complete_name)
        print()
        url = list_of_pdf_links[i]
        r = requests.get(url) 
        print(url)
        print()
        with open(complete_name, 'wb') as f:
            f.write(r.content)
            f.close()
    print("completed downloads")

        
        # complete_name = os.path.join(path, file_name)

# create_file = open(complete_name, 'w')
# create_file.write('please add to the right directory')
# create_file.close()
            # complete_name = os.path.join(path, file_name)

            # create_file = open(complete_name, 'w')
            # create_file.write('please add to the right directory')
            # create_file.close()

    


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
    #   TODO: download

    url = get_url(tax_form_name)
    
    list_of_forms = get_downloads(url, start_year, end_year)

    return list_of_forms


def get_downloads(url, start_year, end_year):

    soup = scrape_page(url)
    list_of_forms = get_pdf_links(soup, start_year, end_year)
    list_of_pdf_links = list_of_forms[0]
    list_of_pdf_years = list_of_forms[1]

    # print(list_of_forms)
    if list_of_forms == []:
        print("list is empty!")
    else:
        subdirectory_for_pdfs = make_subdirectory_for_pdfs()
        done = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_pdf_years)


    # if_next = check_if_next_page(soup)
    # if if_next != None:
    #     print("link for if_next, exiting main function")
    #     # get_downloads(url, start_year, end_year)
    # else:
    #     return list_of_forms

    # print(list_of_pdf_links)


    #             with open(tax_form_name + "/" + tax_form_name + " - " + str(i) + ".pdf", 'wb') as f:
    #                 f.write(page.content)
    #                 f.close()




    # print(tax_form_name + "/" + tax_form_name + " - 2020.pdf")

        
# subdirectory_for_pdfs = 'tax_form_pdfs'

# if not os.path.exists(subdirectory_for_pdfs):
#     os.mkdir(subdirectory_for_pdfs)
#     print("Directory " , subdirectory_for_pdfs ,  " Created ")
# else:    
#     print("Directory ", subdirectory_for_pdfs ,  " already exists")

# path = subdirectory_for_pdfs
# file_name = 'sammy.txt'

# complete_name = os.path.join(path, file_name)

# create_file = open(complete_name, 'w')
# create_file.write('please add to the right directory')
# create_file.close()



print(download_pdfs_and_save(tax_form_name))
