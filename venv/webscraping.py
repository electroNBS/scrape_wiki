from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
# creating browser object and opening the browser by using selenium
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(start_url)
time.sleep(5)


def scrap():
    headers = ["name", "distance", "mass", "radius"]
    # creating soup object to parse html page
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # in the webpage, we can see that there's only one tbody, so j in tbody refers to each <tr> in the tbody
    for j in soup.find_all("tbody"):
        rowsdata = []
        # row_data contains all the td tags in tr tags
        row_data = j.find_all("td")
        # row extracts only the text part from each td tag
        row = [i.text for i in row_data]
        
        # since upon, printing row, all names had an extra "\n" at the end, I used strip() to remove it
        for  i in row:
            k = str(i)
            final = k.strip("\n")
            #print(final)
            
            #Then, finally, I appended the words to the rowsdata list
            rowsdata.append(final)

    #print(rowsdata)
    # Upon printing rowsdata, we see that the data is not in the form of a list of each row in the table, so I split the entire
    # list into chunks of 8 items, which is in the number of elements in each row in the url's table
    chunks = [rowsdata[x:x+8] for x in range(0, len(rowsdata), 8)]
    #print(chunks)
    counter = 0
    # since I did not need all the columns from the table, I removed the elements which I didn't need from each chunk, using the for loop
    for row in chunks:
        counter += 1
        #print(counter)
        row.pop(0)
        row.pop(1)
        row.pop(2)
        row.pop(4)
        #print(row)
        #print(len(row))
    
    # finally write the data scraped into a csv
    with open("scrapper.csv", "w", encoding="utf-8") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(chunks)
    
    # we see that there are empty lines in the csv, so remove the spaces by index=False and creating a final csv with all the data
    df = pd.read_csv('scrapper.csv')
    df.to_csv('output.csv', index=False)


# Call the function
scrap()
