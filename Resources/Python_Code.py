# -*- coding: utf-8 -*-
"""SINHA_Predictive Analysis- CryptoCurrency.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16M5bpPLbPImt87ioKJdVox2lA-NZt40S

Predictive Analysis : Crypto-Currency

Phase 1: Data Exploration and Preparation
"""

# Importing Libraries
import pandas as pd
import numpy as np

# Load the dataset
bitcoin_df = pd.read_csv('bitcoin.csv')
ethereum_df = pd.read_csv('ethereum.csv')

print(bitcoin_df.info())

print(ethereum_df.info())

# BITCOIN: Calculate measures of central tendency and dispersion for numerical features
numerical_features = bitcoin_df.select_dtypes(include=[np.number])
central_tendency = numerical_features.agg(['mean', 'median'])
dispersion = numerical_features.agg(['std'])

# Analyze frequencies for categorical features
categorical_features = bitcoin_df.select_dtypes(include=[object])
categorical_frequencies = categorical_features.apply(pd.Series.value_counts)

# Summary of findings
print("Bitcoin's Central Tendency (Mean, Median):")
print(central_tendency)
print("\nDispersion (Bitcoin's Standard Deviation):")
print(dispersion)
print("\nBitcoin's Categorical Frequencies:")
print(categorical_frequencies)

# ETHEREUM: Calculate measures of central tendency and dispersion for numerical features
numerical_features = ethereum_df.select_dtypes(include=[np.number])
central_tendency = numerical_features.agg(['mean', 'median'])
dispersion = numerical_features.agg(['std'])

# Analyze frequencies for categorical features
categorical_features = ethereum_df.select_dtypes(include=[object])
categorical_frequencies = categorical_features.apply(pd.Series.value_counts)

# Summary of findings
print("Ethereum's Central Tendency (Mean, Median):")
print(central_tendency)
print("\nDispersion (Ethereum's Standard Deviation):")
print(dispersion)
print("\nEthereum's Categorical Frequencies:")
print(categorical_frequencies)

# Missing values for Bitcoin
missing_values = bitcoin_df.isnull().sum()

# Display the cleaned data and missing value summary
bitcoin_df.head(), missing_values

# Missing values for ethereum
missing_values = ethereum_df.isnull().sum()

# Display the cleaned data and missing value summary
ethereum_df.head(), missing_values

# Convert 'Date' column to datetime format
bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])
ethereum_df['Date'] = pd.to_datetime(ethereum_df['date'])

