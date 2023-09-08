import csv
from collections import defaultdict
import os
from datetime import datetime

# Initialize a dictionary to hold financial records, keyed by month and year
financial_records_by_month = defaultdict(list)

# Create a dictionary to store expenses by category
expenses_by_category = defaultdict(float)

# Function to list and select existing CSV files
def select_csv_file():
    try:
        csv_files = [f for f in os.listdir('.') if f.startswith("financial_records_") and f.endswith(".csv")]
    except IOError as e:
        print(f"An error occurred while reading the directory: {e}")
        return
    
    csv_files = [f for f in os.listdir('.') if f.startswith("financial_records_") and f.endswith(".csv")]
    
    if not csv_files:
        print("No existing CSV files found.")
        return
    
    print("\nAvailable CSV Files:")
    for i, filename in enumerate(csv_files, 1):
        print(f"{i}. {filename}")
    
    choice = int(input("Select a file to load (Enter the number): "))
    if choice < 1 or choice > len(csv_files):
        print("Invalid choice.")
        return
    
    selected_file = csv_files[choice - 1]
    load_existing_records(selected_file)

# Function to load existing records from a selected CSV file
def load_existing_records(filename):
    try:
        with open(filename, 'r') as f:
            month_year = filename[18:-4]  # Extract YYYY-MM from filename
            financial_records_by_month[month_year] = []  # Empty existing records for this month-year
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row['Date'].startswith('Total'):  # Ignore rows starting with "Total"
                        try:
                            row['Amount'] = float(row['Amount'])
                            financial_records_by_month[month_year].append(row)
                        except ValueError:
                            print(f"Error converting 'Amount' to float for row: {row}")
            print(f"Records from {filename} loaded successfully.")
    except ValueError:
        print("Invalid amount entered. Record not added.")
        return
# Function to display menu options
def display_menu():
    print("\nFinancial Tracking App")
    print("1. Add New Record")
    print("2. List All Records")
    print("3. Save to CSV")
    print("4. Show Totals")
    print("5. Exit")
    print("6. Select CSV File")
    print("7. Delete Record")  # New option to delete a record
    print("8. Show Expenses by Category")  # New option to display expenses by category
    choice = input("Enter your choice: ")
    return choice

# Function to add a new financial record with a category
def add_record():
    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    description = input("Enter the description: ")
    
    while True:
        try:
            amount = float(input("Enter the amount: "))

             # Check if the amount exceeds 2 decimal places
            if float('{:.2f}'.format(amount)) != amount:
                print("Amount should not exceed 2 decimal places. Try again.")
                continue  # Continue the loop if amount is invalid
            break
        except ValueError:
            print("Invalid amount entered. Record not added.")
            return
    
    record_type = input("Is this income or expense? (I/E): ")

    # Initialize category as 'N/A' (or any placeholder you like)
    category = 'N/A'

    if record_type.lower() == 'e':  # Only ask for category if it's an expense
        # Prompt the user for the category
        print("Expense Categories:")
        print("1. Bills")
        print("2. Food")
        print("3. Subscriptions")
        print("4. School")
        print("5. Business")
        print("6. Work")
        print("7. Investment")
        print("8. Random")
        category_choice = input("Select the category (1-8): ")
    
        category_names = ["Bills", "Food", "Subscriptions", "School", "Business", "Work", "Investment", "Random"]
        category = category_names[int(category_choice) - 1] if category_choice.isdigit() and 1 <= int(category_choice) <= 8 else "Uncategorized"
    
    record = {
        'Date': date,
        'Description': description,
        'Amount': amount,
        'Type': 'Income' if record_type.lower() == 'i' else 'Expense',
        'Category': category  # Add the selected category to the record
    }
    
    month_year = date[:7]  # Extract YYYY-MM from YYYY-MM-DD
    financial_records_by_month[month_year].append(record)
    print("Record added successfully.")

