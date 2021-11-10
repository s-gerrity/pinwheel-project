## Pinwheel Coding Challenge
---------------------------------------------------------------
### Interview project for Software Engineer, Integrations


#### These are two Python utilities that scrape the IRS website to do two things: 
###### 1. **Form data**: Input a list of tax form names and receive a JSON that includes the title of the form with the minimum and maximum years the form has been available. 
###### 2. **Form PDFs**: Input a tax form name and range of years to download all the PDF forms available within that time frame. 

#### Installation instructions / Run Instructions
###### This project was made with Python version 3.6.9
###### Start up a virtual environment, install requirements, and run the file. From here, you will be prompted to input lists or text to run the programs. 
###### For **form data**, you can add your list to the variable at the top of the file named "tax_forms_to_check" and run the file in the command line. This will return a list with JSON and the appropriate data.
###### For **form PDFs**, after running the file in the command line will be prompted via CLI to input data. These are the prompts:
###### 1. You'll be able to download all the available PDFs for a given tax form within a time frame of your choosing. What is the name of the tax form you'd like to download? (Ex: Form W-2)
###### 2. What year would you like the downloads to start at?
###### 3. Up until which year should be included?

#### Approaches & Trade Offs
###### I'm pleased the outputs are correct. With more time, for the **form data** I would have added testing with handling for edge cases, especially for user input like misspelling and empty lists. For the **form PDFs** I would have added more tests in general with better detailed error and completion messaging to the user. 

#### Thank you so much for your time, I had a lot of fun working on this project!