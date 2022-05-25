# -*- coding: utf-8 -*-
"""

YEO! WEEKIANG TO [SPEND & TRACK]
This programme is designed to assist companies in the tracking of business expenses.
[SPEND & TRACK] is proudly developed by AB0403 SG12 Team 6.

"""

import sys
import datetime
import pandas as pd


### OBTAINING USER DETAILS
def password_check():
  employee_password_input = input("Please enter your password: ")
  while employee_password_input != employees_information[employee_ID_new]["Password"]:
      employee_password_input = input("You have entered the wrong password. Please try again: ")
  print("Password is correct")
  return

def password_creator():
  employees_information[employee_ID_new] = {}
  employee_password_new = input("Please enter your new password: ")
  while len(employee_password_new) < 8:
      print("Password should have at least 8 characters.")
      employee_password_new = input("Please enter your new password: ")
  employee_password_repeat = input("Please confirm your new password: ")
  while employee_password_new != employee_password_repeat:
    employee_password_repeat = input("Please re-confirm your new password: ")
  employees_information[employee_ID_new]["Password"] = employee_password_new
  print("Password created successfully!")
  return

def get_name():
  employee_name_new = input("What is your name? ")
  while employee_name_new.isalpha() is False:
        print("Only alphabets are allowed.")
        employee_name_new = input("What is your name? ")
  employees_information[employee_ID_new]["Name"] = employee_name_new
  return
    

def get_position():
  employee_position_new = input("Please enter your position (Intern/Associate/Manager/Senior Manager) ")
  while True:
    if employee_position_new.lower() in positions:
      employees_information[employee_ID_new]["Position"] = employee_position_new.lower()
      break
    else:
      employee_position_new = input("You have entered an invalid position. Please enter your position again (Intern/Associate/Manager/Senior Manager) ")
  return

def get_department():
  employee_department_new = input("Please enter your department (Finance/Marketing/Sales/Human Resource) ")
  while True:
    if employee_department_new.lower() in departments:
      employees_information[employee_ID_new]["Department"] = employee_department_new.lower()
      return
    else:
      employee_department_new = input("You have entered an invalid entry.\nPlease enter your department (Finance/Marketing/Sales/Human Resource) ")
  return

### KEY ACTIONS
def budget_balance_updater_temp(dept,mth,amt):
    departmental_budget_balance_temp = departmental_budget_balance[mth][dept]["Remaining"] - amt
    running_low = departmental_budget_balance_temp <= 0.05*departmental_budget_balance[mth][dept]["Beginning"]
    exceed = departmental_budget_balance_temp < 0       
    return (running_low, exceed)


def store_transaction(dept,cat,trc_date,amt,ent_date):
  details = [dept,cat,trc_date,amt,ent_date]
  transaction_code = len(expense_history)
  expense_history[transaction_code] = details
  return transaction_code
  

def view_budget():
    viewing_month = input("Please enter the month you would like to view in MMM format: ").upper()
    while viewing_month not in months:
        viewing_month = input("You have entered an invalid month. Please enter the month in which the expense was incurred in MMM format: ").upper()
    
    if employees_information[employee_ID_new]["Department"] == "finance":
        print("-"*30)
        print(f"BUDGET RECORDS ({viewing_month.upper()})")
        for key, value in departmental_budget_balance[viewing_month].items():
            print("Beginning Budget ({}): ${:>10,.2f}".format(key.upper(),value["Beginning"]))
            print("Remaining Budget ({}): ${:>10,.2f}".format(key.upper(),value["Remaining"]))
            
        print("-"*30)
        return
    else:
        department_selection = employees_information[employee_ID_new]["Department"]
        amount_beginning = departmental_budget_balance[viewing_month][department_selection]["Beginning"]
        amount_remaining = departmental_budget_balance[viewing_month][department_selection]["Remaining"]
        print("-"*30)
        print(f"BUDGET RECORDS ({viewing_month.upper()})")
        print(f"Beginning Budget ({department_selection.upper()}): ${amount_beginning:>10,.2f}")
        print(f"Remaining Budget ({department_selection.upper()}): ${amount_remaining:>10,.2f}")
        print("-"*30)
        return    
    
    
