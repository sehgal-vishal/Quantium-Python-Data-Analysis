#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as colors
import matplotlib.cm as cm


# In[ ]:


# loading csv
transaction=pd.read_csv(r"C:\Users\vishal\Downloads\QVI_transaction_data.csv", encoding='unicode_escape')
customer=pd.read_csv(r"C:\Users\vishal\Downloads\QVI_purchase_behaviour.csv", encoding='unicode_escape')


# In[27]:


transaction.shape


# In[28]:


customer.shape


# In[29]:


transaction.head(15)


# In[30]:


customer.head(15)


# In[31]:


transaction.isnull().sum()


# In[32]:


customer.isnull().sum()


# In[33]:


transaction_purchase_merge=pd.merge(transaction, customer, on='LYLTY_CARD_NBR')


# In[34]:


transaction_purchase_merge.shape


# In[35]:


transaction_purchase_merge.isnull().sum()


# In[36]:


transaction_purchase_merge.head(100)


# In[37]:


Total_sales=transaction_purchase_merge['TOT_SALES'].sum()
print(Total_sales)


# In[38]:


sales_by_store =transaction_purchase_merge.groupby('STORE_NBR')['TOT_SALES'].sum().sort_values(ascending=False).reset_index()
print(sales_by_store)


# In[39]:


sales_by_lifestage = transaction_purchase_merge.groupby('LIFESTAGE')['TOT_SALES'].sum().sort_values(ascending=False).reset_index()
print(sales_by_lifestage)


# In[40]:


sales_by_premium =transaction_purchase_merge.groupby('PREMIUM_CUSTOMER')['TOT_SALES'].sum().sort_values(ascending=False).reset_index()
print(sales_by_premium)


# In[49]:


sales_over_time = transaction_purchase_merge.groupby('DATE')['TOT_SALES'].sum().reset_index()
print(sales_over_time)


# In[41]:


Sales_by_Product= transaction_purchase_merge.groupby('PROD_NAME')['TOT_SALES'].sum()
print(Sales_by_Product)


# In[54]:


# Extract Packet Size from Product Name
transaction_purchase_merge['PACKET_SIZE'] = transaction_purchase_merge['PROD_NAME'].str.extract('(\d+g)', expand=False).str.replace('g', '').astype(float)

# Analyze packet size by lifestage
packet_size_by_lifestage = transaction_purchase_merge.groupby('LIFESTAGE')['PACKET_SIZE'].mean().sort_values(ascending=False).reset_index()


# In[46]:


# Create a colormap
cmap = cm.get_cmap('viridis')

# Normalize the color values to the range [0, 1]
normalize = plt.Normalize(vmin=transaction_purchase_merge['TOT_SALES'].head(10).min(), vmax=transaction_purchase_merge['TOT_SALES'].head(10).max())

colors = [cmap(normalize(value)) for value in transaction_purchase_merge['TOT_SALES'].head(10)]

plt.figure(figsize=(12, 8))
plt.barh(transaction_purchase_merge['PROD_NAME'].head(10), transaction_purchase_merge['TOT_SALES'].head(10), color=colors)
plt.xlabel('Total Sales')
plt.ylabel('Product Name')
plt.title('Top 10 Products by Sales')
plt.gca().invert_yaxis()
plt.show()


# In[43]:


plt.figure(figsize=(10, 6))
transaction_purchase_merge.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().unstack().plot(kind='bar', stacked=True)
plt.title('Total Sales by Lifestage and Premium Customer')
plt.xlabel('Lifestage')
plt.ylabel('Total Sales')
plt.show()


# In[44]:


import plotly.express as px

fig = px.scatter(transaction_purchase_merge, x='TOT_SALES', y='PROD_QTY', color='LIFESTAGE', title='Total Sales vs Product Quantity')
fig.show()


# In[47]:


# Normalize the color values to the range [0, 1]
normalize_store = plt.Normalize(vmin=sales_by_store['TOT_SALES'].head(10).min(), vmax=sales_by_store['TOT_SALES'].head(10).max())
colors_store = [cmap(normalize_store(value)) for value in sales_by_store['TOT_SALES'].head(10)]

plt.figure(figsize=(12, 8))
plt.barh(sales_by_store['STORE_NBR'].head(10), sales_by_store['TOT_SALES'].head(10), color=colors_store)
plt.xlabel('Total Sales')
plt.ylabel('Store Number')
plt.title('Top 10 Stores by Sales')
plt.gca().invert_yaxis()
plt.show()


# In[50]:


plt.figure(figsize=(12, 8))
plt.plot(sales_over_time['DATE'], sales_over_time['TOT_SALES'], marker='o', linestyle='-', color='mediumseagreen')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.title('Sales Over Time')
plt.xticks(rotation=45)
plt.show()


# In[51]:


# Normalize the color values to the range [0, 1]
normalize_lifestage = plt.Normalize(vmin=sales_by_lifestage['TOT_SALES'].min(), vmax=sales_by_lifestage['TOT_SALES'].max())
colors_lifestage = [cmap(normalize_lifestage(value)) for value in sales_by_lifestage['TOT_SALES']]

plt.figure(figsize=(12, 8))
plt.bar(sales_by_lifestage['LIFESTAGE'], sales_by_lifestage['TOT_SALES'], color=colors_lifestage)
plt.xlabel('Lifestage')
plt.ylabel('Total Sales')
plt.title('Total Sales by Lifestage')
plt.xticks(rotation=45)
plt.show()


# In[52]:


# Normalize the color values to the range [0, 1]
normalize_premium = plt.Normalize(vmin=sales_by_premium['TOT_SALES'].min(), vmax=sales_by_premium['TOT_SALES'].max())
colors_premium = [cmap(normalize_premium(value)) for value in sales_by_premium['TOT_SALES']]

plt.figure(figsize=(12, 8))
plt.bar(sales_by_premium['PREMIUM_CUSTOMER'], sales_by_premium['TOT_SALES'], color=colors_premium)
plt.xlabel('Premium Customer')
plt.ylabel('Total Sales')
plt.title('Total Sales by Premium Customer')
plt.show()


# In[55]:




# Normalize the color values to the range [0, 1]
normalize_packet_size = plt.Normalize(vmin=packet_size_by_lifestage['PACKET_SIZE'].min(), vmax=packet_size_by_lifestage['PACKET_SIZE'].max())
colors_packet_size = [cmap(normalize_packet_size(value)) for value in packet_size_by_lifestage['PACKET_SIZE']]

plt.figure(figsize=(12, 8))
plt.bar(packet_size_by_lifestage['LIFESTAGE'], packet_size_by_lifestage['PACKET_SIZE'], color=colors_packet_size)
plt.xlabel('Lifestage')
plt.ylabel('Average Packet Size (g)')
plt.title('Average Packet Size by Lifestage')
plt.xticks(rotation=45)
plt.show()


# In[ ]:




