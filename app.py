import streamlit as st
from counter import DailyCounter

# Initialize counter
counter = DailyCounter()

# App title
st.title("📊 Daily Counter Calculator")
st.subheader("Track cash and SPAN values")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Entry", "Update Cash", "Add Item", "View Data", "Delete Entry"]
)

if menu == "Add Entry":
    st.header("Add New Date Entry")
    date = st.text_input("Date (DD/MM/YYYY)")
    if st.button("Add Date"):
        try:
            result = counter.add_entry(date)
            st.success(result)
        except ValueError as e:
            st.error(str(e))

elif menu == "Update Cash":
    st.header("Update Cash Amount")
    date = st.text_input("Date (DD/MM/YYYY)")
    amount = st.number_input("Cash Amount", min_value=0.0, step=0.01)
    if st.button("Update Cash"):
        try:
            result = counter.update_cash(date, amount)
            st.success(result)
        except ValueError as e:
            st.error(str(e))

elif menu == "Add Item":
    st.header("Add/Update Item")
    date = st.text_input("Date (DD/MM/YYYY)")
    item_num = st.text_input("Item Number")
    amount = st.number_input("Item Amount", min_value=0.0, step=0.01)
    if st.button("Update Item"):
        try:
            result = counter.add_item(date, item_num, amount)
            st.success(f"{result['message']} - New SPAN: {result['span']}")
        except ValueError as e:
            st.error(str(e))

elif menu == "View Data":
    st.header("All Data")
    data = counter.get_all_data()
    if not data:
        st.info("No data available")
    else:
        # Convert to DataFrame for nice display
        import pandas as pd
        df_data = []
        for date, values in data.items():
            row = {
                'DATE': date,
                'CASH': values['CASH'],
                'SPAN': values['SPAN']
            }
            row.update(values['items'])
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        st.dataframe(df.fillna(''))

elif menu == "Delete Entry":
    st.header("Delete Entry")
    date = st.text_input("Date to delete (DD/MM/YYYY)")
    if st.button("Delete"):
        try:
            result = counter.delete_entry(date)
            st.success(result)
        except ValueError as e:
            st.error(str(e))

# Add some instructions
st.sidebar.markdown("""
### Instructions
1. Use DD/MM/YYYY date format
2. SPAN is automatically calculated
3. Data is saved automatically
""")
