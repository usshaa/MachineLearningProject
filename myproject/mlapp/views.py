from django.shortcuts import render
from .forms import PredictionForm
import pandas as pd
from sklearn.tree import DecisionTreeRegressor,plot_tree
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt

def createmodel(request):
    # Read csv
    # Load the data into a Pandas dataframe
    data = pd.read_csv('analyseddata.csv')
    # Split the data into features (X) and target (y)
    X = data[['Product', 'Quantity Ordered', 'Price Each', 'Month', 'City', 'Hour']]
    y = data['Sales']
    # Convert categorical variables to numerical using one-hot encoding
    X = pd.get_dummies(X, columns=['Product', 'City'])
    # Print the column names and their values
    print(X.columns)
    print(X.head())
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Save the column names
    with open('columns.pkl', 'wb') as f:
        pickle.dump(X.columns, f)
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    # Visualize the decision tree
    fig, ax = plt.subplots(figsize=(15, 10))
    plot_tree(model, filled=True, feature_names=X.columns,max_depth=3,fontsize = 14,label = "all",rounded=True, ax=ax)
    plt.savefig('static/image/decision_tree.png',dpi=300)

    # Predicting the Test set results
    predictions = model.predict(X_test)
    # save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    return render(request,'ml.html')


def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Load the saved model
            model = pickle.load(open('finalized_model.sav', 'rb'))

            # Get the form data
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            month = form.cleaned_data['month']
            city = form.cleaned_data['city']
            hour = form.cleaned_data['hour']

            # Create a DataFrame with the input data
            data = pd.DataFrame({'Product': [product], 'Quantity Ordered': [quantity], 'Price Each': [price],
                                 'Month': [month], 'City': [city], 'Hour': [hour]})

            # Convert categorical variables to numerical using one-hot encoding
            data = pd.get_dummies(data, columns=['Product','City'])

            # Load the column names used during training
            with open('columns.pkl', 'rb') as f:
                columns = pickle.load(f)

            # Ensure input data has same columns as during training
            missing_cols = set(columns) - set(data.columns)
            for c in missing_cols:
                data[c] = 0
            data = data[columns]

            # Make prediction
            prediction = model.predict(data)[0]
            context = {'form': form, 'prediction': prediction,'product':product,'quantity':quantity,'price':price,'month':month,'city':city,'hour':hour}
            return render(request, 'result.html', context)
    else:
        form = PredictionForm()
        context = {'form': form}
        return render(request, 'index.html', context)




