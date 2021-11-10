
import requests
import json
from bs4 import BeautifulSoup

# TODO: JSON needs to take input 
# TODO: JSON needs to take input without requiring code modification for input
# TODO: Report error communication instead of passing error unhandled exceptions

tax_forms_to_check = ["Form W-2"]


def make_url(form_to_check):
    """Make the url with the forms name in lower case."""

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_to_check.lower() + "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    return url
    

def scrape_page(url):
    """Gather the websites html so we can search for our data."""

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def area_to_search_form_data(soup):
    """Locate the area in the html that has the tax form data. It is positioned in a table with
    rows labeled 'even" and 'odd'."""

    # An iterable we'll use later to loop through each forms data
    results = soup.find("div", class_="picklistTable")

    row_form_data = results.find_all("tr", class_=["even", "odd"])

    return row_form_data


def collect_tax_form_details(dict_form_data, row_form_data, form_to_check):
    """We find each form with the name that matches the form we're searching. Add the
    'product number' form name and form title to a dictionary."""

    for form in row_form_data:
        # The IRS site refers to the form name as the "product number"
        product_number_form_name = form.find("td", class_="LeftCellSpacer")

        # Check if the row is the form we are looking for and add it's details to our
        # dictionary data set
        if product_number_form_name.text.strip() == form_to_check:
            dict_form_data['Product Number'] = product_number_form_name.text.strip()
            form_title = form.find("td", class_="MiddleCellSpacer")
            dict_form_data['Title'] = form_title.text.strip()

    return dict_form_data


def collect_tax_years(all_form_years, row_form_data, form_to_check):
    """All years the form is available are added to a list."""

    for form in row_form_data:
            product_number_form_name = form.find("td", class_="LeftCellSpacer")

            if product_number_form_name.text.strip() == form_to_check:
                form_year = form.find("td", class_="EndCellSpacer")
                all_form_years['Years'].append(form_year.text.strip())

    return all_form_years


def check_if_next_page(soup):
    """Check the website to see if there are more pages with forms to search. More pages
    available is noted by 'Next'. Return None if there are no additional pages. If there
    are more pages, return the URL for the next page."""

    url = "https://apps.irs.gov"

    results = soup.find("th", class_="NumPageViewed")

    pagenation_links = results.find_all("a")

    for item in pagenation_links:

        if "Next" in item.text:
            new_url = url + item['href']

            return new_url
    
    return None


def get_min_max_years(all_form_years, dict_form_data):
    """Find highest and lowest years in the Years list and add to our dictionary."""

    dict_form_data['Minimum Year'] = min(all_form_years['Years'])
    dict_form_data['Maximum Year'] = max(all_form_years['Years'])

    return dict_form_data


def append_to_main_list_as_json(dict_with_form_data, tax_form_info):
    """Add our finalized dictionary to the output list."""

    tax_form_info.append(dict_with_form_data)

    return tax_form_info


############## MAIN FUNCTIONS ############  


def get_data(dict_form_data, all_form_years, form_to_check, tax_form_info, url):
    """Get data from the site and store in a data set. If there are more web pages to
    check we gather this data recursively."""

    soup = scrape_page(url)
    row_form_data = area_to_search_form_data(soup)
    dict_form_data = collect_tax_form_details(dict_form_data, row_form_data, form_to_check)
    print(dict_form_data)
    print()
    all_form_years = collect_tax_years(all_form_years, row_form_data, form_to_check)
    print(all_form_years)
    
    # Check for pagination. Returns None if there are no more pages to find form data.
    if_next = check_if_next_page(soup)

    # Recursively search more pages and collect form data
    if if_next != None:
        return get_data(dict_form_data, all_form_years, form_to_check, tax_form_info, if_next)
    
    return finalize_data(all_form_years, dict_form_data, tax_form_info)
            

def finalize_data(all_form_years, dict_form_data, tax_form_info):
    """Add maximum year and minimum year to the dictionary. Insert the dictionary into
    a list."""

    dict_with_form_data = get_min_max_years(all_form_years, dict_form_data)
    tax_form_info = append_to_main_list_as_json(dict_with_form_data, tax_form_info)

    return tax_form_info


def get_tax_info(tax_forms_to_check):
    """Takes in a list of tax forms to collect data on from the IRS website and 
    returns a JSON with the form name, title, minimum and maximum years the forms
    are available."""

    # This list will hold our JSON output when finished
    tax_form_info = []

    for form_to_check in tax_forms_to_check:
        dict_form_data = {}
        all_form_years = {'Years': []}

        url = make_url(form_to_check)

        get_data(dict_form_data, all_form_years, form_to_check, tax_form_info, url)

    # Return list with a dictionary to list with JSON    
    return print(json.dumps(tax_form_info, indent = 4))
    

if __name__ == '__main__':
    get_tax_info(tax_forms_to_check)