# -*- coding: utf-8 -*-
"""Sales Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qg-Ua2a4NgDIi1eohowIdL47Y5XT4fIt

Importing Libraries
"""

# basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.tight_layout()
import os
import statsmodels.formula.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import warnings

# sklearn modules
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib

# remove warnings
import warnings
warnings.filterwarnings('ignore')
print('Successfully Load Libraries')

# read data and remove unnecessary column
df = pd.read_csv("/content/Advertising.csv")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

print('Successfully Read Data')

# data head
df.head()

# data summary
df.describe()

"""Missing Values"""

# check for missing values
print(df.isnull().sum())

print("\nData has no missing values")

# check for duplicates
print("Number of duplicates:", df.duplicated().sum())

"""Outliers"""

# check for outliers
plt.figure(figsize=(15, 5))
sns.boxplot(data=df)
plt.title("Outliers in the data")
plt.show()

# show outlier rows in the data
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
df[(df["Newspaper"] > (Q3["Newspaper"] + 1.5 * IQR["Newspaper"]))]

# remove outliers using IQR
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

print('After removing outliers:')

# check for outliers
plt.figure(figsize=(12, 6))
sns.boxplot(data=df)
plt.title("Outliers in the data")
plt.show()

"""Analysis on Independet Features"""

# Plot histograms for independent variables
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(df['TV'], kde=True, color='blue')
plt.title('Distribution of TV Advertising')

plt.subplot(1, 3, 2)
sns.histplot(df['Radio'], kde=True, color='green')
plt.title('Distribution of Radio Advertising')

plt.subplot(1, 3, 3)
sns.histplot(df['Newspaper'], kde=True, color='orange')
plt.title('Distribution of Newspaper Advertising')

plt.show()

"""Skewness"""

# find skewness
print("Skewness in TV column:", df["TV"].skew())
print("Skewness in Radio column:", df["Radio"].skew())
print("Skewness in Newspaper column:", df["Newspaper"].skew())

# Interpretation of skewness values
print("\nInterpretation of Skewness : ")
print("Skewness > 0: Right skewed distribution (positive skew)")
print("Skewness = 0: Symmetrical distribution")
print("Skewness < 0: Left skewed distribution (negative skew)")

"""Kurtosis"""

# find kurtosis
print("Kurtosis in TV column:", df["TV"].kurtosis())
print("Kurtosis in Radio column:", df["Radio"].kurtosis())
print("Kurtosis in Newspaper column:", df["Newspaper"].kurtosis())
print("Kurtosis in Sales column:", df["Sales"].kurtosis())

# Interpretation of kurtosis values
print("\nInterpretation of Kurtosis:")
print("Kurtosis > 3: Leptokurtic distribution (heavy tails)")
print("Kurtosis = 3: Mesokurtic distribution (normal distribution)")
print("Kurtosis < 3: Platykurtic distribution (light tails)")

"""Features Relationship with target variable"""

# Create a figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # 1 row, 3 columns

# LM plot for TV vs Sales
sns.regplot(x='TV', y='Sales', data=df,
            scatter_kws={'color': 'blue', 'alpha': 0.8},
            line_kws={'color': 'red', 'linewidth': 2.5},
            ax=axes[0])
axes[0].set_title('TV Advertising vs Sales', fontsize=14)
axes[0].set_xlabel('TV Advertising Budget', fontsize=12)
axes[0].set_ylabel('Sales', fontsize=12)

# LM plot for Radio vs Sales
sns.regplot(x='Radio', y='Sales', data=df,
            scatter_kws={'color': 'green', 'alpha': 0.8},
            line_kws={'color': 'purple', 'linewidth': 2.5},
            ax=axes[1])
axes[1].set_title('Radio Advertising vs Sales', fontsize=14)
axes[1].set_xlabel('Radio Advertising Budget', fontsize=12)
axes[1].set_ylabel('Sales', fontsize=12)

# LM plot for Newspaper vs Sales
sns.regplot(x='Newspaper', y='Sales', data=df,
            scatter_kws={'color': 'orange', 'alpha': 0.8},
            line_kws={'color': 'brown', 'linewidth': 2.5},
            ax=axes[2])
axes[2].set_title('Newspaper Advertising vs Sales', fontsize=14)
axes[2].set_xlabel('Newspaper Advertising Budget', fontsize=12)
axes[2].set_ylabel('Sales', fontsize=12)

# Adjust layout for better spacing
plt.tight_layout()
# Show the plots
plt.show()

"""Distribution"""

# Plot histogram for the target variable
plt.figure(figsize=(10, 5))
sns.histplot(df['Sales'], kde=True, color='purple')
plt.title('Distribution of Sales')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.show()

"""Skewness & Kurtosis"""

# Calculate skewness and kurtosis
sales_skewness = df['Sales'].skew()
sales_kurtosis = df['Sales'].kurtosis()

print(f"Skewness of Sales: {sales_skewness}")
print(f"Kurtosis of Sales: {sales_kurtosis}")

"""Transformation"""

# Apply square root transformation on target variable
df['Sales']= np.sqrt(df['Sales']).round(4)

# check distribution after applying square root transformation
plt.figure(figsize=(10, 5))
sns.histplot(df['Sales'], kde=True, color='purple')
plt.title('Distribution of Sales')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.show()

"""Skewness & Kurtosis After Transformation"""

# Calculate skewness and kurtosis after applying transformation
sales_skewness = df['Sales'].skew()
sales_kurtosis = df['Sales'].kurtosis()

print('After applying square root transformation \n')
print(f"Skewness of Sales: {sales_skewness}")
print(f"Kurtosis of Sales: {sales_kurtosis}")

