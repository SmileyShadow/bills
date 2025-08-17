import csv
from datetime import datetime
import os

class DailyCounter:
    def __init__(self):
        self.data = {}
        self.filename = "daily_counter.csv"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = row['DATE']
                    self.data[date] = {
                        'CASH': float(row['CASH']) if row['CASH'] else 0.0,
                        'SPAN': float(row['SPAN']) if row['SPAN'] else 0.0,
                        'items': {k: float(v) for k, v in row.items() 
                                 if k not in ['DATE', 'CASH', 'SPAN'] and v}
                    }
    
    def save_data(self):
        all_items = set()
        for date in self.data:
            all_items.update(self.data[date]['items'].keys())
        sorted_items = sorted(all_items, key=lambda x: int(x))
        
        fieldnames = ['DATE', 'CASH', 'SPAN'] + sorted_items
        
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for date in sorted(self.data.keys()):
                row = {
                    'DATE': date,
                    'CASH': self.data[date]['CASH'],
                    'SPAN': self.data[date]['SPAN']
                }
                row.update(self.data[date]['items'])
                writer.writerow(row)
    
    def add_entry(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            date_key = date_obj.strftime("%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD/MM/YYYY.")
        
        if date_key in self.data:
            raise ValueError(f"Entry for {date_key} already exists.")
        
        self.data[date_key] = {'CASH': 0.0, 'SPAN': 0.0, 'items': {}}
        self.save_data()
        return f"New entry created for {date_key}"
    
    def update_cash(self, date_str, amount):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            date_key = date_obj.strftime("%d/%m/%Y")
            amount = float(amount)
        except ValueError:
            raise ValueError("Invalid input")
        
        if date_key not in self.data:
            self.data[date_key] = {'CASH': 0.0, 'SPAN': 0.0, 'items': {}}
        
        self.data[date_key]['CASH'] = amount
        self.save_data()
        return f"Cash updated for {date_key}: {amount}"
    
    def add_item(self, date_str, item_number, amount):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            date_key = date_obj.strftime("%d/%m/%Y")
            amount = float(amount)
        except ValueError:
            raise ValueError("Invalid input")
        
        if date_key not in self.data:
            self.data[date_key] = {'CASH': 0.0, 'SPAN': 0.0, 'items': {}}
        
        self.data[date_key]['items'][item_number] = amount
        self.data[date_key]['SPAN'] = sum(self.data[date_key]['items'].values())
        self.save_data()
        return {
            'message': f"Item {item_number} updated for {date_key}",
            'span': self.data[date_key]['SPAN']
        }
    
    def get_all_data(self):
        return self.data
    
    def delete_entry(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            date_key = date_obj.strftime("%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid date format")
        
        if date_key in self.data:
            del self.data[date_key]
            self.save_data()
            return f"Entry for {date_key} deleted"
        else:
            raise ValueError(f"No entry found for {date_key}")