def expense_entry():
    # Obtaining department
    user_dept = employees_information[employee_ID_new]["Department"]
    if user_dept == "finance":
        expense_department = input("Which department would you like to enter the expense item for?\n")
        while expense_department.lower() not in departments:
            print("You have entered an invalid department. Please try again.")
            expense_department = input("Which department would you like to enter the expense item for?\n")
    else:
        expense_department = user_dept
    
    # Obtaining expense category
    while True:
        try:
            expense_category = int(input(f"""Please select the category of expense:
1) {expense_categories[0]}
2) {expense_categories[1]}
3) {expense_categories[2]}
4) {expense_categories[3]}
5) {expense_categories[4]}
Selection: """))
            if expense_category in range(1,6):
                break
            else:
                print("\nYou have keyed in an invalid response. Please key in a valid number from 1 to 5.")
        except ValueError:
            print("\nYou have keyed in an invalid response. Please try again.")
        
    expense_category = expense_categories[expense_category-1]
    
    # Obtaining expense date
    spending_month = input("Please enter the month in which the expense was incurred in MMM format: ").upper()
    while spending_month not in months:
        spending_month = input("You have entered an invalid month. Please enter the month in which the expense was incurred in MMM format: ").upper()
    while True:        
        try:
            spending_day = int(input("Please enter the date on which the expense was incurred in DD format: "))
            while spending_day > 31 or spending_day < 1:
                spending_day = int(input("You have entered an invalid date. Please enter the date on which the expense was incurred in DD format: "))
            while spending_month in ["FEB","APR","JUN","SEP","NOV"] and spending_day == 31:
                spending_day = int(input("You have entered an invalid date. Please enter the date on which the expense was incurred in DD format: "))
            while spending_month == "FEB" and spending_day > 28:
                spending_day = int(input("You have entered an invalid date. Please enter the date on which the expense was incurred in DD format: "))
            break
        except ValueError:
            print("\nInvalid response received.")
        
    spending_date = str(spending_day) +" "+ spending_month
    print(f"\nTransaction Date: {spending_date:>10s}")
    
    
    # Obtaining expense amount
    while True:
        try:
            expense_amount = float(input("What is the amount of expense you would like to record?\nAmount of Expense: $ "))
            break
        except ValueError:
            print("You have entered an invalid amount. Please key in a valid number.")
    
    (running_low,exceed) = budget_balance_updater_temp(expense_department,spending_month,expense_amount)
    if exceed:
        print("Entry has failed. Expense entry will exceed budget.")
        return
    elif running_low:
        print("-"*30)
        print("WARNING: Budget is running low.")
                
    
    # Obtaining date
    entry_date = datetime.datetime.now().strftime("%d %B %y")
    
        
    # Confirmation of entry
    print("-"*30)
    print(f"""\nSUMMARY OF EXPENSE ENTRY:\n
Department: {expense_department.upper()}
Category: {expense_category.upper()}
Spending Date: {spending_date}
Amount: ${expense_amount:>10,.2f}

Recorded by: {employees_information[employee_ID_new]["Name"]}
Date: {entry_date}\n
 """)
    print("-"*30)
    
    user_input = input("Would you like to confirm the recording of this expense entry? Y/N\n").upper()
    while user_input != "Y" and user_input != "N":
        user_input = input("Invalid response entered. Please try again.\nWould you like to confirm the recording of this expense entry? Y/N\n").upper()
    
    if user_input == "N":
        print("\nAction cancelled.\n")
        return
    
    departmental_budget_balance[spending_month][expense_department]["Remaining"] -= expense_amount

    trans_code = store_transaction(expense_department,expense_category,spending_date,expense_amount,entry_date)
    print("-"*30)
    print(f"Transaction Code: {trans_code:>10}")
    
    print("\nThe budget balance for the {} department has been updated.\nThere is ${:,.2f} remaining for the month of {}.".format(expense_department,departmental_budget_balance[spending_month][expense_department]["Remaining"],spending_month))
    
    return

    
def edit_budget():
    dept = employees_information[employee_ID_new]["Department"]
    pos = employees_information[employee_ID_new]["Position"]
    if pos == "manager" or pos == "senior manager":
        if dept == "finance":
            while True:
                edit_department = input("Which department would you like to edit the beginning budget for?\n")
                if edit_department.lower() in departments:
                    break
                else:
                    print("You have entered an invalid department. Please try again.")

        else:
            edit_department = dept


        edit_month = input("Which month would you like to edit the budget for? Please enter your selection in MMM format: ").upper()
        while edit_month not in months:
            edit_month = input("You have entered an invalid month. Please enter the month in which the expense was incurred in MMM format: ").upper()
        print("-"*30)
        print("{} DEPARTMENT\nBeginning Budget ({}): ${:10,.2f}".format(edit_department.upper(),edit_month,departmental_budget_balance[edit_month][edit_department]["Beginning"]))
        print("-"*30)
        while True:
            try:
                edit_amount = float(input("What would you like to change the amount to?\nNew Beginning Budget: $"))
                break
            except ValueError:
                print("You have entered an invalid response. Please try again.")
        confirmation = input("""This will be the new budget for the {} department:
              
Beginning budget ({}): ${:>10,.2f}

Do you wish to confirm the changes? Y/N\n""".format(edit_department,edit_month,edit_amount)).upper()
        
            
    
        while confirmation not in ["Y","N"]:
            confirmation = input("You have entered an invalid response. Please try again.\n")
        if confirmation == "Y":
            net_change = edit_amount - departmental_budget_balance[edit_month][edit_department]["Beginning"]
            departmental_budget_balance[edit_month][edit_department]["Beginning"] += net_change
            departmental_budget_balance[edit_month][edit_department]["Remaining"] += net_change
            print("-"*30)

            
            print("""{} DEPARTMENT (UPDATED):
Beginning Budget: ({}): ${:>10,.2f}
Remaining Budget: ({}): ${:>10,.2f}\n""".format(edit_department.upper(),edit_month,edit_amount,edit_month,departmental_budget_balance[edit_month][edit_department]["Remaining"]))
            print("-"*30)
            return
        else:
            print("\nAction cancelled.\n")
            return
    else:
        print("\nERROR:\nYou are not authorized to perform this action. Only employees ranked 'manager' and above are allowed to edit the budget.\n")
        return


