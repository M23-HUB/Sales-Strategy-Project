#ETL

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin

#Load data

product_sales = pd.read_csv(r'C:\Users\mensa\Documents\Dev Projects\Portfolio Projects\Sales Method Analytics\product_sales.csv')

#First look information on our Data

print('First look information on our Data:', '\n')
print(product_sales.info(), '\n')

# Five percent threshold

threshold = len(product_sales) * 0.05
cols_to_drop = product_sales.columns[product_sales.isna().sum() <= threshold]
product_sales.dropna(subset=cols_to_drop, inplace=True)

print('Number of missing values in each column:', '\n', product_sales.isna().sum() , '\n')

#Number of unique Week

print('Unique Week value:')
print(product_sales['week'].sort_values().unique(), '\n')

#Unique Method Values in data

print('Unique Method values:')
print(product_sales['sales_method'].unique(), '\n')

product_sales['sales_method'] = product_sales['sales_method'].str.title().replace('Em + Call', 'Email + Call')

print('Unique Method values corrected:')
print(product_sales['sales_method'].unique(), '\n')

# Number of unique Customers

print('Number of unique Customers:' + '\n' + str(product_sales['customer_id'].nunique()) + '\n')

# Number of Revenue Values

print('Total missing values in \'revenue\' column ' + str(product_sales['revenue'].isna().sum()) + ' rows')

revenue_prices = product_sales.groupby('nb_sold')['revenue'].median()
nb_dict = revenue_prices.to_dict()
product_sales['revenue'] = product_sales['revenue'].fillna(product_sales['nb_sold'].map(nb_dict))
# print(product_sales.isna().sum())
total_revenue = product_sales['revenue'].sum()
print('Total revenue = $' + str(total_revenue) + '\n')

# Number of unique Week

print('Unique years_as_customer value:')
print(product_sales['years_as_customer'].sort_values().unique(), '\n')

# Number of unique nb_site_visits

print('Unique nb_site_visits value:')
print(product_sales['nb_site_visits'].sort_values().unique(), '\n')

# Number of unique states

print('states in data:')
print(product_sales['state'].sort_values().unique(), '\n')

print('Number of states: ' + '\n' + str(product_sales['state'].nunique()), '\n')

# Final look

print(product_sales.info())
product_sales.to_csv(r'C:\Users\mensa\Documents\Dev Projects\Portfolio Projects\Sales Method Analytics\cleaned_product_sales.csv', index=False)

# Sales Insight

sales_method = product_sales[['sales_method', 'nb_sold', 'revenue', 'nb_site_visits']]\
    .groupby('sales_method')\
      .agg({'sales_method':'count', 'nb_sold':'sum', 'revenue':'sum','nb_site_visits':'sum'})\
        .rename(columns={'sales_method': 'Customers Count', 'nb_sold':'Number of Sales', 'revenue':'Total revenue', 'nb_site_visits': 'Total Number of Site Visits'})\
          .sort_values(by='Total revenue', ascending=False)

sales_method

# Proportion of Total Number of Customers by Each Method

plt.figure(figsize=(10,6))
plt.pie(
    sales_method['Customers Count'],\
    labels=sales_method.index,\
    autopct='%1.1f%%',\
    startangle=90,\
    colors=sns.color_palette('pastel'),\
    wedgeprops={'linewidth':1, 'edgecolor':'white'},\
    textprops={'fontsize':10})

plt.gca().add_artist(plt.Circle((0,0),0.8,color='white',fc='white',linewidth=0))

plt.axis('equal')
plt.title(f'Proportion of Total Number of Customers by Each Method\n\nTotal Customer Count: {product_sales["customer_id"].count():,}', pad=20,fontsize=14)

plt.tight_layout()
plt.show()

# Proportion of Total revenue by Method

plt.figure(figsize=(10,6))
plt.pie(
    sales_method['Total revenue'],\
    labels=sales_method.index,\
    autopct='%1.1f%%',\
    startangle=90,\
    colors=sns.color_palette('pastel'),\
    wedgeprops={'linewidth':1, 'edgecolor':'white'},\
    textprops={'fontsize':10})

plt.gca().add_artist(plt.Circle((0,0),0.8,color='white',fc='white',linewidth=0))

plt.axis('equal')
plt.title(f'Proportion of Total revenue by Method\n\nTotal revenue: ${total_revenue:,.2f}', pad=20, fontsize=14)

plt.tight_layout()
plt.show()

# Number of Sales by Method

plt.figure(figsize=(10,6))
ax = sns.boxplot(data=product_sales, y='nb_sold', x='sales_method', palette='pastel')

