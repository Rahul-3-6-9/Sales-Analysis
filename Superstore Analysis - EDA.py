import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser

df = pd.read_csv("cleaned_data_superstore.csv", encoding="latin1")

print(df.head())
print(df.info())
print(df.describe())
print(df.columns)
print(df.shape)

# 1. Understand how sales and profit change over time.
def try_parse(x):
    try:
        return parser.parse(x)
    except:
        return pd.NaT

df['Order Date'] = df['Order Date'].apply(try_parse)
df["Year"]=df["Order Date"].dt.year
df["Month"]=df["Order Date"].dt.month
monthly_sales = df.groupby(['Year', 'Month'])[['Sales', 'Profit']].sum().reset_index()
yearly_sales = df.groupby(["Year"])[['Sales', 'Profit']].sum().reset_index()

plt.figure(figsize=(14, 6))
sns.lineplot(data=monthly_sales, x='Month', y='Sales', hue='Year')
plt.title("Monthly Sales Trend")
plt.show()

sns.boxplot(data=yearly_sales, x='Year', y='Sales', fill=True)
plt.title("Yearly Sales Trend")
plt.show()

# 2. Which product categories and sub-categories contribute the most to sales and profit?
#    Which products have high sales but low or negative profit?
category_perf = df.groupby(['Category', 'Sub-Category'])[['Sales', 'Profit']].sum().sort_values(by='Profit', ascending=False)
category_perf.plot(kind='barh', figsize=(12,8), stacked=True)
plt.title('Sales and Profit by Product Category')
plt.show()

# 3. Which regions and states are most profitable?
#    Are there states with high sales but low profit margins?
state_perf = df.groupby('State')[['Sales', 'Profit']].sum().sort_values(by='Profit', ascending=False)
plt.figure(figsize=(14,6))
state_perf['Profit'].plot(kind='bar')
plt.title("Profit by State")
plt.axhline(0, color='red', linestyle='--')
plt.show()

# 4. Which customer segments generate the most revenue?
#    What are the average order values across segments?
segment_perf = df.groupby('Segment')[['Sales', 'Profit']].agg(['mean', 'sum'])
print(segment_perf)

# 5. How does shipping mode affect delivery time and profitability?
#    Are there correlations between ship date delays and profit?
shipping_perf = df.groupby('Ship Mode')[['Sales', 'Profit']].mean()
print(shipping_perf)

# Ensure dates are datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Calculate Delivery Time in days
df['Delivery Time (Days)'] = (df['Ship Date'] - df['Order Date']).dt.days

# Drop rows with invalid delivery times
df = df[df['Delivery Time (Days)'].notna()]

# Group by Delivery Time and Ship Mode
grouped = df.groupby(['Delivery Time (Days)', 'Ship Mode']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Melt for plotting both Sales and Profit
melted = pd.melt(grouped, id_vars=['Delivery Time (Days)', 'Ship Mode'], value_vars=['Sales', 'Profit'],
                 var_name='Metric', value_name='Amount')

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(
    data=melted,
    x='Delivery Time (Days)',
    y='Amount',
    hue='Ship Mode'
)

plt.title('Sales and Profit vs Delivery Time by Ship Mode')
plt.ylabel('Amount (USD)')
plt.xlabel('Delivery Time (Days)')
plt.legend(title='Ship Mode')
plt.tight_layout()
plt.show()

df.to_csv("data_afterEDA_superstore.csv", index=False)