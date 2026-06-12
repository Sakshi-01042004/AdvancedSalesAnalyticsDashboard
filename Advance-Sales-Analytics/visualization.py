import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/cleaned_sales.csv")

# =========================
# DATA TYPE FIXING
# =========================

# Convert Sales column to numeric
df["Sales"] = pd.to_numeric(df["Sales"], errors='coerce')

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')

# Remove null values if created during conversion
df = df.dropna()

# Style
sns.set(style="whitegrid")

# Create charts folder automatically
import os
os.makedirs("charts", exist_ok=True)

# =========================
# 1. SALES BY CATEGORY
# =========================

plt.figure(figsize=(8,5))

category_sales = df.groupby("Category")["Sales"].sum()

category_sales.plot(kind='bar')

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig("charts/category_sales.png")

plt.close()

# =========================
# 2. SALES BY REGION
# =========================

plt.figure(figsize=(8,5))

region_sales = df.groupby("Region")["Sales"].sum()

plt.pie(region_sales,
        labels=region_sales.index,
        autopct='%1.1f%%')

plt.title("Sales Distribution by Region")

plt.tight_layout()

plt.savefig("charts/region_sales.png")

plt.close()

# =========================
# 3. TOP 10 PRODUCTS
# =========================

plt.figure(figsize=(12,6))

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_products.plot(kind='bar')

plt.title("Top 10 Products by Sales")
plt.xlabel("Product Name")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/top_products.png")

plt.close()

print("Charts created successfully!")