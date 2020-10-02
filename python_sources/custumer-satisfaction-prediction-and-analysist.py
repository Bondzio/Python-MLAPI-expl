#!/usr/bin/env python
# coding: utf-8

# ### **CUSTOMER SATISFACTION**
# I haven't read a lot of theory about customer satisfaction, but the picture down bellow explains how I thought about customer satisfaction work. First, satisfaction happens when what customer expected is the same or higher with what they got. Then I divided expectation and performance based on everyone who has a responsibility in the transaction those are seller, courier, and the product itself.
# 
# Expectations and performance have a different correlation with customer satisfaction. higher expectation would make customer less satisfied while better performance will make them more satisfied.
# 
# here is the explanation and the hyphotesis of each variables: 
# - **EXPECTATION**
#     * **product_price (-)** : the higher amount paid by customer, the higher their expextation
#     * **higher_product_price (-)** : this is dummy variable, 1 when the **product_price** is higher then the average **product_price** in the same category and 0 otherwise. of course customer will expect more when they paid more that the average
#     * **product_sold_by_seller (-)** : this variable explains seller's experience, and the customer will expect more with the experienced one
#     * **freight_rate (-)** : the higher amount paid by customer for delivering their things, the higher their expextation
#     * **higher_freight_rate (-)** : this is dummy variable, 1 when the **freight_rate** is higher then the average **freight_rate** for the same distance and 0 otherwise. of course customer will expect more when they paid more that the average
# - **PERFORMANCE**
#     * **product_rating (+)** : higher **product_rating** indicated higher product performance
#     * **better_product_rating (+)** : this is dummy variable, 1 when the **product_rating** is higher then the average **product_rating** in the same category and 0 otherwise.
#     * **seller_rating (+)** : higher **seller_rating** indicated higher seller performance
#     * **approving_time (-)** : is the different between **order_purchase_timestamp** and **order_approved_at**. higher number of approving time indicated lower seller performance
#     * **processing_time (-)** : is the different between **order_approved_at** and **order_delivered_carrier_date**. higher number of processing time indicated lower seller performance
#     * **seller_on_time (+)** : this is dummy variable, 1 when the seller deliver the product to courier **(order_delivered_carrier_date)** before **shipping_limit_date** and 0 otherwise
#     * **delivery_time (-)** : is the different between **order_delivered_carrier_date** and **order_delivered_customer_date**. higher number of delivery time indicated lower courier performance
#     * **courier_on_time (+)** : this is dummy variable, 1 when the courier deliver the product to customer **(order_delivered_customer_date)** before **order_estimated_delivery_date** and 0 otherwise
#     * **distance (-)** : the risk for delivering product is higher when the distance is higher

# <img src="https://serving.photos.photobox.com/7531498291ad2dfa83791c20e6f4bd5febc5409f88831ccc3812ed4ab7e4c4341d02916c.jpg"
#      alt="Markdown Monster icon" 
#      style="float: left; margin-right: 10px;" />

# # LOAD ALL DATA

# In[ ]:


import pandas as pd
import numpy as np

dfOrdersItems = pd.read_csv('../input/brazilian-ecommerce/olist_order_items_dataset.csv')
dfOrders = pd.read_csv('../input/brazilian-ecommerce/olist_orders_dataset.csv')
dfProducts = pd.read_csv('../input/brazilian-ecommerce/olist_products_dataset.csv')
dfOrdersReviews = pd.read_csv('../input/brazilian-ecommerce/olist_order_reviews_dataset.csv')
dfSellers = pd.read_csv('../input/brazilian-ecommerce/olist_sellers_dataset.csv')
dfCustomers = pd.read_csv('../input/brazilian-ecommerce/olist_customers_dataset.csv')
dfGeolocation = pd.read_csv('../input/olist-modified-data/geolocation_v2.csv')
dfTranslation = pd.read_csv('../input/brazilian-ecommerce/product_category_name_translation.csv')


# # BEAUTYFYING SOME DATASET
# ## Product Dataset

