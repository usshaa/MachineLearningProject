from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from django.conf import settings
import os


def analyze(request):
    # dataset path

    file_path = os.path.join(settings.MEDIA_ROOT, 'Sales_Data/')

    fileNames = os.listdir(file_path)

    fileNames = [file for file in fileNames if '.csv' in file]

    # new dataframe

    new_data = pd.DataFrame()

    # reading and merging .csv file

    for file in fileNames:
        df = pd.read_csv(file_path + file)
        new_data = pd.concat([new_data, df])

    # storing new dataset
    new_data.to_csv('all_data.csv', index=False)

    # loading new dataset
    new_df = pd.read_csv("all_data.csv")

    # Droping null values
    new_df = new_df.dropna(how='all')

    # Checking str Or in Order Date
    new_df = new_df[new_df['Order Date'].str[0:2] != 'Or']

    # Extracting month from order date
    new_df['Month'] = new_df['Order Date'].str[0:2]

    # Change datatype of month to integer type
    new_df['Month'] = new_df['Month'].astype('int32')

    # Change datatype to numeric
    new_df['Quantity Ordered'] = pd.to_numeric(new_df['Quantity Ordered'])
    new_df['Price Each'] = pd.to_numeric(new_df['Price Each'])

    # Creation of new columns as Sales
    new_df['Sales'] = new_df['Quantity Ordered'] * new_df['Price Each']

    # Overall sum of Sales in a Month
    new_df.groupby('Month').sum()

    # plotting monthly sales detail
    months = range(1, 13)
    results = new_df.groupby('Month').sum()

    plt.bar(months, results['Sales'])
    plt.xticks(months)
    labels, location = plt.yticks()
    plt.yticks(labels, (labels / 1000000).astype(int))
    plt.xlabel('Month Number')
    plt.ylabel('Sales in millions USD')
    plt.show()
    # plt.savefig('static/image/plot1.png',dpi=300)

    # Creation of new column as City
    new_df['City'] = new_df['Purchase Address'].apply(lambda x: x.split(',')[1] + ' ' + x.split(',')[2].split(' ')[1])

    # Citywise Sales details
    result2 = new_df.groupby('City').sum()

    # Plotting Citywise Sales Details
    # cities = new_df['City'].unique()
    cities = [city for city, df in new_df.groupby('City')]

    plt.bar(cities, result2['Sales'])
    plt.xticks(cities, rotation='vertical', size=8)
    labels, location = plt.yticks()
    plt.yticks(labels, (labels / 1000000).astype(int))
    plt.xlabel('City Name')
    plt.ylabel('Sales in millions USD')
    plt.show()
    # plt.savefig('static/image/plot2.jpg',dpi=300)

    # Type casting Order_Date_Type to_datetime

    new_df['Order_Date_Type'] = pd.to_datetime(new_df['Order Date'])

    # Extracting Hour Column from Order_Date_Type

    new_df['Hour'] = new_df['Order_Date_Type'].dt.hour

    # Calculate count of Hour spending to Purchase
    result3 = new_df.groupby(['Hour']).count()

    # Plotting Quantity Ordered in a Different time Period
    result3 = new_df.groupby(['Hour'])['Quantity Ordered'].count()
    hours = [hour for hour, df in new_df.groupby('Hour')]

    plt.plot(hours, result3)
    plt.xticks(hours)
    plt.xlabel('Hour')
    plt.ylabel('Number of Orders')
    plt.grid()
    plt.show()
    # plt.savefig('static/image/plot3.jpg',dpi=300)

    # Checking duplicated Order ID
    all_df = new_df[new_df['Order ID'].duplicated(keep=False)]

    # Bundling Product by Order ID
    all_df['Product_Bundle'] = all_df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

    # Dropping duplicates datas in Order ID & Product_Bundle
    all_df = all_df[['Order ID', 'Product_Bundle']].drop_duplicates()

    # Counting no of bundle product
    count = Counter()

    for row in all_df['Product_Bundle']:
        row_list = row.split(',')
        #     count.update(Counter(combinations(row_list,2)))
        count.update(Counter(combinations(row_list, 3)))
    # print(count)
    count.most_common(10)

    # Plotting sum of Product and Quantity ordered
    product_group = new_df.groupby('Product')

    quantity_ordered = product_group.sum()['Quantity Ordered']

    products = [product for product, df in product_group]

    plt.bar(products, quantity_ordered)
    plt.xticks(products, rotation="vertical", size=8)
    plt.xlabel('Product')
    plt.ylabel('Quantity Ordered')
    plt.show()
    # plt.savefig('static/image/plot4.jpg',dpi=300)

    # Plotting Product of Quantity ordered and Price
    prices = new_df.groupby('Product').mean()['Price Each']

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.bar(products, quantity_ordered, color='g')
    ax2.plot(products, prices, 'b-')

    ax1.set_xlabel('Product Name')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price ($)', color='b')
    ax1.set_xticklabels(products, rotation='vertical', size=8)

    plt.show()
    # plt.savefig('static/image/plot5.jpg',dpi=300)

    # storing tranformed data for modeling

    new_df.to_csv('analyseddata.csv', index=False)

def plot(request):
    return render(request, 'plot.html')

def visual(request):
    return render(request, 'visual.html')


import csv
from django.http import JsonResponse

def csv_data(request):
    with open('analyseddata.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {'products': [], 'quantity_ordered': [], 'price_each': [], 'month': [], 'city': [], 'hour': [], 'sales': []}
        for row in reader:
            data['products'].append(row['Product'])
            data['quantity_ordered'].append(int(row['Quantity Ordered']))
            data['price_each'].append(float(row['Price Each']))
            data['month'].append(row['Month'])
            data['city'].append(row['City'])
            data['hour'].append(int(row['Hour']))
            data['sales'].append(float(row['Sales']))
    return JsonResponse(data)
