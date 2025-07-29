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

# Dynamic Spam Amount Inputs (5 fields initially)
spam_amounts = []
for i in range(5):
    spam_amounts.append(st.number_input(f"Enter Spam Amount {i+1}", min_value=0, step=1))

# Dynamically add more input fields based on user input
more_spam = True
while more_spam:
    if len(spam_amounts) < 15:
        more_spam = st.button(f"Add More Spam Amounts")
        if more_spam:
            spam_amounts.extend([st.number_input(f"Enter Spam Amount {len(spam_amounts)+1}", min_value=0, step=1) for _ in range(5)])
    else:
        more_spam = False

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