ax.set_title('Number of Sales by Method', pad=20,fontsize=14)
ax.set_ylabel('Number of Sales')
ax.set_xlabel('Sale Method')
ax.yaxis.grid(True, linestyle='--', alpha=0.8)

plt.tight_layout()
plt.show()

# nb_sales_p_val

nb_sales_p_val = pingouin.anova(data= product_sales, dv='nb_sold', between='sales_method')
nb_sales_p_val

# Sales Revenue by Method

plt.figure(figsize=(10,6))
ax = sns.boxplot(data=product_sales, y='revenue', x='sales_method', palette='pastel')

ax.set_title('Sales Revenue by Method', pad=20,fontsize=14)
ax.set_ylabel('Revenue ($)')
ax.set_xlabel('Sale Method')
ax.yaxis.grid(True, linestyle='--', alpha=0.8)

plt.tight_layout()
plt.show()

# sales_p_val

sales_p_val = pingouin.anova(data= product_sales, dv='revenue', between='sales_method')
sales_p_val

# Engagement by Method

plt.figure(figsize=(10,6))
ax = sns.boxplot(data=product_sales, y='nb_site_visits', x='sales_method', palette='pastel')

ax.set_title('Engagement by Method', pad=20,fontsize=14)
ax.set_ylabel('Engagement')
ax.set_xlabel('Sale Method')
ax.yaxis.grid(True, linestyle='--', alpha=0.8)

plt.tight_layout()
plt.show()

# visits_p_val

visits_p_val = pingouin.anova(data= product_sales, dv='nb_site_visits', between='sales_method')
visits_p_val

# Revenue by Week

revenue_by_week = product_sales[['revenue','week']]\
                  .groupby('week').agg({'revenue':'sum'}).round(2)

revenue_by_week

# Revenue Across Week After Product Launch

plt.figure(figsize=(10,6))
ax = sns.barplot(data=revenue_by_week.reset_index(), x='week', y='revenue')

ax.set_title(f'Revenue Across Week After Product Launch\n\nTotal revenue: ${total_revenue:,.2f}', pad=20,fontsize=14)
ax.set_ylabel('Revenue ($)')
ax.set_xlabel('Week')
ax.yaxis.grid(True, linestyle='--', alpha=0.8)

plt.tight_layout()
plt.show()

# Number of Customers by week

customers_in_method_by_week = product_sales.pivot_table(index='sales_method', columns='week', values='customer_id', aggfunc='count')

customers_in_method_by_week

# Count of Customers by Method Across Week After Product Launch

to_plot = customers_in_method_by_week.reset_index().melt(id_vars='sales_method',\
                                                         var_name='week',\
                                                         value_name='Count')

pastel_colors = sns.color_palette('pastel',3)
custom_palette = {
    'Email':pastel_colors[0],
    'Email + Call':pastel_colors[1],
    'Call':pastel_colors[2]
}
plt.figure(figsize=(10,6))
ax = sns.lineplot(data=to_plot, x='week', y='Count', hue='sales_method', palette= custom_palette,
                  linewidth=3, errorbar=None, marker='o',markersize=8, dashes=False)

ax.set_title('Count of Customers by Method Across Week After Product Launch', pad=20,fontsize=14)
ax.set_ylabel('Count')
ax.set_xlabel('Week Asfter Launch')
ax.grid(True, linestyle='--', alpha=0.8)

plt.legend(title='Sales Method')
plt.tight_layout()
plt.show()

# Revenue by Method Across Week 

method_revenue_by_week = product_sales.pivot_table(
                         index='sales_method', 
                         columns='week', 
                         values='revenue', 
                         aggfunc='sum')

method_revenue_by_week

# Revenue by Method Across Week After Product Launch

to_plot = method_revenue_by_week.reset_index().melt(id_vars='sales_method',\
                                               var_name='week',\
                                               value_name='revenue')

pastel_colors = sns.color_palette('pastel',3)

custom_palette = {
    'Email':pastel_colors[0],
    'Email + Call':pastel_colors[1],
    'Call':pastel_colors[2]}

plt.figure(figsize=(10,6))
ax = sns.lineplot(data=to_plot, x='week', y='revenue', hue='sales_method', palette= custom_palette,
                  linewidth=3, errorbar=None, marker='o',markersize=8, dashes=False)

ax.set_title('Revenue by Method Across Week After Product Launch', pad=20,fontsize=14)
ax.set_ylabel('Revenue ($)')
ax.set_xlabel('Week After Launch')
ax.grid(True, linestyle='--', alpha=0.8)


plt.legend(title='Sales Method')
plt.tight_layout()
plt.show()