import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from datetime import datetime

# Authenticate Google Sheets API
def authenticate_google_sheets():
    # Use the credentials from the downloaded JSON key
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Function to get existing sheet data
def get_sheet_data():
    client = authenticate_google_sheets()
    sheet = client.open("Bill Tracker").sheet1  # Open the first sheet
    data = sheet.get_all_records()  # Retrieve all records as a list of dictionaries
    return data

# Function to update the Google Sheet with new data
def update_sheet(date, cash, spam_amounts, total_spam, daily_total):
    client = authenticate_google_sheets()
    sheet = client.open("Bill Tracker").sheet1  # Open the first sheet
    sheet.append_row([date, cash, ', '.join(map(str, spam_amounts)), total_spam, daily_total])

# Streamlit UI
st.title("Bill Tracker")

# Date input
date = st.date_input("Select Date", datetime.today())

# Cash input
cash = st.number_input("Enter Total Cash", min_value=0, step=1)

# Spam amounts input (each separated by a comma)
spam_input = st.text_area("Enter Spam Amounts (comma separated)")
if spam_input:
    spam_amounts = list(map(int, spam_input.split(',')))
    total_spam = sum(spam_amounts)
else:
    spam_amounts = []
    total_spam = 0

# Calculate the daily total
daily_total = cash + total_spam

# Show the results
st.write(f"**Total Spam**: {total_spam}")
st.write(f"**Total Cash**: {cash}")
st.write(f"**Daily Total**: {daily_total}")

# Button to save data to Google Sheets
if st.button('Save to Google Sheets'):
    update_sheet(date, cash, spam_amounts, total_spam, daily_total)
    st.success("Data saved successfully!")