# Function to save records to a CSV file with expenses by category
def save_to_csv():
    try:
        for month_year, records in financial_records_by_month.items():
            filename = f"financial_records_{month_year}.csv"

            # Extract keys from the first existing record, if available
            keys = records[0].keys() if records else []

            # Overwrite the CSV with only the in-memory records
            with open(filename, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(records)

                # Calculate new totals
                total_income = sum(float(record['Amount']) for record in records if record['Type'] == 'Income')
                total_expense = sum(float(record['Amount']) for record in records if record['Type'] == 'Expense')
                money_left = total_income - total_expense

                # Calculate totals by category
                calculate_expenses_by_category()

                # Write new totals
                output_file.write('\n')
                output_file.write(f"Total Income,,{total_income}\n")
                output_file.write(f"Total Expense,,{total_expense}\n")
                output_file.write("\n")
                output_file.write(f"Total Money Left,,{money_left}\n")
                output_file.write("\n")

                # Write totals by category
                for category, total in expenses_by_category.items():
                    output_file.write(f"Total by Category,{category},{total}\n")

            print(f"Records for {month_year} saved to '{filename}'.")

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
# Function to calculate and aggregate expenses by category
def calculate_expenses_by_category():
    global expenses_by_category  # Use the global variable
    
    # Reset the expenses_by_category dictionary
    expenses_by_category = defaultdict(float)
    
    for month_year, records in financial_records_by_month.items():
        for record in records:
            if record['Type'] == 'Expense':
                category = record['Category']
                amount = record['Amount']
                expenses_by_category[category] += amount

def list_records():
    if not financial_records_by_month:
        print("No records available.")
        return

    for month_year, records in financial_records_by_month.items():
        print(f"\nRecords for {month_year}:")
        print('-' * 50)
        print(f"{'Date':<12} | {'Description':<20} | {'Amount':<10} | {'Type':<8} | {'Category'}")
        print('-' * 50)
        for record in records:
            print(f"{record['Date']:<12} | {record['Description']:<20} | {record['Amount']:<10.2f} | {record['Type']:<8} | {record['Category']}")
        print('-' * 50)

# Function to show total income and expenses
def show_totals():
    print("\nTotal Income, Expenses, and Money Left:")
    for month_year, records in financial_records_by_month.items():
        total_income = sum(record['Amount'] for record in records if record['Type'] == 'Income')
        total_expense = sum(record['Amount'] for record in records if record['Type'] == 'Expense')
        money_left = total_income - total_expense  # Calculate money left
        
        print(f"Month-Year: {month_year}")
        print(f"  Total Income: {total_income:.2f}")
        print(f"  Total Expense: {total_expense:.2f}")
        print(f"  Money Left: {money_left:.2f}")

# Function to delete a financial record
def delete_record():
    try:
        record_index = int(input("Enter the number of the record to delete: ")) - 1
    except ValueError:
        print("Invalid input for record number. No record was deleted.")
        return
    
    month_year = input("Enter the month-year (YYYY-MM) for the record you want to delete: ")
    
    if month_year not in financial_records_by_month:
        print("No records found for the specified month-year.")
        return
    
    records = financial_records_by_month[month_year]
    
    if not records:
        print("No records found for the specified month-year.")
        return
    
    list_records()  # Display all records
    
    record_index = int(input("Enter the number of the record to delete: ")) - 1
    
    if 0 <= record_index < len(records):
        deleted_record = records.pop(record_index)
        print(f"Deleted the following record: {deleted_record}")
        
        # Update the selected CSV file by rewriting it without the deleted record
        selected_csv_file = f"financial_records_{month_year}.csv"
        with open(selected_csv_file, 'w', newline='') as output_file:
            keys = records[0].keys()
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(records)
            
        print(f"Record deleted from '{selected_csv_file}' as well.")
    else:
        print("Invalid record number. No record was deleted.")

try:
# Main program loop
    while True:
        choice = display_menu()
        
        if choice == '1':
            add_record()
        elif choice == '2':
            list_records()
        elif choice == '3':
            if financial_records_by_month:
                save_to_csv()
            else:
                print("No records to save.")
        elif choice == '4':
            if financial_records_by_month:
                show_totals()
            else:
                print("No records to show totals.")
        elif choice == '5':
            print("Exiting the app.")
            break
        elif choice == '6':
            select_csv_file()
        elif choice == '7':
            delete_record()
        elif choice == '8':
            calculate_expenses_by_category()
            print("\nExpenses by Category:")
            for category, total_expense in expenses_by_category.items():
                print(f"{category}: {total_expense:.2f}")
        else:
            print("Invalid choice. Please try again.")

except KeyboardInterrupt:
    print("\nCtrl+C pressed. Exiting the app.")
    # Perform any cleanup here if needed, like saving records to a file        
