import pandas as pd
from datetime import datetime

# Set paths and dates
doss = "https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/genAI_out_py/"

# Read in CSV files
out1 = pd.read_csv(doss + "customers.csv", delimiter=";")
out2 = pd.read_csv(doss + "orders.csv", delimiter=";")

out1 = out1.rename(columns={'Customer ID': 'Customer_ID'})
out2["Total_Amount"] = out2["Total_Amount"].astype(str).str.replace(',', '.').astype(float)

# Calculate age of customers
out1["Birthday"] = pd.to_datetime(out1["Birthday"], dayfirst=True)
out1["Age"] = (datetime.now() - out1["Birthday"]).dt.days // 365.25

# Create age range column
out1["Age_range"] = pd.cut(out1["Age"], 
                            bins=[0, 18, 25, 35, 50, 65, float("inf")], 
                            labels=["00-18", "18-25", "25-35", "35-50", "50-65", "65-More"], 
                            right=False)

# Find last order date for each customer
out2["Order_Date"] = pd.to_datetime(out2["Order_Date"], format="%d/%m/%Y")
last_orders = out2.groupby("Customer_ID").agg({"Order_Date": "max"}).reset_index()
last_orders = last_orders.rename(columns={"Order_Date": "Last_order_dt"})

# Merge last order date with customers DataFrame
out1 = pd.merge(out1, last_orders, on="Customer_ID", how="left")

# Add VAT tax, weekday, and week number to orders DataFrame
out2["Total_Amount"] = pd.to_numeric(out2["Total_Amount"])
out2["VAT"] = out2["Total_Amount"] / 1.2
out2["Order_Date"] = pd.to_datetime(out2["Order_Date"])
out2["Day"] = out2['Order_Date'].dt.day_name()
out2["Week"] = out2["Order_Date"].dt.isocalendar().week

# Merge customers and orders DataFrames on the "customer_id" column
out3 = pd.merge(out1, out2, on="Customer_ID", how="right")

# Group by the required columns and calculate the sums and counts
out4 = out3.groupby(["Age_range", "Sex", "Day"], observed=True).agg(
    CA_TTC=("Total_Amount", "sum"),
    tot_TVA=("VAT", "sum"),
    nb_cli=("Customer_ID", "nunique"),
    nb_cmd=("Order_ID", "nunique"),
)

#Export the output file
#out2.to_csv('C:/Projects/SAS2PY/Tulku-Code-Repo-main/Tulku/Sas2Py_Repo/OutData/out2.csv', sep=';', index=True)
