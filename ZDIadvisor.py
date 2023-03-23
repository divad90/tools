#!/usr/bin/env python

"""
ZDIadvisor.py: It saves in a csv file all ZDI advisories.
Saving the following values:
ZDI ID	
ZDI CAN	
AFFECTED VENDOR(S)	
CVE	
CVSS v3.0	
PUBLISHED	
UPDATED	
TITLE	
URL
"""
__author__      = "Dbad"

import requests
from bs4 import BeautifulSoup
import csv

url_base = "https://www.zerodayinitiative.com/"
url = url_base + "advisories/published/"

# Get the HTML content of the page
response = requests.get(url)
html = response.content

# Create a BeautifulSoup object with the obtained HTML
soup = BeautifulSoup(html, "html.parser")

# Find all options in the select with id "select-year"
options = soup.find("select", {"id": "select-year"}).find_all("option")

# Create a list to store the values
values = []

print("[+] Finding all years...", end="")
# Add the values to the list
for option in options:
    value = option["value"]
    values.append(value)
print(" done")

# Create CSV file
csv_file = open("zdi_advisories.csv", mode="w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)

# Make HTTP requests for each year in the list
for value in values:
    # Combine the base URL with the current year
    url_with_year = url + value + "/"
    print("[+] opening " + url_with_year)
    # Make the HTTP request
    response = requests.get(url_with_year)

    # Parse the HTML of the response to obtain the table with id="search-table"
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "search-table"})

    # Get the <th> and <td> tags of the table and display their values
    if table:
        headers = table.find_all("th")
        header_values = []
        for header in headers:
            header_values.append(header.text.strip())
        header_values.append("URL")
        writer.writerow(header_values)

        rows = table.find_all("tr")
        for row in rows[1:]:
            cell_values = []
            cells = row.find_all("td")
            for cell in cells:
                if cell.find("a"):
                    # Get the full URL and the cell value
                    url_post = cell.find("a")["href"]
                    cell_value = cell.get_text(strip=True)
                    # Write the full URL and the cell value
                    cell_values.append(cell_value)
                    cell_values.append(url_base + url_post)
                else:
                    cell_values.append(cell.text.strip())
            writer.writerow(cell_values)
    else:
        print("[ERROR] The table with id=\"search-table\" was not found")

# Close the CSV file
csv_file.close()