"""Features Creation"""

# Feature Engineering: Create new features
df["Total_Advertising"] = df["TV"] + df["Radio"] + df["Newspaper"]
df["TV_Radio_Interaction"] = df["TV"] * df["Radio"]

print('Successfully created new features')

"""Correlation"""

# Calculate the correlation matrix
correlation_matrix = df.corr()
correlation_matrix

# Display the correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='Set1', linewidths=0.5)
plt.title('Correlation Matrix of Advertising Data')
plt.show()

"""**Build ML Model**"""

# Split the data
X = df.drop("Sales", axis=1)
y = df["Sales"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps
preprocessor = Pipeline(steps=[
    ("scaler", StandardScaler())  # Normalize features
])
# Define models and their hyperparameter grids
models = {
    "linear_regression": (LinearRegression(), {}),
    "ridge_regression": (Ridge(), {"ridge_regression__alpha": [0.1, 1.0, 10.0]}),
    "lasso_regression": (Lasso(), {"lasso_regression__alpha": [0.1, 1.0, 10.0]}),
    "decision_tree": (DecisionTreeRegressor(random_state=42), {"decision_tree__max_depth": [5, 10, 20]}),
    "random_forest": (RandomForestRegressor(random_state=42), {"random_forest__n_estimators": [50, 100], "random_forest__max_depth": [10, 20]}),
    "gradient_boosting": (GradientBoostingRegressor(random_state=42), {"gradient_boosting__n_estimators": [50, 100], "gradient_boosting__learning_rate": [0.1, 0.2]}),
    "support_vector_regression": (SVR(), {"support_vector_regression__C": [0.1, 1.0], "support_vector_regression__kernel": ["linear", "rbf"]}),
    "k_nearest_neighbors": (KNeighborsRegressor(), {"k_nearest_neighbors__n_neighbors": [3, 5, 7]}),
    "xgboost": (XGBRegressor(random_state=42), {"xgboost__n_estimators": [50, 100], "xgboost__learning_rate": [0.1, 0.2]})
}
# Create a pipeline for each model and perform hyperparameter tuning
results = {}

for model_name, (model, param_grid) in models.items():
    print(f"Training {model_name}...")
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        (model_name, model)
    ])

     # Use GridSearchCV for hyperparameter tuning
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="r2")
    grid_search.fit(X_train, y_train)

    # Evaluate the model
    y_pred = grid_search.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Store results
    results[model_name] = {
        "Best Parameters": grid_search.best_params_,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R²": r2
    }
  # Sort the results by RMSE in ascending order
sorted_results = sorted(results.items(), key=lambda x: x[1]["RMSE"])

# Print sorted results
print("\nModel Evaluation Results (Sorted by RMSE in Ascending Order):")
for model_name, result in sorted_results:
    print(f"{model_name}:")
    print(f"  Best Parameters: {result['Best Parameters']}")
    print(f"  MAE: {result['MAE']}")
    print(f"  MSE: {result['MSE']}")
    print(f"  RMSE: {result['RMSE']}")
    print(f"  R²: {result['R²']}")
    print()

# Display the best model with all metrics
best_model_name = sorted_results[0][0]
best_model_result = sorted_results[0][1]
print("\nBest Model:")
print(f"{best_model_name}:")
print(f"  Best Parameters: {best_model_result['Best Parameters']}")
print(f"  MAE: {best_model_result['MAE']}")
print(f"  MSE: {best_model_result['MSE']}")
print(f"  RMSE: {best_model_result['RMSE']}")
print(f"  R²: {best_model_result['R²']}")

"""**Prediction using Linear Regression Model**"""

# Model Preparation
X = df.drop('Sales', axis=1)
y = df[["Sales"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=46)

# Linear Regression Model
lin_model = sm.ols(formula="Sales ~ TV + Radio + Newspaper", data=df).fit()

# Define a list of models to evaluate
models = [('LinearRegression', LinearRegression())]

for name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"{name}: RMSE = {rmse:.2f}")

# Linear Regression Model

lin_model = sm.ols(formula="Sales ~ TV + Radio + Newspaper", data=df).fit()
# Make predictions on new data
new_data_1 = pd.DataFrame({'TV': [100], 'Radio': [50], 'Newspaper': [25]})
predicted_sales_1 = lin_model.predict(new_data_1)
print("Predicted Sales (Data 1):", predicted_sales_1)

"""**Prediction using XGboost Model**"""

# Generate additional features
df['Total_Advertising'] = df['TV'] + df['Radio'] + df['Newspaper']
df['TV_Radio_Interaction'] = df['TV'] * df['Radio']

# Define features and target variable
X = df[['TV', 'Radio', 'Newspaper', 'Total_Advertising', 'TV_Radio_Interaction']]
y = df['Sales']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost model with optimized parameters
xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=20, learning_rate=0.1, max_depth=2)

# Train the model
xgb_model.fit(X_train, y_train)

# Predict on test data
y_pred = xgb_model.predict(X_test)

# Evaluate model performance
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"XGBoost: RMSE = {rmse:.2f}")

# Prepare new data for prediction
new_data_1 = pd.DataFrame({'TV': [100], 'Radio': [50], 'Newspaper': [25]})
new_data_1['Total_Advertising'] = new_data_1['TV'] + new_data_1['Radio'] + new_data_1['Newspaper']
new_data_1['TV_Radio_Interaction'] = new_data_1['TV'] * new_data_1['Radio']

# Predict sales for the new data point
predicted_sales_1 = xgb_model.predict(new_data_1)
print("Predicted Sales (Data 1):", predicted_sales_1)