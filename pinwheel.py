import requests
from bs4 import BeautifulSoup

#This code issues an HTTP GET request to the given URL. It retrieves the HTML data 
# that the server sends back and stores that data in a Python object.
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# print(page.text)

#object that takes page.content, which is the HTML content you scraped, as its input
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

# pull the element *id* you want
results = soup.find(id="ResultsContainer")

#prettify() formats results
# print(results.prettify())

# this creats an "iterable" to loop through all results
job_elements = results.find_all("div", class_="card-content")
# print(job_elements)

# for job_element in job_elements:
#     print(job_element, end="\n"*2)

# pull text in an element and clean it up
# for job_element in job_elements:
#     title_element = job_element.find("h2", class_="title")
#     company_element = job_element.find("h3", class_="company")
#     location_element = job_element.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     print()

# this matches exact strings
# python_jobs = results.find_all("h2", string="Python")
# print(python_jobs)

# The lambda function looks at the text of each <h2> element, converts it to 
# lowercase, and checks whether the substring "python" is found anywhere.
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

# need to call parent of parent to encompass all sections that include data 
# we're wanting to show
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

# unpack and lable each section
for job_element in python_job_elements:

    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    #to print the actual link not the text shown on site, need to search by href
    links = job_element.find_all("a", string="Apply")
    for link in links:
        link_url = link["href"]
        print(link_url)
    print()



# Take in a list of tax form names

# Search the website for the tax forms

# Return: JSON of the "Product Number", the "Title", and the maximum and minimum 
# years the form is available for download.

# Return: download all PDFs available within the years range specified. The 
# downloaded PDFs should be downloaded to a subdirectory under your script's main 
# directory with the name of the form, and the file name should be the "Form Name - Year"

# click (cli)
# optional arg parse - stnd py package (cli)

# parse website with bs3
# to dl pdf file use python requests, remember to use flags

#tax_form_names = ["Form W-2", "Form 1095-C"]



