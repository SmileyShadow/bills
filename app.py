import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Authenticate Google Sheets API
def authenticate_google_sheets():
    try:
        # Define the scope and authenticate using the credentials JSON file
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)  # Ensure credentials.json is uploaded
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        return None

# Function to get data from Google Sheets
def get_sheet_data():
    client = authenticate_google_sheets()
    if client:
        try:
            # Open the Google Sheet (make sure it's named correctly)
            sheet = client.open("Bill Tracker").sheet1  # Change if the name is different
            data = sheet.get_all_records()  # Get all rows of data
            return data
        except Exception as e:
            st.error(f"Error fetching data from Google Sheets: {e}")
            return []
    else:
        return []

# Function to update Google Sheet with new data
def update_sheet(date, cash, spam_amounts, total_spam, daily_total):
    client = authenticate_google_sheets()
    if client:
        try:
            sheet = client.open("Bill Tracker").sheet1  # Open the first sheet
            sheet.append_row([date, cash, ', '.join(map(str, spam_amounts)), total_spam, daily_total])
        except Exception as e:
            st.error(f"Error saving data to Google Sheets: {e}")
    else:
        st.error("Could not authenticate with Google Sheets.")

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
    if len(spam_amounts) < 15:  # Limit the number of fields to 15
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
