import requests
import os
from bs4 import BeautifulSoup
from unittest.mock import Mock

# TODO: Move testing code into a separate sheet or within a separate function (currently
# testing has been moved to separate file but cannot be called to add input yet)
# TODO: Make input or testing work without making code modification (currently
# performs correctly if calling this file and without any misspelling inputs)


def get_user_input():
    tax_form_name = input(">> You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2) ")
    start_year = input(">> What year would you like the downloads to start at? ")
    end_year = input(">> Up until which year should be included? ")
    return tax_form_name, start_year, end_year


def get_url(tax_form_name):
    """Create URL for initial web scraping."""

    form_name = tax_form_name.lower()

    # Saved here with 200 items per page. Manual site checking defaults to 25 per. 
    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_name + "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    return url


def make_list_of_years(start_year, end_year):
    """Takes user input and creates a list of all years (inclusive)."""

    list_of_form_years = []
    years_list = [start_year, end_year]

    for input in years_list:
        if input not in '0123456789':
            print("MUST BE INT", input)
            break

    for i in range(int(start_year), int(end_year)+1):
        list_of_form_years.append(i)

    return list_of_form_years


def scrape_page(url):
    """Grab all html that has content we need for tax form PDF downloads."""

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def validate_form_input(soup):
    """If the input has a typo or misspelling, the page will not produce results. 
    Show the user a message to check their input."""

    # Soup is a BS4 type. To check for a string, we need to temporarily convert it to a string.
    soup_string = str(soup)

    if 'No results were found that match your entry' in soup_string:
        return 'There are no results that match your entry. Please check for typos and that you are using the correct form name.'
        
    else:
        # Returns as a BS4 type
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
    """Check if there are other web pages the forms' PDFs could be available to 
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


def make_subdirectory_for_pdfs(sample_tax_form_name):
    """Make one subdirectory for each form type to save the PDF's inside. Name 
    it after the form."""

    subdirectory_for_pdfs = sample_tax_form_name

    if not os.path.exists(subdirectory_for_pdfs):
        os.mkdir(subdirectory_for_pdfs)
        return subdirectory_for_pdfs

    else:    
        return subdirectory_for_pdfs


def save_pdf(subdirectory_for_pdfs, list_of_pdf_links, sample_tax_form_name):
    """Save any PDFs available inside the subdirectory."""

    if list_of_pdf_links == []:
        return 'There are no PDF downloads for those years. If you think this is an error, please check for typos.'

    else:
        for i in range(len(list_of_pdf_links)):
            url = list_of_pdf_links[i]
            path = subdirectory_for_pdfs

            # Naming convention example: Form W-2/Form W-2 - 2020.pdf
            file_name = sample_tax_form_name + " - " + str(url[-8:])
            complete_name = os.path.join(path, file_name)
            r = requests.get(url) 

            with open(complete_name, 'wb') as f:
                f.write(r.content)
                f.close()

        return 'Downloads completed'


def get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year, sample_tax_form_name):
    """Perform all actions to find any PDF"s and download them to a subdirectory."""

    soup = scrape_page(url)

    # Check for typos or zero results
    validate_response = validate_form_input(soup)

    if 'no results' in validate_response:
        return validate_response

    only_pdf_links = get_only_pdf_links(soup)
    list_of_pdf_links = get_pdf_links(list_of_pdf_links, list_of_form_years, only_pdf_links)

    # Not 0 if there are still years that need forms downloaded
    if len(list_of_form_years) != 0:

        if_next = check_if_next_page(soup)

        # None is if there are no more pages available to check
        if if_next == None:

            # Download PDFs
            subdirectory_for_pdfs = make_subdirectory_for_pdfs(sample_tax_form_name)
            formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, sample_tax_form_name)

            return formatted_download_response

        # Recursively search pages for more links
        else:
            return get_downloads(if_next, list_of_pdf_links, list_of_form_years, start_year, end_year, sample_tax_form_name)
    
    # Download PDFs
    else:
        subdirectory_for_pdfs = make_subdirectory_for_pdfs(sample_tax_form_name)
        formatted_download_response = save_pdf(subdirectory_for_pdfs, list_of_pdf_links, sample_tax_form_name)

        return formatted_download_response


def download_pdfs_and_save():
    """Puts together initial URL for web scraping, list of years to download tax
    forms, and calls function to download the PDFs."""

    user_input = get_user_input()
    sample_tax_form_name = user_input[0]
    start_year = user_input[1]
    end_year = user_input[2]

    url = get_url(sample_tax_form_name)

    list_of_form_years = make_list_of_years(start_year, end_year)

    # this list will collect all PDFs to be downloaded
    list_of_pdf_links = []
    
    download_response = get_downloads(url, list_of_pdf_links, list_of_form_years, start_year, end_year, sample_tax_form_name)

    return download_response



if __name__ == '__main__':
    print(download_pdfs_and_save())
