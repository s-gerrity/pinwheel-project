import requests
import os
from bs4 import BeautifulSoup


# tax_form_name = input(">> What is the name of the tax form you'd like to download? ")
# start_year = input(">> What starting year would you like to download: ")
# end_year = input(">> What year would you like your search to end: ")
tax_form_name = "Form W-2"
start_year = 1933
end_year = 1934



def get_url(tax_form_name):
    form_name = tax_form_name.lower()

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_name + "&criteria=formNumber&resultsPerPage=25&isDescending=false"
    
    return url


def make_list_of_years(start_year, end_year):
    list_of_form_years = []

    for i in range(int(start_year), int(end_year)+1):
        list_of_form_years.append(i)

    return list_of_form_years


def scrape_page(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_pdf_links(soup, list_of_pdf_links, list_of_form_years):
    # print(list_of_form_years, "YEARS", list_of_pdf_links, "LINKS")

    links = soup.find_all('a')


    for i in range(int(start_year), int(end_year)+1):
        # print(i)
        # print()
        for link in links:
            link_url = link["href"]

            if 'pdf' in link_url and str(i) in link_url:
                # print("YES", link_url)
                list_of_pdf_links.append(link_url)
                # print(list_of_pdf_links, "list_of_pdf_links YES")
            # else:
            #     print("expected link not found")

    return list_of_pdf_links, list_of_form_years


def check_if_next_page(soup):
    url = "https://apps.irs.gov"

    results = soup.find("th", class_="NumPageViewed")

    pagenation_links = results.find_all("a")

    for item in pagenation_links:

        if "Next" in item.text:
            new_url = url + item['href']

            return new_url
            
    return None


def make_subdirectory_for_pdfs():
    subdirectory_for_pdfs = tax_form_name

    if not os.path.exists(subdirectory_for_pdfs):
        os.mkdir(subdirectory_for_pdfs)
        return subdirectory_for_pdfs

    else:    
        return subdirectory_for_pdfs


def save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_pdf_years):

    if list_of_pdf_links == []:
        return "no links found"
    
    for i in range(len(list_of_pdf_years)):
        url = list_of_pdf_links[i]
        path = subdirectory_for_pdfs
        file_name = tax_form_name + " - " + str(url[-8:])
        # print(file_name, "**********")
        complete_name = os.path.join(path, file_name)
        
        # r = requests.get(url) 
        # print(url)
        # print()
        # with open(complete_name, 'wb') as f:
        #     f.write(r.content)
        #     f.close()

    return "Downloads completed"





def get_downloads(url, list_of_pdf_links, list_of_form_years):

    soup = scrape_page(url)
    list_of_forms = get_pdf_links(soup, list_of_pdf_links, list_of_form_years)
    # print(list_of_forms)
    list_of_pdf_links = list_of_forms[0]
    list_of_pdf_years = list_of_forms[1]

    # check if pagination is necessary
    if len(list_of_pdf_years) != len(list_of_pdf_links):
        # print(list_of_forms, "lens not")
        if_next = check_if_next_page(soup)
        # print(if_next, "ALOHA")
        # print()
        # print(list_of_forms)

        if if_next == None:
            subdirectory_for_pdfs = make_subdirectory_for_pdfs()
            done = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_form_years)

            return done

        else:
            done = get_downloads(if_next, list_of_pdf_links, list_of_form_years)
    
    else:
        subdirectory_for_pdfs = make_subdirectory_for_pdfs()
        done = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_pdf_years)
        # print("len is equal and done", done)
        return done

def download_pdfs_and_save():
    url = get_url(tax_form_name)

    list_of_form_years = make_list_of_years(start_year, end_year)

    list_of_pdf_links = []
    
    how_it_ends = get_downloads(url, list_of_pdf_links, list_of_form_years)

    return how_it_ends
    
print(download_pdfs_and_save())