def edit_existing_expense_entry():
  user_dept = employees_information[employee_ID_new]["Department"]
  if user_dept != "finance":
        print("You are not authorized to edit expense entries. Please contact the finance department for further assistance.")
        return
      
  while True:
      try:
        transaction_code = int(input("Please enter transaction code: "))
        if transaction_code in expense_history.keys():    
            break
        else: 
            print("This transaction code does not exist. Please try again.")
      except ValueError:
        print("Invalid transaction code entered. Please try again: ")
    
  print("-"*30)  
  print(f"""EXISTING EXPENSE ENTRY:
        Transaction Code: {transaction_code}
        Department: {expense_history[transaction_code][0]}
        Expense Category: {expense_history[transaction_code][1]}
        Spending Date: {expense_history[transaction_code][2]}
        Amount: ${expense_history[transaction_code][3]:>10,.2f}
        Entry Date: {expense_history[transaction_code][4]}""")
  print("-"*30)
  while True:
      confirmation = input("Do you wish to edit the entry? Y/N\n").upper()
      if confirmation in ["Y","N"]:
          break
      else:
          confirmation = input("You have entered an invalid response. Please try again.\n").upper()
  if confirmation == "N":
      print("\nAction cancelled.\n")
      return    
  elif confirmation == "Y":
    while True:
        try:
          edit_amount = float(input("Enter new expense amount: $"))
          break
        except ValueError:
          print("You have entered an invalid value. Please try again.") 
    net_change_amount = edit_amount - expense_history[transaction_code][3]
    (running_low,exceed) = budget_balance_updater_temp(expense_history[transaction_code][0],expense_history[transaction_code][2][-3:],net_change_amount)
    if exceed:
        print("Adjustment has failed. Expense entry will exceed budget.")
        return
    elif running_low:
        print("-"*30)
        print("WARNING: Budget is running low.")
        print("-"*30)
    
    # Update Data
    departmental_budget_balance[expense_history[transaction_code][2][-3:]][expense_history[transaction_code][0]]["Remaining"] -= net_change_amount

    expense_history[transaction_code][3] = edit_amount
    expense_history[transaction_code][4] = datetime.datetime.now().strftime("%d %B %y")
    print("-"*30)
    print(f"""UPDATED EXPENSE ENTRY:
        Transaction Code: {transaction_code}
        Department: {expense_history[transaction_code][0]}
        Expense Category: {expense_history[transaction_code][1]}
        Spending Date: {expense_history[transaction_code][2]}
        Amount: ${expense_history[transaction_code][3]:>10,.2f}
        Entry Date: {expense_history[transaction_code][4]}""")
    print("-"*30)

  return