# In[ ]:


dfProducts = dfProducts.merge(dfTranslation, on='product_category_name')
dfProducts.drop('product_category_name', axis=1, inplace=True)
dfProducts.rename(columns={
    'product_category_name_english' : 'product_category'
}, inplace=True)
dfProducts = dfProducts[['product_id','product_category']]
dfProducts.head()


# ## Seller Dataset

# In[ ]:


dfSellerx = pd.merge(dfSellers, dfGeolocation, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix')
dfSellerx.rename(columns={
    'geolocation_lat' : 'seller_lat',
    'geolocation_lng' : 'sellet_lng',
}, inplace=True)
dfSellerx = dfSellerx[['seller_id','seller_lat','sellet_lng']]
dfSellerx.head()


# ## Customer Dataset

# In[ ]:


dfCustomerx = pd.merge(dfCustomers, dfGeolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
dfCustomerx.rename(columns={
    'geolocation_lat' : 'customer_lat',
    'geolocation_lng' : 'customer_lng',
}, inplace=True)
dfCustomerx = dfCustomerx[['customer_id','customer_lat','customer_lng']]
dfCustomerx.head()


# # MERGING DATASET

# In[ ]:


df = pd.merge(dfOrders, dfOrdersItems, on='order_id', how='right')
df = df.merge(dfProducts, on='product_id')
df = df.merge(dfOrdersReviews, on='order_id')
df = df.merge(dfSellerx, on='seller_id')
df = df.merge(dfCustomerx, on='customer_id')
df = df.rename(columns={'price':'product_price','order_item_id':'quantity'})
df = df.drop(['review_id', 'review_creation_date','review_answer_timestamp','review_comment_title','review_comment_message','customer_id','product_id',], axis=1)
df.columns


# ## Filtering

# In[ ]:


df = df[df['order_status'] == 'delivered']
df.head()


# # CREATING ANOTHER COLUMNS THAT NEEDED
# ## Seller rating, product rating, number of product sold by seller and average price & rating for each product category
# ###### I created the columns in vscode because it takes a very long time but the algorithm is down below

# **SELLER RATING, PRODUCT RATING AND NUMBER OF PRODUCT SOLD BY SELLER**<br>
# > seller_ratingx = {}<br>
# product_ratingx = {}<br>
# product_soldx = {}<br>
# 
# > for item in df['seller_id'].unique():<br>
#     seller_ratingx[item] = round(df[df['seller_id'] == item].describe().iloc[1][3],1)<br>
#     product_soldx[item] = int(df[df['seller_id'] == item].describe().iloc[0][0])<br>
# 
# > for item in df['product_id'].unique():<br>
#     product_ratingx[item] = round(df[df['product_id'] == item].describe().iloc[1][3],1)<br>
#     product_soldx[item] = int(df[df['seller_id'] == item].describe().iloc[0][0])<br>
# 
# > seller_rating = []<br>
# product_sold = []<br>
# for item in df['seller_id']:<br>
#     seller_rating.append(seller_ratingx[item])<br>
#     product_sold.append(product_soldx[item])<br>
# 
# > product_rating = []<br>
# for item in df['product_id']:<br>
#     product_rating.append(product_ratingx[item])<br>
# 
# > df['seller_rating'] = seller_rating<br>
# df['product_sold'] = product_sold<br>
# df['product_rating'] = product_rating<br>
# 
# 
# **AVERAGE PRICE & RATING FOR EACH PRODUCT CATEGORY**<br>
# >avg_pricex = {}<br>
# avg_ratingx = {}<br>
# for item in df['product_category'].unique():<br>
#     avg_pricex[item] = round(df[df['product_category'] == item].describe().iloc[1][1],1)<br>
#     avg_ratingx[item] = round(df[df['product_category'] == item].describe().iloc[1][8],1)<br>
# 
# >avg_price = []<br>
# avg_rating = []<br>
# for item in df['product_category']:<br>
#     avg_price.append(avg_pricex[item])<br>
#     avg_rating.append(avg_ratingx[item])<br>
#     
# >df['avg_price'] = mean

# In[ ]:


df = pd.read_csv('../input/olist-modified-data/final_project_v2.csv')
df.head()


# ## Distance

# In[ ]:


from math import sin, cos, sqrt, atan2, radians
df['distance'] = df[['seller_lat','seller_lng','customer_lat','customer_lng']].apply(
    lambda row : round(6373.0 * (2 * atan2(sqrt((sin((radians(row['customer_lat']) - radians(row['seller_lat']))/2))**2 + cos(radians(row['seller_lat'])) * cos(radians(row['customer_lat'])) * (sin((radians(row['customer_lng']) - radians(row['seller_lng']))/2))**2), sqrt(1-((sin((radians(row['customer_lat']) - radians(row['seller_lat']))/2))**2 + cos(radians(row['seller_lat'])) * cos(radians(row['customer_lat'])) * (sin((radians(row['customer_lng']) - radians(row['seller_lng']))/2))**2)))))
    , axis=1
)
df.head()


# ## Freight Rate

# In[ ]:


df['freight_rate'] = df[['freight_value','quantity']].apply(
    lambda row : round(row['freight_value'] / row['quantity'],2), axis=1
)
df.head()


# ## Average Freight_Rate
# ###### I created the columns in vscode because it takes a very long time but the algorithm is down below
# > avg_freightx = {}<br>
# for item in df['distance'].unique():<br>
#     avg_freightx[item] = round(df[df['distance'] == item].describe().iloc[1][14],2)<br>
# 
# > avg_freight = []<br>
# for item in df['distance']:<br>
#     avg_freight.append(avg_freightx[item])<br>
#     
# > df['avg_freight'] = avg_freight<br>

# In[ ]:


df = pd.read_csv('../input/olist-modified-data/final_project_v4.csv')
df.head()


# ## Approving time, Processing time, Delivery time

# In[ ]:


for item in ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date','shipping_limit_date']:
    df[item] = pd.to_datetime(df[item])


# In[ ]:


df['approving_time'] = df[['order_purchase_timestamp','order_approved_at']].apply(
    lambda row : str(row['order_approved_at'] - row['order_purchase_timestamp']).split(' ')[0], axis=1
)
df['processing_time'] = df[['order_approved_at','order_delivered_carrier_date']].apply(
    lambda row : str(row['order_delivered_carrier_date'] - row['order_approved_at']).split(' ')[0], axis=1
)
df['delivery_time'] = df[['order_delivered_carrier_date','order_delivered_customer_date']].apply(
    lambda row : str(row['order_delivered_customer_date'] - row['order_delivered_carrier_date']).split(' ')[0], axis=1
)
df['courier_on_time'] = df[['order_delivered_customer_date','order_estimated_delivery_date']].apply(
    lambda row : 1 if row['order_delivered_customer_date'] <= row['order_estimated_delivery_date'] else 0, axis=1
)
df['seller_on_time'] = df[['order_delivered_carrier_date','shipping_limit_date']].apply(
    lambda row : 1 if row['order_delivered_carrier_date'] <= row['shipping_limit_date'] else 0, axis=1
)
df.head()


# In[ ]:


df = df[df.approving_time != 'NaT']
df = df[df.processing_time != 'NaT']
df = df[df.delivery_time != 'NaT']


# # CREATING DUMMY FOR SOME COLUMNS
# ## higher_product_price, better_product and higher_freight_rate

# In[ ]:


df['higher_product_price'] = df[['product_price','avg_price']].apply(
    lambda row: 1 if row['product_price'] > row['avg_price'] else 0, axis = 1
)
df['higher_freight_rate'] = df[['freight_rate','avg_freight']].apply(
    lambda row: 1 if row['freight_rate'] > row['avg_freight'] else 0, axis = 1
)
df['better_product'] = df[['product_rating','avg_rating']].apply(
    lambda row: 1 if row['product_rating'] > row['avg_rating'] else 0, axis = 1
)
df.head()


# ## Beautifying DataFrame

# In[ ]:


df = df[['product_rating','avg_rating','better_product','product_price','avg_price','higher_product_price','seller_rating','product_sold','distance','freight_rate','avg_freight','higher_freight_rate','approving_time','processing_time','delivery_time','courier_on_time','seller_on_time','review_score']]
df = df.rename(columns={
    'avg_rating' : 'avg_product_category_rating',
    'avg_price' : 'avg_product_category_price',
    'avg_freight' : 'avg_freight_rate',
    'product_sold' : 'product_sold_by_seller'
})
df.head()


# In[ ]:


df['approving_time'] = pd.to_numeric(df['approving_time'])
df['processing_time'] = pd.to_numeric(df['processing_time'])
df['delivery_time'] = pd.to_numeric(df['delivery_time'])


# In[ ]:


df = pd.read_csv('../input/olist-modified-data/final_project_v5.csv')
df = df.rename(columns={
    'better_product' : 'better_product_rating'
})
df = df.drop(['avg_product_category_rating','avg_product_category_price','avg_freight_rate'], axis=1)


# ## Checking Correlation

# In[ ]:


corr = df.corr()
corr['review_score']


# ## Dropping Columns
# Because the correlation of higher_product_price, higher_freight_rate, freight_rate and product_price are different with hypothesis

# In[ ]:


df = df.drop(['higher_product_price','higher_freight_rate','freight_rate','product_price'], axis=1)
corr = df.corr()
corr['review_score']


# # MACHINE LEARNING MODEL (Prediction)
# ### Without Cleaning Outliers Data

# ## Splitting

# In[ ]:


from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(
    df.drop('review_score', axis=1),
    df['review_score'],
    test_size = .1
)


# ## Decision Tree Classifier

# In[ ]:


from sklearn import tree 
model = tree.DecisionTreeClassifier()
model.fit(xTrain,yTrain)
print('model score =',model.score(xTrain,yTrain))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = model.predict(xTest)
print('accuracy =',accuracy_score(yTest, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = model.predict(xTrain)
forest_mse = mean_squared_error(yTrain, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# ## Random Forest Classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
model2 = RandomForestClassifier(n_estimators=100)
model2.fit(xTrain,yTrain)
print('model score =',model2.score(xTrain,yTrain))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = model2.predict(xTest)
print('accuracy =',accuracy_score(yTest, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = model2.predict(xTrain)
forest_mse = mean_squared_error(yTrain, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# since RandomForestClassifier has a better accuracy lets focus on it!

# # MACHINE LEARNING MODEL (Prediction)
# ## Cleaning Outliers Data

# ## Checking our data

# ## Histogram Before Cleaning

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.distplot(df[item])


# ## Boxplot Before Cleaning

# In[ ]:


fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.boxplot(df[item])


# since there are a lot of outliers data, so lets clean it!

# ## Cleaning 1.0
# droping any row which have value < (mean - (3 x std)) or > (mean + (3 x std))

# In[ ]:


df1 = df
for item in df1.describe().columns:
    df1 = df1[df[item] < (df1.describe()[item].iloc[1] + (df1.describe()[item].iloc[2]*3))]
    df1 = df1[df[item] > (df1.describe()[item].iloc[1] - (df1.describe()[item].iloc[2]*3))]


# after we clean the outliers lets check our data again!

# In[ ]:


df1.shape


# ## Histogram After Cleaning 1.0

# In[ ]:


fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df1.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.distplot(df1[item])


# ## Boxplot After Cleaning 1.0

# In[ ]:


fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df1.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.boxplot(df1[item])


# ## Checking Correlation After Cleaning 1.0

# In[ ]:


corr = df1.corr()
corr['review_score']


# there are NaN correlation from **courier_on_time** and **seller_on_time**, but lets ignore it!

# ## Splitting After Cleaning 1.0

# In[ ]:


from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(
    df1.drop('review_score', axis=1),
    df1['review_score'],
    test_size = .1
)


# ## Random Forrest Classifier After Cleaning 1.0

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelR1 = RandomForestClassifier(n_estimators=100)
modelR1.fit(xTrain,yTrain)
print('model score =',modelR1.score(xTrain,yTrain))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = modelR1.predict(xTest)
print('accuracy =',accuracy_score(yTest, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = modelR1.predict(xTrain)
forest_mse = mean_squared_error(yTrain, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# ## Cleaning 2.0 Using Z Score

# In[ ]:


df2 = df
from scipy import stats
z = np.abs(stats.zscore(df2.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'],axis=1)))
df2 = df2[(z<3).all(axis=1)]


# In[ ]:


df2.shape


# ## Histogram After Cleaning 2.0

# In[ ]:


fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df2.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.distplot(df2[item])


# ## Boxplot After Cleaning 2.0

# In[ ]:


fig = plt.figure(figsize = (18,15))
for i, item in enumerate (df2.drop(['better_product_rating','courier_on_time','seller_on_time','review_score'], axis=1)):
    plt.subplot(3,3,i+1)
    sns.boxplot(df2[item])


# ## Splitting After Cleaning 2.0

# In[ ]:


from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(
    df2.drop('review_score', axis=1),
    df2['review_score'],
    test_size = .1
)


# ## Random Forrest Classifier After Cleaning 2.0

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelR2 = RandomForestClassifier(n_estimators=100)
modelR2.fit(xTrain,yTrain)
print('model score =',modelR2.score(xTrain,yTrain))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = modelR2.predict(xTest)
print('accuracy =',accuracy_score(yTest, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = modelR2.predict(xTrain)
forest_mse = mean_squared_error(yTrain, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# **SUMMARY**<br>
# ** 1. RANDOM FOREST CLASSIFIER (Without Cleaning Outliers) **<br>
#   Model Score = 99.70<br>
#   Accuracy Score = 68.94%<br>
#   Error = 0.12236<br>
# ** 2. RANDOM FOREST CLASSIFIER (Cleaning Outliers 1.0) **<br>
#   Model Score = 99.67<br>
#   Accuracy Score = 69.48%<br>
#   Error = 0.12376<br>
#   **Note** : there are NaN correlation between **seller_on_time** and **courier_on_time** with **review_score**<br>
# ** 3. RANDOM FOREST CLASSIFIER (Cleaning Outliers 2.0 Using Z Score) **<br>
#   Model Score = 99.67<br>
#   Accuracy Score = 68.59%<br>
#   Error = 0.12825<br><br>
#   
#   Based on summary, I choose using data and model number 3 because the data is cleaner and the model score, accuracy and error was almost the same with the others

# # MACHINE LEARNING MODEL (Analysist)
# the idea is if your customer didn't give you 5 rating it's mean that he/she was not satisfied enough and might be one of the sellers, courier or the product itself that underperform. So we need to create another Machine Learning to analyze that

# ## Manual Splitting

# In[ ]:


xTrainPrediction = df.drop('review_score', axis=1).iloc[100:]
yTrainPrediction = df['review_score'].iloc[100:]
xTestPrediction = df.drop('review_score', axis=1).iloc[:100]
yTestPrediction = df['review_score'].iloc[:100]

xTrainProduct = df[['product_rating','better_product_rating']].iloc[100:]
yTrainProduct = df['review_score'].iloc[100:]
xTestProduct = df[['product_rating','better_product_rating']].iloc[:100]
yTestProduct = df['review_score'].iloc[:100]

xTrainSeller = df[['product_sold_by_seller','seller_rating','approving_time','processing_time','seller_on_time']].iloc[100:]
yTrainSeller = df['review_score'].iloc[100:]
xTestSeller = df[['product_sold_by_seller','seller_rating','approving_time','processing_time','seller_on_time']].iloc[:100]
yTestSeller = df['review_score'].iloc[:100]

xTrainCourier = df[['delivery_time','courier_on_time','distance']].iloc[100:]
yTrainCourier = df['review_score'].iloc[100:]
xTestCourier = df[['delivery_time','courier_on_time','distance']].iloc[:100]
yTestCourier = df['review_score'].iloc[:100]


# ## Prediction

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelPrediction = RandomForestClassifier(n_estimators=100)
modelPrediction.fit(xTrainPrediction,yTrainPrediction)
print('model score =',modelPrediction.score(xTrainPrediction,yTrainPrediction))


# ## Product Performance

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelProduct = RandomForestClassifier(n_estimators=100)
modelProduct.fit(xTrainProduct,yTrainProduct)
print('model score =',modelProduct.score(xTrainProduct,yTrainProduct))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = modelProduct.predict(xTestProduct)
print('accuracy =',accuracy_score(yTestProduct, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = modelProduct.predict(xTrainProduct)
forest_mse = mean_squared_error(yTrainProduct, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# ## Seller Performance

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelSeller = RandomForestClassifier(n_estimators=100)
modelSeller.fit(xTrainSeller,yTrainSeller)
print('model score =',modelSeller.score(xTrainSeller,yTrainSeller))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = modelSeller.predict(xTestSeller)
print('accuracy =',accuracy_score(yTestSeller, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = modelSeller.predict(xTrainSeller)
forest_mse = mean_squared_error(yTrainSeller, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# ## Courier Performance

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
modelCourier = RandomForestClassifier(n_estimators=100)
modelCourier.fit(xTrainCourier,yTrainCourier)
print('model score =',modelCourier.score(xTrainCourier,yTrainCourier))


# In[ ]:


from sklearn.metrics import accuracy_score
prediction = modelCourier.predict(xTestCourier)
print('accuracy =',accuracy_score(yTestCourier, prediction)*100,'%')


# In[ ]:


from sklearn.metrics import mean_squared_error
predictions = modelCourier.predict(xTrainCourier)
forest_mse = mean_squared_error(yTrainCourier, predictions)
forest_rmse = np.sqrt(forest_mse)
print('error = ',forest_rmse)


# # Analyzing

# In[ ]:


for i in range (0,100,10):
    print('index ',i)
    print('actual data =', yTestPrediction.iloc[i])
    print('rating prediction = ', modelPrediction.predict([xTestPrediction.iloc[i]]))
    print('product performance = ', modelProduct.predict([xTestProduct.iloc[i]]))
    print('seller performance = ', modelSeller.predict([xTestSeller.iloc[i]]))
    print('courier performane = ', modelCourier.predict([xTestCourier.iloc[i]]))
    print('----------------------------------------------------------------------------')


# pretty good isn't it?<br>
# let's analyze base on those data<br>
# we got wrong prediction in **index 10** while the other is fine<br>
# in **index 0, 40, 50** the customer didn't give you 5 rating because he/she didn't satisfied with the product<br> 
# in **index 20, 30, 70, 80, 90** the customer satisfied with all of the performance as our model predict that either product, seller and courier perfomance is good<br>
# in **index 60** the customer give us 5 rating even the courier performance was bad in can be indicated the customer didn't really care the courier performance as long as the product is good<br><br>
# let's take a look from another data to make sure our model is good enough

# In[ ]:


for i in range (0,100,10):
    print('index ',i+5)
    print('actual data =', yTestPrediction.iloc[i+5])
    print('rating prediction = ', modelPrediction.predict([xTestPrediction.iloc[i+5]]))
    print('product performance = ', modelProduct.predict([xTestProduct.iloc[i+5]]))
    print('seller performance = ', modelSeller.predict([xTestSeller.iloc[i+5]]))
    print('courier performane = ', modelCourier.predict([xTestCourier.iloc[i+5]]))
    print('----------------------------------------------------------------------------')


# we got wrong prediction in **index 15,55 and 75** <br>
# in **index 65 and 95** itindicate that the customer didn't really care with the courier performance as long as the product performas was good as I said before
