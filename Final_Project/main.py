# Ticket Sales Management System
# COMP308 - Programming for Business
# Final Project - Academic Year 2025-2026
# College of Business Administration
# Imam Abdulrahman Bin Faisal University

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Login details
USERNAME = "admin"
PASSWORD = "admin123"
FILE_NAME = "tickets.csv"


# ---------- Login ----------
def login():
    print("===========================================")
    print("   TICKET SALES MANAGEMENT SYSTEM - LOGIN")
    print("===========================================")
    attempts = 0
    while attempts < 3:
        user = input("Username: ")
        pwd = input("Password: ")
        if user == USERNAME and pwd == PASSWORD:
            print("\nLogin successful. Welcome admin!\n")
            return True
        else:
            print("Wrong username or password. Please try again.\n")
            attempts = attempts + 1
    print("Too many failed attempts. Exiting...")
    return False


# ---------- Add a new ticket ----------
def add_ticket():
    df = pd.read_csv(FILE_NAME)

    # Generate next Ticket ID
    if len(df) == 0:
        new_id = 1
    else:
        new_id = int(df["Ticket ID"].max()) + 1

    print("\n--- Add New Ticket ---")
    event = input("Event Name: ")
    customer = input("Customer Name: ")
    date = input("Date of Purchase (YYYY-MM-DD): ")

    # Check date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Ticket not saved.\n")
        return

    # Check price
    try:
        price = float(input("Ticket Price (SAR): "))
        if price <= 0:
            print("Price must be positive. Ticket not saved.\n")
            return
    except ValueError:
        print("Invalid price. Ticket not saved.\n")
        return

    # Check quantity
    try:
        qty = int(input("Quantity: "))
        if qty <= 0:
            print("Quantity must be positive. Ticket not saved.\n")
            return
    except ValueError:
        print("Invalid quantity. Ticket not saved.\n")
        return

    total = price * qty

    # Add to dataframe and save
    new_row = pd.DataFrame([[new_id, event, customer, date, price, qty, total]],
                           columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

    print("\nTicket ID", new_id, "saved. Total cost =", total, "SAR\n")


# ---------- View all tickets ----------
def view_tickets():
    df = pd.read_csv(FILE_NAME)
    if len(df) == 0:
        print("\nNo tickets found.\n")
        return
    print("\n--- All Ticket Records ---")
    print(df)
    print("\nTotal records:", len(df), "\n")


# ---------- Search by Ticket ID ----------
def search_ticket():
    df = pd.read_csv(FILE_NAME)
    try:
        tid = int(input("Enter Ticket ID to search: "))
    except ValueError:
        print("Invalid ID. Please enter a number.\n")
        return

    result = df[df["Ticket ID"] == tid]
    if len(result) == 0:
        print("No ticket found with ID", tid, "\n")
    else:
        print("\n--- Ticket Details ---")
        print(result)
        print()


# ---------- Reports ----------
def produce_reports():
    df = pd.read_csv(FILE_NAME)
    if len(df) == 0:
        print("No data available for reports.\n")
        return

    # Convert date column for grouping
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"])

    # 1) Bar chart - Total tickets sold per event
    sales_by_event = df.groupby("Event Name")["Quantity"].sum()
    print("\n--- Total Tickets Sold by Event ---")
    print(sales_by_event)

    plt.figure(figsize=(9, 5))
    sales_by_event.plot(kind="bar", color="steelblue")
    plt.title("Total Tickets Sold by Event")
    plt.xlabel("Event")
    plt.ylabel("Tickets Sold")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("bar_chart_sales_by_event.png")
    plt.show()

    # 2) Line chart - Sales over time
    sales_over_time = df.groupby("Date of Purchase")["Quantity"].sum()
    print("\n--- Daily Tickets Sold ---")
    print(sales_over_time)

    plt.figure(figsize=(9, 5))
    sales_over_time.plot(kind="line", marker="o", color="green")
    plt.title("Ticket Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Tickets Sold")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("line_chart_sales_over_time.png")
    plt.show()

    # 3) Descriptive statistics
    print("\n--- Descriptive Statistics (Daily Sales) ---")
    print("Mean    :", round(sales_over_time.mean(), 2))
    print("Median  :", round(sales_over_time.median(), 2))
    print("Maximum :", int(sales_over_time.max()))
    print("Minimum :", int(sales_over_time.min()))
    print("Std Dev :", round(sales_over_time.std(), 2))
    print()


# ---------- Main Menu ----------
def main_menu():
    while True:
        print("************MAIN MENU**************")
        print("A: Enter Ticket Details")
        print("B: View Ticket Details")
        print("C: Search by Ticket ID")
        print("D: Produce Reports")
        print("Q: Quit/Log Out")
        choice = input("Please enter your choice: ").upper()

        if choice == "A":
            add_ticket()
        elif choice == "B":
            view_tickets()
        elif choice == "C":
            search_ticket()
        elif choice == "D":
            produce_reports()
        elif choice == "Q":
            print("\nLogged out successfully. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose A, B, C, D or Q.\n")


# ---------- Run program ----------
if not os.path.exists(FILE_NAME):
    print("Error: tickets.csv not found in the project folder.")
else:
    if login():
        main_menu()
