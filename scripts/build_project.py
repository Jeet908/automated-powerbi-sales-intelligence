import os
import json
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BASE_DIR = r"c:\Users\HP\Downloads\Linkedin\Headshot\automated-powerbi-sales-intelligence"
DATA_DIR = os.path.join(BASE_DIR, "data")
THEME_DIR = os.path.join(BASE_DIR, "theme")
DAX_DIR = os.path.join(BASE_DIR, "dax")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(THEME_DIR, exist_ok=True)
os.makedirs(DAX_DIR, exist_ok=True)

np.random.seed(42)
random.seed(42)

print("1. Generating Relational Dimension Tables...")

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
df_region.to_csv(os.path.join(DATA_DIR, "Dim_Region.csv"), index=False)

# 2. Dim_Product
categories = {
    "Technology": [
        ('Smart Monitor 27"', 280.0, 420.0, "Displays"),
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
df_product.to_csv(os.path.join(DATA_DIR, "Dim_Product.csv"), index=False)

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
df_customer.to_csv(os.path.join(DATA_DIR, "Dim_Customer.csv"), index=False)

# 4. Dim_Date (Pre-built Calendar from 2022 to 2024 with clean numeric sorting)
start_dt = datetime(2022, 1, 1)
end_dt = datetime(2024, 12, 31)
date_records = []
cur_dt = start_dt
while cur_dt <= end_dt:
    qtr = (cur_dt.month - 1) // 3 + 1
    date_records.append({
        "DateKey": int(cur_dt.strftime("%Y%m%d")),
        "FullDate": cur_dt.strftime("%Y-%m-%d"),
        "Year": cur_dt.year,
        "Quarter": f"Q{qtr}",
        "MonthNumber": cur_dt.month,
        "MonthName": cur_dt.strftime("%B"),
        "MonthYear": cur_dt.strftime("%b %Y"),
        "DayOfWeekNumber": cur_dt.isoweekday(),
        "DayOfWeekName": cur_dt.strftime("%A"),
        "IsWeekend": 1 if cur_dt.isoweekday() >= 6 else 0
    })
    cur_dt += timedelta(days=1)
df_date = pd.DataFrame(date_records)
df_date.to_csv(os.path.join(DATA_DIR, "Dim_Date.csv"), index=False)

print("2. Generating Fact_Sales (25,000 Transactions)...")
total_days = (end_dt - start_dt).days + 1
transactions = []
for i in range(1, 25001):
    day_offset = random.randint(0, total_days - 1)
    tx_date = start_dt + timedelta(days=day_offset)
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
df_sales.to_csv(os.path.join(DATA_DIR, "Fact_Sales.csv"), index=False)

print("3. Generating Automated Power BI Theme (Auto-styles all canvas, cards, borders, shadows in 1 click)...")
theme_json = {
    "name": "Executive Navy and Clean Slate",
    "dataColors": ["#0F172A", "#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#64748B"],
    "background": "#FFFFFF",
    "foreground": "#0F172A",
    "tableAccent": "#2563EB",
    "visualStyles": {
        "page": {
            "*": {
                "background": [{"color": {"solid": {"color": "#F4F5F7"}}, "transparency": 0}]
            }
        },
        "*": {
            "*": {
                "background": [{"color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}],
                "border": [{"color": {"solid": {"color": "#E2E8F0"}}, "show": True, "radius": 8}],
                "dropShadow": [{"show": True, "color": {"solid": {"color": "#E2E8F0"}}, "position": "Outer", "preset": "BottomRight"}],
                "title": [{"show": True, "fontFamily": "Segoe UI Semibold", "fontSize": 12, "fontColor": {"solid": {"color": "#0F172A"}}}]
            }
        },
        "card": {
            "*": {
                "labels": [{"fontFamily": "Segoe UI Bold", "fontSize": 22, "color": {"solid": {"color": "#0F172A"}}}],
                "categoryLabels": [{"fontFamily": "Segoe UI", "fontSize": 10, "color": {"solid": {"color": "#64748B"}}}]
            }
        }
    }
}
with open(os.path.join(THEME_DIR, "executive_theme.json"), "w", encoding="utf-8") as f:
    json.dump(theme_json, f, indent=2)

print("4. Generating DAX Reference File...")
dax_content = """-- =====================================================================
-- COMPLETE DAX MEASURES MASTER LIST
-- Table: _KeyMeasures
-- =====================================================================

-- 1. Total Revenue
Total Revenue = SUM(Fact_Sales[Revenue])

-- 2. Total Cost
Total Cost = SUM(Fact_Sales[TotalCost])

-- 3. Total Profit
Total Profit = [Total Revenue] - [Total Cost]

-- 4. Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

-- 5. Total Orders
Total Orders = DISTINCTCOUNT(Fact_Sales[SalesKey])

-- 6. Average Order Value (AOV)
Average Order Value (AOV) = DIVIDE([Total Revenue], [Total Orders], 0)

-- 7. Prior Year Revenue (LY)
Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[FullDate]))

-- 8. YoY Revenue Growth $
YoY Revenue Growth $ = [Total Revenue] - [Revenue LY]

-- 9. YoY Revenue Growth %
YoY Revenue Growth % = DIVIDE([YoY Revenue Growth $], [Revenue LY], 0)

-- 10. Revenue YTD
Revenue YTD = TOTALYTD([Total Revenue], Dim_Date[FullDate])

-- 11. Dynamic Performance Status Badge
YoY Performance Status = 
VAR Growth = [YoY Revenue Growth %]
RETURN
    SWITCH(
        TRUE(),
        Growth >= 0.10, "🟢 Outperforming (≥ +10%)",
        Growth >= 0.00, "🟡 On Target (0% to +10%)",
        "🔴 Underperforming (< 0%)"
    )
"""
with open(os.path.join(DAX_DIR, "all_measures.dax"), "w", encoding="utf-8") as f:
    f.write(dax_content)

print("SUCCESS: All datasets, automated theme, and DAX measures generated completely!")
