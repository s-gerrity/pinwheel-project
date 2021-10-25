import requests
from bs4 import BeautifulSoup
import os
import sys
import argparse

# list of the files in your path when cli executed
# python3 practice.py = ['practice.py']
# python3 practice.py /Pinwheel /projects = ['practice.py', '/Pinwheel', '/projects']
# print(sys.argv)

# if len(sys.argv) > 2:
#     print('You have specified too many arguments')
#     sys.exit()

# if len(sys.argv) < 2:
#     print('You need to specify the path to be listed')
#     sys.exit()

# input_path = sys.argv[1]

# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()

# print('\n'.join(os.listdir(input_path)))

# Create the parser
# my_parser = argparse.ArgumentParser(description='List the content of a folder')

# # Add the arguments
# my_parser.add_argument('Path',
#                        metavar='path',
#                        type=str,
#                        help='the path to list')

# # Execute the parse_args() method
# args = my_parser.parse_args()

# input_path = args.Path

# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()

# print('\n'.join(os.listdir(input_path)))










########################
# Beautiful Soup practice

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
# python_jobs = results.find_all(
#     "h2", string=lambda text: "python" in text.lower()
# )

# # need to call parent of parent to encompass all sections that include data 
# # we're wanting to show
# python_job_elements = [
#     h2_element.parent.parent.parent for h2_element in python_jobs
# ]
# # print(python_job_elements)

# # pack and lable each section
# for job_element in python_job_elements:

#     title_element = job_element.find("h2", class_="title")
#     company_element = job_element.find("h3", class_="company")
#     location_element = job_element.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     #to print the actual link not the text shown on site, need to search by href
#     links = job_element.find_all("a", string="Apply")
#     for link in links:
#         link_url = link["href"]
#         print(link_url)
#     print()


