import matplotlib.pyplot as plt
import streamlit as st
import re
import numpy as np
import pandas as pd
from datetime import datetime


st.markdown(
    """
    <style>
    .main {
        background-color: #000000
        }
        .sidebar .sidebar-content {
        background-color: #000000
        }
    </style>
    """,
    unsafe_allow_html=True
)





# color dictionary for pie chart
color_dict = {
    'Black': '#000000', 'White': '#FFFFFF', 'Navy': '#000080', 'Asphalt': '#3C3F41', 'Kelly Green': '#4CBB17',
    'Olive': '#808000', 'Slate': '#708090', 'Brown': '#A52A2A', 'Purple': '#800080', 'Pink': '#FFC0CB', 'Heather Grey': '#BEBEBE',
    'Baby Blue': '#89CFF0', 'Dark Heather': '#555555', 'Royal': '#4169E1', 'Red': '#FF0000', 'Sage Green': '#B2AC88', 'Burgundy': '#800020',
    'Silver': '#C0C0C0', 'Lemon': '#FFF44F', 'Cranberry': '#950714', 'Royal Blue White': '#FFFFFF'  
}

df = pd.read_csv('report.csv', parse_dates=['Date'])   #reading csv file
#turning number headers to numeric
df['Sold'] = pd.to_numeric(df['Sold'], errors='coerce')
df['Royalty'] = pd.to_numeric(df['Royalty'], errors='coerce')
df['Returned'] = pd.to_numeric(df['Returned'], errors='coerce')


#making a seperate header named Month_Year using the datetime library
df['Month_Year'] = df['Date'].dt.strftime('%m/%Y')
#grouping 2 headers(month_year and marketplace) and their sold sums filling any empty value with 0
marketplace_monthly_sales = df.groupby(['Month_Year', 'Marketplace'])['Sold'].sum().unstack(fill_value=0)
#sorting by date oldest to newest
marketplace_monthly_sales.index = pd.to_datetime(marketplace_monthly_sales.index, format='%m/%Y')
marketplace_monthly_sales = marketplace_monthly_sales.sort_index()
#**********************PIE CHART CODE******************************START
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

valid_colors = list(color_dict.keys())

# Aggregate the color counts
color_aggregate = {}
for colors in df['Sold Colors'].dropna():
    color_counts = extract_colors(colors, valid_colors)
    for color, count in color_counts.items():
        if color in color_aggregate:                
            color_aggregate[color] += count             #count is how many of those colors were found
        else:
            color_aggregate[color] = count

# Display the aggregated color counts
colors = list(color_aggregate.keys())
counts = list(color_aggregate.values())
pie_colors = [color_dict[color] for color in colors]

fig, ax = plt.subplots()
ax.pie(counts, labels=None, autopct=None, startangle=140, colors=pie_colors)
ax.axis('equal')
st.title(':red[Colors Sold]')
st.pyplot(fig)

data = pd.DataFrame({
    'Color': list(color_aggregate.keys()),
    'Count': list(color_aggregate.values())
})
st.write(data)
#**********************PIE CHART CODE******************************END

#**********************LINE CHART CODE******************************START

fig, ax = plt.subplots(figsize=(10, 7))

for column in marketplace_monthly_sales.columns:
    ax.plot(marketplace_monthly_sales.index, marketplace_monthly_sales[column], label=column)

ax.set_title('Monthly Sales by Marketplace')
ax.set_xlabel('Month-Year')
ax.set_ylabel('Sales')
ax.legend(title='Marketplace')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

st.title(':red[Marketplace Sales Analysis]')
st.pyplot(fig)

st.write(marketplace_monthly_sales)
#**********************LINE CHART CODE******************************END


#**********************DASHBOARD CODE******************************START
grouped = df.groupby('Product Type').agg({'Royalty': 'sum', 'Sold': 'sum', 'Returned': 'sum'})
grouped['Return Rate'] = grouped['Returned'] / grouped['Sold'] * 100
grouped['Return Rate'] = grouped['Return Rate'].apply(lambda x: f'{x:.2f}%')
royalty_by_product = df.groupby('Product Type')['Royalty'].sum().reset_index()
st.title(':red[Dashboard]')
fig, ax = plt.subplots()
ax.bar(royalty_by_product['Product Type'], royalty_by_product['Royalty'])
ax.set_xlabel('Product Type')
ax.set_ylabel('Royalty')
ax.set_xticklabels(royalty_by_product['Product Type'], rotation=90)
st.pyplot(fig)

st.write(grouped)
#**********************DASHBOARD CODE******************************END




