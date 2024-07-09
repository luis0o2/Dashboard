import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime


dateparse = lambda x: datetime.strptime(x, '%m-%d-%Y')

df = pd.read_csv('C:\\Users\\ochoa\\Desktop\\Dev\\Python\\Dashboard\\.venv\\report.csv', parse_dates=['Date'])
df['Sold'] = pd.to_numeric(df['Sold'], errors='coerce')
df['Royalty'] = pd.to_numeric(df['Royalty'], errors='coerce')
df['Returned'] = pd.to_numeric(df['Returned'], errors='coerce')

df['Month_Year'] = df['Date'].dt.strftime('%m/%Y')

"""""
total_sales_per_clothing_type = df.groupby('Product Type')['Sold'].sum()
total_profit_per_clothing_type = df.groupby('Product Type')['Royalty'].sum()
total_returns_per_clothing_type = df.groupby('Product Type')['Returned'].sum()
"""""
marketplace_monthly_sales = df.groupby(['Marketplace', 'Month_Year']).agg({
    'Sold': 'sum'
}).reset_index()

st.title('Marketplace Sales Analysis')

fig, ax = plt.subplots()

for marketplace in marketplace_monthly_sales['Marketplace'].unique():
    data = marketplace_monthly_sales[marketplace_monthly_sales['Marketplace'] == marketplace]
    ax.plot(data['Month_Year'], data['Sold'], label=marketplace)

ax.set_xlabel('Month')
ax.set_ylabel('Total Sales')
ax.set_title('Marketplace Sales Over Time')
ax.legend(loc='upper left')
ax.grid(True)

st.pyplot(fig)
grouped = df.groupby('Product Type').agg({'Royalty': 'sum', 'Sold': 'sum', 'Returned': 'sum'})
grouped['Return Rate'] = grouped['Returned'] / grouped['Sold'] * 100
grouped['Return Rate'] = grouped['Return Rate'].apply(lambda x: f'{x:.2f}%')

st.title('Dashboard')
st.write(grouped)
