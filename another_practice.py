import requests
import os
from bs4 import BeautifulSoup


# tax_form_name = input(">> What is the name of the tax form you'd like to download? ")
# start_year = input(">> What starting year would you like to download: ")
# end_year = input(">> What year would you like your search to end: ")


def get_url(tax_form_name):
    """Create URL for initial web scraping."""

    form_name = tax_form_name.lower()

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_name + "&criteria=formNumber&resultsPerPage=25&isDescending=false"
    
    return url


def make_list_of_years(start_year, end_year):
    """Takes user input and creates a list of all years (inclusive)."""

    list_of_form_years = []

    for i in range(int(start_year), int(end_year)+1):
        list_of_form_years.append(i)

    return list_of_form_years


def scrape_page(url):
    """Grab all html that has content we need for tax form PDF downloads."""

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_only_pdf_links(soup):
    """Adds only links from page that go to a PDF."""

    links = soup.find_all('a')
    only_pdf_links = []

    for link in links:
        link_url = link["href"]

        # Looks for 'pdf' and the year as string in each url
        if 'pdf' in link_url:
            only_pdf_links.append(link_url)

    return only_pdf_links


def get_pdf_links(list_of_pdf_links, list_of_form_years, only_pdf_links):
    """Check each PDF for the year. If it's a year we are requesting, add
    it to our list. Remove years found from original to track how many to
    keep searching for."""

    for link in only_pdf_links:

        for year in list_of_form_years:

            if str(year) in link:
                list_of_pdf_links.append(link)
                list_of_form_years.remove(year)

    return list_of_pdf_links 


def check_if_next_page(soup):
    """Check if there are other web pages the forms' PDF's could be available to 
    download from. The links are identified by 'Next'. We return None when there are
    no additional pages to search."""

    url = "https://apps.irs.gov"

    results = soup.find("th", class_="NumPageViewed")

    pagenation_links = results.find_all("a")

    for item in pagenation_links:

        if "Next" in item.text:
            new_url = url + item['href']

            return new_url
            
    return None


def make_subdirectory_for_pdfs():
    """Make one subdirectory for each form type to save the PDF's inside. Name 
    it after the form."""

    subdirectory_for_pdfs = tax_form_name

    if not os.path.exists(subdirectory_for_pdfs):
        os.mkdir(subdirectory_for_pdfs)
        return subdirectory_for_pdfs

    else:    
        return subdirectory_for_pdfs


def save_pdf(subdirectory_for_pdfs, list_of_pdf_links):
    """Save any PDF's available inside the subdirectory."""

    if list_of_pdf_links == []:
        return 'There are no PDF downloads for those years'

    else:
        for i in range(len(list_of_pdf_links)):
            url = list_of_pdf_links[i]
            path = subdirectory_for_pdfs

            # Naming convention example: Form W-2/Form W-2 - 2020.pdf
            file_name = tax_form_name + " - " + str(url[-8:])
            complete_name = os.path.join(path, file_name)
            r = requests.get(url) 

            with open(complete_name, 'wb') as f:
                f.write(r.content)
                f.close()

        return 'Downloads completed'


def get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year):
    """Perform all actions to find any PDF"s and download them to a subdirectory."""

    # Get any PDF links from the webpage
    soup = scrape_page(url)
    only_pdf_links = get_only_pdf_links(soup)
    list_of_pdf_links = get_pdf_links(list_of_pdf_links, list_of_form_years, only_pdf_links)

    # Pagination is necessary if there are years that haven't had links for PDF's located yet
    if len(list_of_form_years) != 0:

        # See if there is another page to search for remaining links needed
        if_next = check_if_next_page(soup)

        # None is if there are no more pages available to check and proceed downloading
        if if_next == None:

            # Download PDF's
            subdirectory_for_pdfs = make_subdirectory_for_pdfs()
            formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links)

            return formatted_download_response

        # Search pages for more links
        else:
            return get_downloads(if_next, list_of_pdf_links, list_of_form_years, start_year, end_year)
    
    # Download PDF's
    else:
        subdirectory_for_pdfs = make_subdirectory_for_pdfs()
        formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links)

        return formatted_download_response


def download_pdfs_and_save(tax_form_name, start_year, end_year):
    """Puts together initial URL for web scraping, list of years to download tax
    forms, and calls function to download the PDF's."""

    url = get_url(tax_form_name)

    list_of_form_years = make_list_of_years(start_year, end_year)

    # this link will collect all PDF's to be downloaded
    list_of_pdf_links = []
    
    download_response = get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year)

    return download_response
    



################ TESTS ##########

def run_test(testValue, expectedResult, description):
    print(description)
    if testValue == expectedResult:
        print('    ✅ Test passed')
    else:
        print('    ❌ Test failed!')


tax_form_name = "Form W-2"
not_found_start_year = 1935
not_found_end_year = 1937
found_start_year = 2017
found_end_year = 2020
found_page_two_start_year = 2012
found_page_two_end_year = 2016
beginning_available_end_year = 1954


run_test(download_pdfs_and_save(tax_form_name, not_found_start_year, not_found_end_year), 'There are no PDF downloads for those years', 'Input years are neither available for the form')
run_test(download_pdfs_and_save(tax_form_name, found_start_year, found_end_year), 'Downloads completed', 'Input years both available and on one page')
run_test(download_pdfs_and_save(tax_form_name, found_page_two_start_year, found_end_year), 'Downloads completed', 'Start year on diff page, all pdf"s available')
run_test(download_pdfs_and_save(tax_form_name, found_page_two_start_year, found_page_two_end_year), 'Downloads completed', 'Start and end years both available and on page two')
run_test(download_pdfs_and_save(tax_form_name, not_found_start_year, beginning_available_end_year), 'Downloads completed', 'Only one year available')
