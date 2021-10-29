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
    print()
    print(list_of_form_years)
    print()
    print(start_year, end_year)

    return list_of_form_years


def scrape_page(url):
    """Grab all html that has content we need for tax form PDF downloads."""

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_pdf_links(soup, list_of_pdf_links, start_year, end_year):
    """For each year a donwnload is needed, find the link for its PDF on the
    web page and save it to a list."""

    links = soup.find_all('a')


    for i in range(int(start_year), int(end_year)+1):

        for link in links:
            link_url = link["href"]

            # Looks for 'pdf' and the year as string in each url
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


def make_subdirectory_for_pdfs():
    subdirectory_for_pdfs = tax_form_name

    if not os.path.exists(subdirectory_for_pdfs):
        os.mkdir(subdirectory_for_pdfs)
        return subdirectory_for_pdfs

    else:    
        return subdirectory_for_pdfs


def save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_pdf_years):

    if list_of_pdf_links == []:
        # return "There are no " + tax_form_name + "PDF's for the years: " + str(list_of_pdf_years)
        # print("There are no " + tax_form_name + " PDF's for the years: " + str(list_of_pdf_years))
        # return "There are no " + tax_form_name + "PDF's for the years: " + str(list_of_pdf_years)
        return 'There are no PDF downloads for those years'
        # return list_of_pdf_links

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

    return 'Downloads completed'


def get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year):
    """Perform all actions to download the PDF"s."""

    soup = scrape_page(url)
    list_of_pdf_links = get_pdf_links(soup, list_of_pdf_links, start_year, end_year)

    # Pagination is necessary if there are years that haven't had links for PDF's located yet
    if len(list_of_form_years) != len(list_of_pdf_links):
        # If links needed, see if there is another page to search
        if_next = check_if_next_page(soup)

        # If there are no more pages to check 'if_next' will be None and proceed to downloading
        if if_next == None:
            subdirectory_for_pdfs = make_subdirectory_for_pdfs()
            formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_form_years)

            return formatted_download_response

        else:
            get_downloads(if_next, list_of_pdf_links, list_of_form_years, start_year, end_year)
    
    else:
        subdirectory_for_pdfs = make_subdirectory_for_pdfs()
        formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, list_of_form_years)

        return formatted_download_response


def download_pdfs_and_save(tax_form_name, start_year, end_year):
    """Puts together initial URL for web scraping, list of years to download tax
    forms, and calls function to download the PDF's."""

    url = get_url(tax_form_name)

    list_of_form_years = make_list_of_years(start_year, end_year)

    # this link will collect all PDF's to be downloaded
    list_of_pdf_links = []
    
    download_response = get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year)
    print(download_response, "how it ends")
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


# if len is off and next is not none
# search next page

# if len is off and next is none and download needed
# get downloads
# report that only some were available



# if len is equal and fields are empty
# check for next
# if no next
# report none were available

# if len is equal
# donwload
# report completed