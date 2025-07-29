import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Authenticate Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Function to get data from Google Sheets
def get_sheet_data():
    client = authenticate_google_sheets()
    sheet = client.open("Bill Tracker").sheet1
    data = sheet.get_all_records()
    return data

# Function to update Google Sheet with new data
def update_sheet(date, cash, spam_amounts, total_spam, daily_total):
    client = authenticate_google_sheets()
    sheet = client.open("Bill Tracker").sheet1
    sheet.append_row([date, cash, ', '.join(map(str, spam_amounts)), total_spam, daily_total])

# Streamlit UI Setup
st.title("Bill Tracker")

# Sidebar for navigation
st.sidebar.title("Navigate Between Days")
day_selection = st.sidebar.selectbox('Select Day', ['2025-07-29', '2025-07-30', '2025-07-31'])

# Date input
date = st.date_input("Select Date", datetime.today())

# Cash input
cash = st.number_input("Enter Total Cash", min_value=0, step=1)

# Dynamic Spam Amount Inputs: 5 fields initially
spam_input_1 = st.number_input("Enter Spam Amount 1", min_value=0, step=1)
spam_input_2 = st.number_input("Enter Spam Amount 2", min_value=0, step=1)
spam_input_3 = st.number_input("Enter Spam Amount 3", min_value=0, step=1)
spam_input_4 = st.number_input("Enter Spam Amount 4", min_value=0, step=1)
spam_input_5 = st.number_input("Enter Spam Amount 5", min_value=0, step=1)

# Display more spam fields if needed:
if st.button('Add More Spam Amounts'):
    spam_input_6 = st.number_input("Enter Spam Amount 6", min_value=0, step=1)
    spam_input_7 = st.number_input("Enter Spam Amount 7", min_value=0, step=1)
    spam_input_8 = st.number_input("Enter Spam Amount 8", min_value=0, step=1)
    spam_input_9 = st.number_input("Enter Spam Amount 9", min_value=0, step=1)
    spam_input_10 = st.number_input("Enter Spam Amount 10", min_value=0, step=1)
else:
    spam_input_6 = spam_input_7 = spam_input_8 = spam_input_9 = spam_input_10 = None

# Collect all spam inputs
spam_amounts = [spam_input_1, spam_input_2, spam_input_3, spam_input_4, spam_input_5]
if spam_input_6 is not None:
    spam_amounts.extend([spam_input_6, spam_input_7, spam_input_8, spam_input_9, spam_input_10])

# Calculate total spam
total_spam = sum(spam_amounts)

# Calculate daily total
daily_total = cash + total_spam

# Show results
st.write(f"**Total Spam**: {total_spam}")
st.write(f"**Total Cash**: {cash}")
st.write(f"**Daily Total**: {daily_total}")

# Button to save data to Google Sheets
if st.button('Save to Google Sheets'):
    update_sheet(date, cash, spam_amounts, total_spam, daily_total)
    st.success("Data saved successfully!")

# Show recorded data for the selected day
st.write(f"### Data for {day_selection}:")
data = get_sheet_data()

# Filter data for the selected day
filtered_data = [entry for entry in data if entry['Date'] == day_selection]

# Display the data
if filtered_data:
    st.write(f"**Date**: {filtered_data[0]['Date']}")
    st.write(f"**Total Cash**: {filtered_data[0]['Total Cash']}")
    st.write(f"**Spam Amounts**: {filtered_data[0]['Spam Amounts']}")
    st.write(f"**Total Spam**: {filtered_data[0]['Total Spam']}")
    st.write(f"**Daily Total**: {filtered_data[0]['Daily Total']}")
else:
    st.write("No data found for this day.")
