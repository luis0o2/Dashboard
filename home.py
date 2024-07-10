import matplotlib.pyplot as plt
import streamlit as st
import re
import numpy as np
import pandas as pd
from datetime import datetime


df = pd.read_csv('C:\\Users\\ochoa\\Desktop\\Dev\\Python\\Dashboard\\.venv\\report.csv', parse_dates=['Date'])
df['Sold'] = pd.to_numeric(df['Sold'], errors='coerce')
df['Royalty'] = pd.to_numeric(df['Royalty'], errors='coerce')
df['Returned'] = pd.to_numeric(df['Returned'], errors='coerce')

df['Month_Year'] = df['Date'].dt.strftime('%m/%Y')

marketplace_monthly_sales = df.groupby(['Month_Year', 'Marketplace'])['Sold'].sum().unstack(fill_value=0)
marketplace_monthly_sales.index = pd.to_datetime(marketplace_monthly_sales.index, format='%m/%Y')
marketplace_monthly_sales = marketplace_monthly_sales.sort_index()

def extract_colors(sold_colors, valid_colors):
    color_counts = {}
    items = sold_colors.split(',')
    for item in items:
        color, count = item.strip().split(':')
        color = color.strip()
        count = int(count.strip())
        if color in valid_colors:
            if color in color_counts:
                color_counts[color] += count
            else:
                color_counts[color] = count
    return color_counts

valid_colors = [
    'Black', 'White', 'Navy', 'Asphalt', 'Kelly Green', 'Olive', 'Slate', 'Brown', 'Purple',
    'Pink', 'Heather Grey', 'Baby Blue', 'Dark Heather', 'Royal', 'Red', 'Sage Green', 'Burgundy',
    'Silver', 'Lemon', 'Cranberry', 'Royal Blue White'
]



# Aggregate the color counts
color_aggregate = {}
for colors in df['Sold Colors'].dropna():
    color_counts = extract_colors(colors, valid_colors)
    for color, count in color_counts.items():
        if color in color_aggregate:
            color_aggregate[color] += count
        else:
            color_aggregate[color] = count



# Display the aggregated color counts
colors = list(color_aggregate.keys())
counts = list(color_aggregate.values())
fig, ax = plt.subplots()
ax.pie(counts, labels=None, autopct=None, startangle=140)
ax.axis('equal')
st.pyplot(fig)
data = pd.DataFrame({
    'Color': list(color_aggregate.keys()),
    'Count': list(color_aggregate.values())
})
st.write(data)
fig, ax = plt.subplots(figsize=(10,7))

for column in marketplace_monthly_sales.columns:
    ax.plot(marketplace_monthly_sales.index, marketplace_monthly_sales[column], label=column)



ax.set_title('Monthly Sales by Marketplace')
ax.set_xlabel('Month-Year')
ax.set_ylabel('Sales')
ax.legend(title ='Marketplace')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

st.sidebar.title('Menu')
st.markdown(
    """
    <style>
    .main {
        background-color: #4F007F
        }
        .sidebar .sidebar-content {
        background-color: #4F007F;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Marketplace Sales Analysis')
st.pyplot(fig)

st.write(marketplace_monthly_sales)

grouped = df.groupby('Product Type').agg({'Royalty': 'sum', 'Sold': 'sum', 'Returned': 'sum'})
grouped['Return Rate'] = grouped['Returned'] / grouped['Sold'] * 100
grouped['Return Rate'] = grouped['Return Rate'].apply(lambda x: f'{x:.2f}%')

st.title('Dashboard')
st.write(grouped)

