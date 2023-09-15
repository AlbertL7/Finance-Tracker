# Finance-Tracker

#Project Description

This is a Financial Tracking App written in Python that allows users to manage their income and expenses. The application stores records for each month and year and can generate CSV files for data persistence. Users can add, list, and delete financial records, as well as view them by category. The application is user-friendly and provides prompts to guide the user through different actions.

## Requirements
- Python 3.x
- CSV files for record storage (automatically generated)
## Features
- Add new financial records with date, description, amount, type (Income/Expense), and category.
- List all records by month and year.
- Save records to a CSV file.
- Show totals for income, expenses, and money left.
- Load existing records from a selected CSV file.
- Delete a specific financial record.
- Show expenses by category.
## Usage

Simply run the Python script, and you will be presented with a menu to:

1. Add New Record:
Allows you to add a new financial record. You'll be prompted to enter the date, description, amount, type (Income/Expense), and optionally, a category if it's an expense.

2. List All Records:
Displays all the financial records you have entered, sorted by month and year.

3. Save to CSV:
Saves all your financial records into a CSV file. Each month and year's records will be saved into a separate CSV file named accordingly (e.g., financial_records_YYYY-MM.csv).

4. Show Totals:
Calculates and displays the total income, expenses, and the remaining balance (money left) for each month and year.

5. Exit:
Exits the application, terminating the program.

6. Load / Select Existing CSV File:
Lists all the available CSV files that match the naming convention for the financial records. Allows you to select one to load its records into the application.

7. Delete Record:
Allows you to delete a specific financial record. You'll be prompted to select which record to delete by providing the record's number and the month-year it belongs to.

8. Show Expenses by Category:
Calculates and displays the total amount spent in each expense category, such as Food, Bills, Subscriptions, etc.

9. Create New CSV File:
Create a CSV file with your own naming convention.

## Updates
Updated to include new categories
  - health, Medical, Gas, Car Maintenance and repaid, Travel
- Option to exit "Add New Record" once "Add New Record" has been initiated by typing "back"
- Create a CSV with your own naming convention. Old default naming still exists and works.
- Warning message for over writing already created csv files with default naming convention.

## Future Features to Add
- Add A help page with directions on how to use the program and how each feature works
- *Add Feature to compare totals between multiple differetn spread sheets