def export_data():
    user_dept = employees_information[employee_ID_new]["Department"]
    
    export_selection = input("""What data would you like to export?
[1] Monthly expense history
[2] Employee data\n
Selection: """)
    while export_selection not in ["1","2"]:
        export_selection = input("Invalid response received. Please try again: ")
    
    if export_selection == "1":
        if user_dept == "finance":
            expense_department_export = input("""Which department's data would you like to export?
[1] Finance
[2] Marketing
[3] Sales
[4] Human Resource
Selection: """)
            while expense_department_export not in ["1","2","3","4"]:
                expense_department_export = input("Invalid response received. Please try again: ")
            
            if expense_department_export == "1":
                expense_department_export = "finance"
            elif expense_department_export == "2":
                expense_department_export = "marketing"
            elif expense_department_export == "3":
                expense_department_export = "sales"
            elif expense_department_export == "4":
                expense_department_export = "human resource"
            
        else:
            expense_department_export = user_dept
            
        expense_month_export = input("Which month would you like to export data for? Please enter your selection in MMM format: ").upper()
        while expense_month_export not in months:
            expense_month_export = input("You have entered an invalid month. Please enter the month in which the expense was incurred in MMM format: ").upper()
        
               
        # create DF
        df_expense_history = pd.DataFrame.from_dict(expense_history, orient='index', columns=["department","category","spending_date","amount","entry_date"])
        df_expense_export = df_expense_history[df_expense_history["department"]==expense_department_export]
        df_expense_export = df_expense_export[df_expense_export["spending_date"].str.contains(expense_month_export)]
        df_expense_export.loc['Total'] = pd.Series(df_expense_export['amount'].sum(), index = ['amount'])
       
        df_expense_export.to_csv(f"{expense_department_export}_{expense_month_export}_expenses.csv")
        print("Your data has been exported.")
    
    
    else:
        if user_dept == "human resource":
            df_employees_info = pd.DataFrame(employees_information)
            df_employees_info = df_employees_info.T
            df_employees_info.to_csv("employees_info.csv")
            print("Your data has been exported.")
            
        else:
            print("You are not allowed to export employee data. Please contact the human resource department.")    
    return


def programme_end():
    print("Thank you and have a nice day!")
    sys.exit()
    return

def programme_start():
    while True:
        print("-"*30)
        print("Welcome,", employees_information[employee_ID_new]["Name"]+"!")
        user_input = input("""What would you like to do today?
[1] View budget
[2] Key in an expense entry
[3] Edit budget
[4] Edit existing expense entry
[5] Export data
[6] End programme
Selection: """)
        if user_input == "1":
            view_budget()
        elif user_input == "2":
            expense_entry()
        elif user_input == "3":
            edit_budget()
        elif user_input == "4":
            edit_existing_expense_entry()
        elif user_input == "5":
            export_data()
        elif user_input == "6":
            programme_end()
        else:
            print("You have keyed in an invalid response. Please try again.")
            
### Database Set Up

positions = ["intern", "associate", "manager", "senior manager"]
departments = ["finance", "marketing", "sales", "human resource"]
expense_categories = ["Stationery","Salary","Marketing","Miscellaneous","Others"]
months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


departmental_monthly_budget = {"finance":5000, "marketing":10000, "sales":2000, "human resource":2000}


departmental_budget_balance = {}
for month in months:
    departmental_budget_balance[month] = {}
    for dept, budg in departmental_monthly_budget.items():
        departmental_budget_balance[month][dept] = {"Beginning":budg, "Remaining":budg}


employees_information = {"s01":{"Password":"password1",
                               "Name":"Sandra",
                               "Department":"sales",
                               "Position":"manager"},
                         "f02":{"Password":"password2",
                               "Name":"Fred",
                               "Department":"finance",
                               "Position":"senior manager"},
                         "h03":{"Password":"password3",
                               "Name":"Hazel",
                               "Department":"human resource",
                               "Position":"associate"},
                         "m04":{"Password":"password4",
                               "Name":"Mabel",
                               "Department":"marketing",
                               "Position":"intern"}
                               }


expense_history = {'placeholder':[0,0,0,0,0]}

### Programme Start

# Logging In

employee_input = input("Welcome! Are you a new user? Y/N  ").upper()
# NEW USER
while employee_input not in ["Y","N"]:
    employee_input = input("Invalid response received. Please try again.\n").upper()

if employee_input.upper() == "Y":
  employee_ID_new = input("Please enter your new employee ID: ").lower()
  # Check if is actually existing user
  if employee_ID_new in employees_information.keys():
    print("You are an existing user!")
    password_check()
  else:
      password_creator()
      get_name()
      get_position()
      get_department()
  
  print(f"""========================\nEmployee Record Summary:\n========================
Employee ID: {employee_ID_new}
Password: {employees_information[employee_ID_new]["Password"]}
Employee Name: {employees_information[employee_ID_new]["Name"]}
Employee Position: {employees_information[employee_ID_new]["Position"]}
Employee Department: {employees_information[employee_ID_new]["Department"]}""")


else:
  employee_ID_new = input("Please enter your employee ID: ").lower()
  if employee_ID_new in employees_information.keys():
    password_check()
  else:
    print("Sorry! Your ID does not exist. Please create a new account.")
    password_creator()
    get_name()
    get_position()
    get_department()
    print(f"""========================\nEmployee Record Summary:\n========================
Employee ID: {employee_ID_new}
Password: {employees_information[employee_ID_new]["Password"]}
Employee Name: {employees_information[employee_ID_new]["Name"]}
Employee Position: {employees_information[employee_ID_new]["Position"]}
Employee Department: {employees_information[employee_ID_new]["Department"]}""")

# Getting user activity
programme_start()

