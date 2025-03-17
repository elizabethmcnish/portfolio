from splitwise_client import Client
import logging
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

GROUP_NAME_STR = "Grosvenor Baddies 😝"

# Define the scope
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Authenticate with credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name("gsheets_credentials.json", scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/19ZFo45Vo0wV6TvmrUUbL2F-h7tMlZAD_142eBFME0qM/edit?gid=406458046#gid=406458046"
)

# Initiate splitwise client
splitwise_client = Client()
expenses = splitwise_client.get_group_expenses_by_name(GROUP_NAME_STR)


# Writing the .csv file from the list[dict] data
columns = expenses[0].keys()

with open("splitwise.csv", "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, columns)
    dict_writer.writeheader()
    dict_writer.writerows(expenses)

# Reading back
with open("splitwise.csv", "r", encoding="utf-8") as input_file:
    reader = csv.reader(input_file)
    csv_data = list(reader)

new_worksheet = spreadsheet.add_worksheet(title=f"Splitwise Data {datetime.now()}", rows="1000", cols="26").update(
    values=csv_data
)
