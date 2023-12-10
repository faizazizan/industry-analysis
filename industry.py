pip install -r requirements.txt

import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Your industry data
data = """
Industry,Gross Profit Margin,Net Profit Margin
Advertising,26.20%,3.10%
Apparel,53.04%,7.06%
Auto,14.25%,3.96%
Alcoholic Beverages,47.99%,5.07%
Broadcasting,45.22%,10.40%
Business & Consumer Services,31.80%,4.97%
Computer Services,27.24%,3.42%
Computers/Peripherals,36.88%,18.72%
Drugs (Biotechnology),62.25%,-0.62%
Drugs (Pharmaceutical),67.35%,11.03%
Education,47.90%,7.17%
Electrical Equipment,33.53%,7.26%
Electronics (Consumer & Office),32.41%,7.08%
Electronics (General),28.40%,7.02%
Engineering/Construction,13.45%,1.81%
Entertainment,41.94%,3.86%
Farming/Agriculture,13.61%,6.03%
Food Processing,27.00%,8.44%
Food Wholesalers,14.85%,0.69%
Furniture,29.74%,7.64%
Green & Renewable Energy,62.92%,-19.78%
Healthcare Products,59.04%,12.92%
Heathcare Information and Technology,52.49%,16.64%
Hotel/Gaming,55.45%,-28.56%
Household Products,50.13%,12.45%
Machinery,35.42%,10.79%
Office Equipment & Services,33.40%,2.55%
Precious Metals,52.43%,14.48%
Publishing & Newspapers,42.65%,3.55%
Restaurant/Dining,31.52%,12.63%
Software (Entertainment),64.45%,29.04%
Software (Internet),61.00%,-10.36%
Software (System & Application),71.59%,19.66%
Tobacco,62.87%,20.58%
Financial,85.08%,32.33%
"""

# Convert the string data to a DataFrame
df = pd.read_csv(io.StringIO(data))

# Ensure numeric columns
df['Gross Profit Margin'] = pd.to_numeric(df['Gross Profit Margin'].str.rstrip('%'), errors='coerce') / 100
df['Net Profit Margin'] = pd.to_numeric(df['Net Profit Margin'].str.rstrip('%'), errors='coerce') / 100

# Streamlit App
st.title("Profit Margin Analysis Dashboard")

# Checkbox to select all industries
select_all_industries = st.checkbox("Select All Industries", value=True)

# Simple selection for picking industries
if select_all_industries:
    selected_industry = "All Industries"
else:
    selected_industry = st.selectbox("Pick an Industry:", sorted(df['Industry'].unique()))

# Simple selection for choosing between net profit margin and gross profit margin
filter_option = st.selectbox("Select Profit Margin Type:", ["Net Profit Margin", "Gross Profit Margin"])

# Filter DataFrame based on the selected industry
if selected_industry == "All Industries":
    filtered_df = df
else:
    filtered_df = df[df['Industry'] == selected_industry]

# Professional chart based on the selected filter option
if not filtered_df.empty:
    fig = px.bar(filtered_df, x='Industry', y=filter_option, color='Industry',
                 labels={'Industry': 'Industry', filter_option: filter_option},
                 title=f"{filter_option} for {selected_industry}",
                 template='plotly_dark')

    # Update layout for better visibility
    fig.update_layout(
        xaxis_title=None,  # Removed x-axis label
        yaxis_title=filter_option,
        legend_title="Industry",
        width=800,  # Set width for better visibility
        height=500,  # Set height for better visibility
        xaxis=dict(showticklabels=False),  # Disable x-axis labels
        yaxis=dict(tickmode='array', tickformat=".2%"),
        yaxis_tickvals=[i/100 for i in range(-30, 31, 10)])  # Convert tick values to percentage

    # Show chart
    st.plotly_chart(fig)

# Display the filtered DataFrame with percentage formatting for Gross Profit Margin and Net Profit Margin
formatted_df = filtered_df.copy()
formatted_df['Gross Profit Margin'] = formatted_df['Gross Profit Margin'].apply("{:.2%}".format)
formatted_df['Net Profit Margin'] = formatted_df['Net Profit Margin'].apply("{:.2%}".format)

# Show the table
st.subheader(f"Data Table for {selected_industry}:")
st.table(formatted_df)

