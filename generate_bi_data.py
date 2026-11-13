"""
Dataset Generator for Power BI Automated Sales Intelligence System
Run: python generate_bi_data.py
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

os.makedirs("bi_data", exist_ok=True)
np.random.seed(42)
random.seed(42)

# 1. Dim_Region
regions_data = [
    {"RegionKey": 1, "Region": "North America", "Territory": "US-East", "Country": "United States", "RegionalManager": "Sarah Jenkins"},
    {"RegionKey": 2, "Region": "North America", "Territory": "US-West", "Country": "United States", "RegionalManager": "David Miller"},
    {"RegionKey": 3, "Region": "Europe", "Territory": "Central Europe", "Country": "Germany", "RegionalManager": "Klaus Richter"},
    {"RegionKey": 4, "Region": "Europe", "Territory": "UK & Ireland", "Country": "United Kingdom", "RegionalManager": "Emma Watson"},
    {"RegionKey": 5, "Region": "Asia-Pacific", "Territory": "South Asia", "Country": "India", "RegionalManager": "Rajesh Sharma"},
    {"RegionKey": 6, "Region": "Asia-Pacific", "Territory": "East Asia", "Country": "Japan", "RegionalManager": "Kenji Sato"}
]
df_region = pd.DataFrame(regions_data)
df_region.to_csv("bi_data/Dim_Region.csv", index=False)

# 2. Dim_Product
categories = {
    "Technology": [
        ("Smart Monitor 27\"", 280.0, 420.0, "Displays"),
        ("Mechanical Keyboard", 45.0, 89.0, "Peripherals"),
        ("Noise-Cancelling Headphones", 110.0, 199.0, "Audio"),
        ("USB-C Thunderbolt Hub", 35.0, 75.0, "Accessories")
    ],
    "Office Supplies": [
        ("Ergonomic Task Chair", 140.0, 260.0, "Furniture"),
        ("Height-Adjustable Desk", 220.0, 450.0, "Furniture"),
        ("Laser Toner Cartridge", 25.0, 65.0, "Supplies"),
        ("Premium Archival Binders (Pack of 10)", 12.0, 28.0, "Paper Products")
    ],
    "Consumer Electronics": [
        ("Fitness Smartwatch V2", 65.0, 149.0, "Wearables"),
        ("Fast Wireless Charging Pad", 14.0, 32.0, "Accessories"),
        ("Smart LED Desk Lamp", 22.0, 52.0, "Smart Home")
    ]
}

products_list = []
prod_key = 101
for cat, items in categories.items():
    for name, cost, price, subcat in items:
        products_list.append({
            "ProductKey": prod_key,
            "ProductName": name,
            "Category": cat,
            "SubCategory": subcat,
            "StandardCost": cost,
            "UnitPrice": price,
            "TargetMarginPct": round((price - cost) / price, 2)
        })
        prod_key += 1

df_product = pd.DataFrame(products_list)
df_product.to_csv("bi_data/Dim_Product.csv", index=False)

# 3. Dim_Customer
first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "Amit", "Priya", "Rahul", "Ananya"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Mukherjee", "Das", "Banerjee", "Taylor", "Anderson"]
segments = ["Consumer", "Corporate", "Small Business"]

customers_list = []
for c_id in range(1, 501):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    customers_list.append({
        "CustomerKey": c_id,
        "CustomerName": f"{fn} {ln}",
        "CustomerSegment": random.choices(segments, weights=[0.55, 0.30, 0.15])[0],
        "Country": random.choice(["United States", "Germany", "United Kingdom", "India", "Japan"])
    })
df_customer = pd.DataFrame(customers_list)
df_customer.to_csv("bi_data/Dim_Customer.csv", index=False)

# 4. Fact_Sales (25,000 Transactions across 2022-2024)
start_date = datetime(2022, 1, 1)
total_days = 365 * 3

transactions = []
for i in range(1, 25001):
    day_offset = random.randint(0, total_days - 1)
    tx_date = start_date + timedelta(days=day_offset)
    
    prod = random.choice(products_list)
    cust = random.randint(1, 500)
    region = random.randint(1, 6)
    
    qty = random.choices([1, 2, 3, 4, 5, 8, 10], weights=[0.4, 0.3, 0.15, 0.08, 0.04, 0.02, 0.01])[0]
    discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.6, 0.15, 0.12, 0.08, 0.05])[0]
    
    unit_price = prod["UnitPrice"]
    unit_cost = prod["StandardCost"]
    
    gross_revenue = round(qty * unit_price, 2)
    net_revenue = round(gross_revenue * (1 - discount), 2)
    total_cost = round(qty * unit_cost, 2)
    profit = round(net_revenue - total_cost, 2)
    
    transactions.append({
        "SalesKey": i,
        "OrderDate": tx_date.strftime("%Y-%m-%d"),
        "OrderDateKey": int(tx_date.strftime("%Y%m%d")),
        "CustomerKey": cust,
        "ProductKey": prod["ProductKey"],
        "RegionKey": region,
        "Quantity": qty,
        "UnitPrice": unit_price,
        "UnitCost": unit_cost,
        "Discount": discount,
        "Revenue": net_revenue,
        "TotalCost": total_cost,
        "Profit": profit
    })

df_sales = pd.DataFrame(transactions)
df_sales.to_csv("bi_data/Fact_Sales.csv", index=False)
print("All 4 CSV files successfully created in ./bi_data folder!")
