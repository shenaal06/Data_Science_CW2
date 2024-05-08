# Importing the libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import association_rules, apriori
import seaborn as sns
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')


# Naming the Dashboard
st.set_page_config(page_title="Key Insights on Minger", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Key Insights on Minger")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


# Reading the default file
df_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRQib_xqSDNclt9e2Pb9lMPKa3T95nvHng4kQ_7pZxaK0_uOrGmxmd_DG9JW0A3HPLGlS3EgKdfdYdy/pub?output=csv")
# Reading the association rules 
df_2 = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTMnEgv2ppA9uArqbNDa0u1qe7kAzW14XRD2GmTq1eZybf3ZViSnip6KWdeMaodOxV46TMT8gPlOI3Z/pub?output=csv")

# Displaying the DataFrame
st.write(df_1)

# Creating pivot table for heatmap
pivot_t = df_2.pivot(index='antecedents', columns='consequents', values='lift')

# Displaying the heatmap
st.subheader("Heatmap for the Association Rules")
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_t, cmap="YlGnBu", annot=True, fmt=".2f", linewidths=.5)
plt.xlabel("Consequents")
plt.ylabel("Antecedents")
plt.title("Heatmap for the Association Rules (Lift)")
# Get the current figure
heatmap_figure = plt.gcf() 
# Display the heatmap
st.pyplot(heatmap_figure) 

# Displaying the association rules table
st.subheader("Association Rules")
st.write(df_2)

# Creating a scatter plot
df_3 = px.scatter(df_1, x = "Sales", y = "Profit", size = "Quantity")
df_3['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(df_3,use_container_width=True)

# Assuming that Bookcases, Chairs, Supplies, and Tables are the best-selling product names
df_for_best_selling_products = ['Bookcases', 'Chairs', 'Supplies', 'Tables']

# Filtering the data for the best-selling products
df_for_best_selling_data = df_1[df_1['Sub-Category'].isin(df_for_best_selling_products)]

# Grouping the data by sub-category and calculating total sales
sub_category_sales_df = df_for_best_selling_data.groupby('Sub-Category')['Sales'].sum().reset_index()

# Sorting the sub-categories by sales in descending order
sub_category_sales_df = sub_category_sales_df.sort_values(by='Sales', ascending=False)

# Printing the sub-category sales data for debugging
print(sub_category_sales_df)

# Creating a horizontal bar chart
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(sub_category_sales_df['Sub-Category'], sub_category_sales_df['Sales'], color='green')
ax.set_ylabel("Sub-Category")
ax.set_xlabel("Sales")
ax.set_title("Sales of Best-Selling Products by Sub-Category")
# Invert y-axis to have the highest sales at the top
ax.invert_yaxis() 
plt.show()

# Printing the figure object for debugging
st.write(fig)

# Creating a directed graph
G = nx.DiGraph()

# Adding nodes from antecedents and consequents
G.add_nodes_from(df_2['antecedents'], color='red')
G.add_nodes_from(df_2['consequents'], color='blue')

# Adding edges between antecedents and consequents
for i in range(len(df_2)):
    G.add_edge(df_2['antecedents'][i], df_2['consequents'][i], weight=df_2['support'][i])

# Drawing the graph
pos = nx.spring_layout(G, seed=32)  # Layout for the nodes
node_colors = [G.nodes[n]['color'] for n in G.nodes()]
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# Plotting with Matplotlib
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', width=edge_weights, arrowsize=20)
plt.title("Association Rules Network Graph")

# Showing the plot using Streamlit
st.pyplot(fig)

# Filtering data to include only specified sub-categories
df_sub_categories = ['Bookcases', 'Chairs', 'Tables', 'Supplies']
df_filtered = df_1[df_1['Sub-Category'].isin(df_sub_categories)]

# Grouping by Region and Sub-Category and calculate total sales
df_region_subcategory_sales = df_filtered.groupby(['Region', 'Sub-Category'])['Sales'].sum().reset_index()

# Adding a selectbox widget to filter by region
df_selected_region = st.selectbox("Select Region", df_region_subcategory_sales['Region'].unique())

# Filtering data for the selected region
df_selected_region_data = df_region_subcategory_sales[df_region_subcategory_sales['Region'] == df_selected_region]

# Creating a grouped bar chart using Plotly Express
df_figure_5 = px.bar(df_selected_region_data, x='Sub-Category', y='Sales', color='Sub-Category',
             title=f"Sales by Sub-Category in {df_selected_region}",
             labels={'Sales': 'Total Sales', 'Sub-Category': 'Sub-Category'})

# Updating the layout
df_figure_5.update_layout(xaxis_title="Sub-Category", yaxis_title="Total Sales")

# Displaying the chart
st.plotly_chart(df_figure_5)

# Filtering data to include only specified sub-categories
df_sub_categories = ['Bookcases', 'Chairs', 'Tables', 'Supplies']
df_filtered = df_1[df_1['Sub-Category'].isin(df_sub_categories)]

# Extracting quarter from 'Ship Date' column and convert it to string
df_filtered['Quarter'] = pd.to_datetime(df_filtered['Ship Date']).dt.to_period('Q').astype(str)

# Grouping by Quarter and Sub-Category and calculate total sales
df_quarterly_sales = df_filtered.groupby(['Quarter', 'Sub-Category'])['Sales'].sum().reset_index()

# Plotting the Line Chart
df_figure_6 = px.line(df_quarterly_sales, x='Quarter', y='Sales', color='Sub-Category',
              title="Quarterly Sales Trends for Specific Sub-Categories",
              labels={'Sales': 'Total Sales', 'Quarter': 'Quarter'})

# Updating layout
df_figure_6.update_layout(xaxis_title="Quarter", yaxis_title="Total Sales")

# Displaying the chart
st.plotly_chart(df_figure_6)