"""Visualization"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Line graph for Closing price of Bitcoin
plt.figure(figsize=(8, 5))
plt.plot(bitcoin_df['Date'], bitcoin_df['Close'], color='blue',)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.title("Closing price of Bitcoin over time")
plt.xlabel("Month/Year")
plt.ylabel("Closing Price")
plt.show()

# Line graph for Closing price of Ethereum
plt.figure(figsize=(10, 5))
plt.plot(ethereum_df['Date'], ethereum_df['Close'], color='orange')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=9))
plt.title("Closing price of Ethereum over time")
plt.xlabel("Month/Year")
plt.ylabel("Closing Price")
plt.show()

# Scatter plot of Open vs Close price of Bitcoin
plt.scatter(bitcoin_df['Open'], bitcoin_df['Close'],  color='blue', alpha=0.5)
plt.xlabel('Open Price')
plt.ylabel('Close Price')
plt.title('Open vs Close Price')
plt.show()

# Scatter plot of Open vs Close price of Ethereum
plt.scatter(ethereum_df['Open'], ethereum_df['Close'], color='orange', alpha=0.5)
plt.xlabel('Open Price')
plt.ylabel('Close Price')
plt.title('Open vs Close Price')
plt.show()

# Rolling window for Bitcoin
bitcoin_df['120_day_ma'] = bitcoin_df['Close'].rolling(window=120).mean()
# Rolling window for Ethereum
ethereum_df['120_day_ma'] = ethereum_df['Close'].rolling(window=120).mean()

# Line graph of bitcoin of 120 days moving averages
plt.figure(figsize=(9, 5))
plt.plot(bitcoin_df['Date'], bitcoin_df['120_day_ma'], color='purple', label='120-day MA')
plt.title("Closing price of Bitcoin over 120 days moving averages")
plt.xlabel("120 days Interval")
plt.ylabel("Closing Average")
plt.show()

# Line graph of ethereum of 120 days moving averages
plt.figure(figsize=(9, 5))
plt.plot(ethereum_df['Date'], ethereum_df['120_day_ma'], color='blue', label='120-day MA')
plt.title("Closing price of Ethereum over 120 days moving averages")
plt.xlabel("120 days Interval")
plt.ylabel("Closing Average")
plt.show()

# Feature engineering
bitcoin_df['Price_change'] = bitcoin_df['Close'] - bitcoin_df['Open']
bitcoin_df['Spread'] = bitcoin_df['High'] - bitcoin_df['Low']
bitcoin_df['Target'] = bitcoin_df['Close'].shift(-1)

ethereum_df['Price_change'] = ethereum_df['Close'] - ethereum_df['Open']
ethereum_df['Spread'] = ethereum_df['High'] - ethereum_df['Low']
ethereum_df['Target'] = ethereum_df['Close'].shift(-1)

print(bitcoin_df[['Price_change', 'Spread', 'Target']].head())
print("\n", ethereum_df[['Price_change', 'Spread', 'Target']].head())

# Check for currency
bitcoin_df.head()
usd = (bitcoin_df['Currency'] == "USD").all()
if usd:
    print("All values in the 'Currency' column are 'USD' for Bitcoin.")

ethereum_df.head()
usd = (ethereum_df['Currency'] == "USD").all()
if usd:
    print("All values in the 'Currency' column are 'USD' for Ethereum.")

btc_df = bitcoin_df.drop(columns=['Currency'])
ethm_df = ethereum_df.drop(columns=['Currency'])

import seaborn as sns
numerical_btc = btc_df.select_dtypes(include=np.number).columns
corr_matrix = btc_df[numerical_btc].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Bitcoin')
plt.show()

numerical_ethm = ethm_df.select_dtypes(include=np.number).columns
corr_matrix = ethm_df[numerical_ethm].corr()
sns.heatmap(corr_matrix, annot=True, cmap='plasma')
plt.title('Correlation Matrix of Ethereum')
plt.show()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
btc_scaled = scaler.fit_transform(btc_df[['Open', 'High', 'Low','Price_change','Spread','Target' ]])
eth_scaled = scaler.fit_transform(ethm_df[['Open', 'High', 'Low', 'Price_change','Spread', 'Target']])

"""Phase 2: Feature Selection

Scope of the Next Section is Only Bitcoin's dataset
"""

btc_scaled_df = pd.DataFrame(btc_scaled, columns=['Open', 'High', 'Low', 'Price_change', 'Spread', 'Target'])

btc_scaled_df1 = btc_scaled_df.dropna() # any missing value is dropped
x = btc_scaled_df1[['Open', 'High', 'Low', 'Price_change', 'Spread']]  # :features
y = btc_scaled_df1['Target']  # :target variable

# Importing Libraries
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_error

# Using SelectKBest
k_best = SelectKBest(score_func=f_regression, k=5)
x_train_btc_kbest = k_best.fit_transform(x, y)

print(k_best.scores_,"\n")
print("Shape of the dataset :",x_train_btc_kbest.shape)

# Calculating RFE
estimator = LinearRegression()
selector = RFE(estimator, n_features_to_select=5)

selector.fit(x, y)
print(selector.support_)
print(selector.ranking_)

# using LASSO
lasso_cv = LassoCV(cv=5)
lasso_cv.fit(x, y)

# Get the best alpha
best_alpha = lasso_cv.alpha_
print("Best Alpha:", best_alpha)

# Print selected features
selected_features = [f for f, c in zip(x.columns, lasso_cv.coef_) if c != 0]
print("Selected Features:", selected_features)

"""Phase 3: Model Training and Evaluation"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor
#Random Forest
rand_forest = RandomForestRegressor()
rand_forest.fit(x_train, y_train)
rand_forest_pred = rand_forest.predict(x_test)
print(rand_forest.feature_importances_)

