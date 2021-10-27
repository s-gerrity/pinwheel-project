
import requests
import json
import re
from bs4 import BeautifulSoup


# click (cli)
# optional arg parse - stnd py package (cli)

# parse website with bs3
# to dl pdf file use python requests, remember to use flags

tax_forms_to_check = ["Form W-2", "Form 1095-C"]


# TODO: pagenation

# url_last_page = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=200&sortColumn=sortOrder&value=Form+w-2&criteria=formNumber&resultsPerPage=200&isDescending=false"
# url_not_last_page = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value=Form+w-2&isDescending=false"
# base_url = "https://apps.irs.gov"
# page_four = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=75&sortColumn=sortOrder&value=Form+w-2&criteria=formNumber&resultsPerPage=25&isDescending=false"

# def start_checking():

#     page = requests.get(url_not_last_page)

#     soup = BeautifulSoup(page.content, "html.parser")

#     results = soup.find("th", class_="NumPageViewed")

#     pagenation_links = results.find_all("a")
#     print(pagenation_links)
#     print()
#     for item in pagenation_links:
#         if "Next" in item.text:
#             new_url = base_url + item['href']
#     return 


# def go_to_next_page():
#     # take in the url and change it. update index begins.

#     # takes url
#     page = requests.get(page_four)

#     # gets all page content
#     soup = BeautifulSoup(page.content, "html.parser")

#     # finds on the page the link within "next", but without the base url
#     next_page = soup.find('a', text=re.compile(r'.*Next.*'))
#     if next_page == None:
#         print("next page none")
#         print()
#     else:
#         print(next_page['href'])
#         print("new link: " + base_url + next_page['href'])


# pseudocode
# do we check for next after we've scraped the page already once?
# if next in <a> tag
# move to next page and keep adding to the same json set
# add 200 to the urls start index on

    

def scrape_page(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    print("SCRAPE WITH URL", url)
    print()

    return soup


def area_to_search_form_data(soup):

    # this creats an "iterable" to loop through all results
    results = soup.find("div", class_="picklistTable")

    form_data = results.find_all("tr", class_=["even", "odd"])

    return form_data


def collect_tax_form_details(dict_for_data, form_data, form_to_check):
    

    for form in form_data:
        product_number = form.find("td", class_="LeftCellSpacer")

        if product_number.text.strip() == form_to_check:
            dict_for_data['Product Number'] = product_number.text.strip()
            form_title = form.find("td", class_="MiddleCellSpacer")

            # collect applicable years in a list to sort the min and max later
            dict_for_data['Title'] = form_title.text.strip()

    return dict_for_data

def collect_tax_years(all_form_years, form_data, form_to_check):

    for form in form_data:
            product_number = form.find("td", class_="LeftCellSpacer")

            if product_number.text.strip() == form_to_check:
                form_year = form.find("td", class_="EndCellSpacer")
                all_form_years['Years'].append(form_year.text.strip())


    return all_form_years


def get_min_max_years(all_form_years, dict_for_data):

    dict_for_data['Minimum Year'] = min(all_form_years['Years'])
    dict_for_data['Maximum Year'] = max(all_form_years["Years"])

    return dict_for_data


def append_to_main_list_as_json(dict_with_form_data, tax_form_info):

    tax_form_info.append(dict_with_form_data)

    return tax_form_info


def make_url(form_to_check):

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=" + form_to_check.lower() + "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    return url


def check_if_next_page(soup, base_url):
    url = "https://apps.irs.gov"
    print(base_url, "BASE")
    print()
    results = soup.find("th", class_="NumPageViewed")

    pagenation_links = results.find_all("a")
    # print(pagenation_links)
    # print()
    # print("SJDSJDHBVDJBVDJVB")
    for item in pagenation_links:
        print(item)
        print()
        if "Next" in item.text:
            new_url = url + item['href']
            print(new_url, "new url")
            return new_url
    
    return None


def get_tax_info(tax_forms_to_check):
    tax_form_info = []

    for form_to_check in tax_forms_to_check:
        dict_for_data = {}
        all_form_years = {'Years': []}

        url = make_url(form_to_check)
        

        get_data(dict_for_data, all_form_years, form_to_check, tax_form_info, url)
    
    print(json.dumps(tax_form_info, indent = 4))
    
    return print("All forms have been checked")
        

def get_data(dict_for_data, all_form_years, form_to_check, tax_form_info, url):
        soup = scrape_page(url)
        form_data = area_to_search_form_data(soup)
        dict_for_data = collect_tax_form_details(dict_for_data, form_data, form_to_check)
        print(dict_for_data, "dict_for_data")
        print()
        all_form_years = collect_tax_years(all_form_years, form_data, form_to_check)
        print(all_form_years, "all_form_years")
        print()
        if_next = check_if_next_page(soup, url)
        print(if_next, "if_next")
        print()
        if if_next != None:
            print("SDJFSDJBHDJHBVDLKVNKSDNVDKBVJDB")
            get_data(dict_for_data, all_form_years, form_to_check, tax_form_info, if_next)
        else:
            finalize_data(all_form_years, dict_for_data, tax_form_info)
            

def finalize_data(all_form_years, dict_for_data, tax_form_info):
    dict_with_form_data = get_min_max_years(all_form_years, dict_for_data)
    tax_form_info = append_to_main_list_as_json(dict_with_form_data, tax_form_info)



get_tax_info(tax_forms_to_check)

# start_checking()
# go_to_next_page()