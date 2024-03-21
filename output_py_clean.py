import pandas as pd
from datetime import datetime

# Set paths and dates
doss = "https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/genAI_out_py/"

# Read in CSV files
customers = pd.read_csv(doss + "customers.csv", delimiter=";")
orders = pd.read_csv(doss + "orders.csv", delimiter=";")

customers = customers.rename(columns={'Customer ID': 'Customer_ID'})
orders["Total_Amount"] = orders["Total_Amount"].astype(str).str.replace(',', '.').astype(float)

# Calculate age of customers
customers["Birthday"] = pd.to_datetime(customers["Birthday"], dayfirst=True)
customers["Age"] = (datetime.now() - customers["Birthday"]).dt.days // 365.25

# Create age range column
customers["Age_range"] = pd.cut(customers["Age"], 
                                bins=[0, 18, 25, 35, 50, 65, float("inf")], 
                                labels=["00-18", "18-25", "25-35", "35-50", "50-65", "65-More"], 
                                right=False)

# Find last order date for each customer
orders["Order_Date"] = pd.to_datetime(orders["Order_Date"], format="%d/%m/%Y")
last_orders = orders.groupby("Customer_ID").agg({"Order_Date": "max"}).reset_index()
last_orders = last_orders.rename(columns={"Order_Date": "Last_order_dt"})

# Merge last order date with customers DataFrame
customers = pd.merge(customers, last_orders, on="Customer_ID", how="left")

# Add VAT tax, weekday, and week number to orders DataFrame
orders["Total_Amount"] = pd.to_numeric(orders["Total_Amount"])
orders["VAT"] = orders["Total_Amount"] / 1.2
orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])
orders["Day"] = orders['Order_Date'].dt.day_name()
orders["Week"] = orders["Order_Date"].dt.isocalendar().week

# Merge customers and orders DataFrames on the "customer_id" column
out1 = pd.merge(customers, orders, on="Customer_ID", how="right")

# Group by the required columns and calculate the sums and counts
out2 = out1.groupby(["Age_range", "Sex", "Day"], observed=True).agg(
    CA_TTC=("Total_Amount", "sum"),
    tot_TVA=("VAT", "sum"),
    nb_cli=("Customer_ID", "nunique"),
    nb_cmd=("Order_ID", "nunique"),
)

#Export the output file
#out2.to_csv('C:/Projects/SAS2PY/Tulku-Code-Repo-main/Tulku/Sas2Py_Repo/OutData/out2.csv', sep=';', index=True)