#Linear Regression
linear_reg = LinearRegression()
linear_reg.fit(x_train, y_train)
linear_reg_pred = linear_reg.predict(x_test)
print(linear_reg.coef_)

#KNN Regressor
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(x_train, y_train)
knn_pred = knn.predict(x_test)
print(knn.get_params())

#Checking Root Mean Squared Error (RMSE)
rand_forest_rmse = np.sqrt(mean_squared_error(y_test, rand_forest_pred))
linear_reg_rmse = np.sqrt(mean_squared_error(y_test, linear_reg_pred))
knn_rmse = np.sqrt(mean_squared_error(y_test, knn_pred))

print("Random Forest :", rand_forest_rmse)
print("Linear Regression :", linear_reg_rmse)
print("KNN : ", knn_rmse)

actual_price = y_test.values
predicted_price_rf = rand_forest_pred
plt.figure(figsize=(12, 9))
plt.plot(actual_price, label="Actual Prices", color="blue", marker='o')
plt.plot(predicted_price_rf, label="Predicted Prices", color="red", marker='x')
plt.title("Actual vs Predicted Prices (Random Forest)", fontsize=14)
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

predicted_price_lr = linear_reg_pred
plt.figure(figsize=(12, 9))
plt.plot(actual_price, label="Actual Prices", color="blue", marker='+')
plt.plot(predicted_price_lr, label="Predicted Prices", color="green", marker='^')
plt.title("Actual vs Predicted Prices (Linear Regression)", fontsize=14)
plt.xlabel("Time ")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

predicted_price_knn = knn_pred
plt.figure(figsize=(12, 9))
plt.plot(actual_price, label="Actual Prices", color="blue", marker='*')
plt.plot(predicted_price_knn, label="Predicted Prices", color="red", marker='^')
plt.title("Actual vs Predicted Prices (KNN)", fontsize=14)
plt.xlabel("Time ")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

# Comparison of Actual vs Predicted prices
comparison_df = pd.DataFrame({
    'Actual Price': actual_price.flatten(),
    'Random Forest Prediction': predicted_price_rf.flatten(),
    'Linear Regression Prediction': predicted_price_lr.flatten(),
    'KNN Prediction': knn_pred.flatten()
})

comparison_df['Closest Model'] = comparison_df[['Random Forest Prediction',
                                                'Linear Regression Prediction',
                                                'KNN Prediction']].apply(
    lambda row: row.idxmin(), axis=1
)
print("\nComparison of Actual vs Predicted Prices:")
print(comparison_df.head(10))

comparison_df.to_csv("Prediction_Comparison.csv", index=False)
print("\nThe comparison table has been saved as 'Prediction_Comparison.csv'.")

comparison_df['RF Error'] = abs(comparison_df['Actual Price'] - comparison_df['Random Forest Prediction'])
comparison_df['LR Error'] = abs(comparison_df['Actual Price'] - comparison_df['Linear Regression Prediction'])
comparison_df['KNN Error'] = abs(comparison_df['Actual Price'] - comparison_df['KNN Prediction'])

mean_errors = {
    'Random Forest': comparison_df['RF Error'].mean(),
    'Linear Regression': comparison_df['LR Error'].mean(),
    'KNN': comparison_df['KNN Error'].mean()
}

best_model = min(mean_errors, key=mean_errors.get)

print("\nMean Absolute Errors for Each Model:")
for model, error in mean_errors.items():
    print(f"{model}: {error:.4f}")

print(f"\nThe best-performing model based on mean absolute error is: {best_model}")