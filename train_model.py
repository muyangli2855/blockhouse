import os
import django
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blockhouse.settings')

# Set up Django
django.setup()

# Now you can import your models
from financials.models import StockData

# Fetch stock data from your Django model (you can modify the query as needed)
stock_data = StockData.objects.filter(symbol='AAPL').order_by('date')

# Check if there's data available for the given symbol
if not stock_data.exists():
    print("No stock data available for this symbol.")
    exit()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(list(stock_data.values('date', 'close_price')))
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Ensure there's enough data to train the model
if len(df) < 2:
    print("Not enough data points to train the model.")
    exit()

# Prepare the input features and target variable
df['day'] = range(len(df))  # Using "day" as a feature (time progression)
X = df[['day']]  # Input feature (could be enhanced with more features)
y = df['close_price']  # Target variable (stock price)

# Split the data into training and test sets (optional)
train_size = int(len(df) * 0.8)  # 80% for training, 20% for testing
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train the model and handle errors
try:
    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model to a .pkl file
    joblib.dump(model, 'stock_model.pkl')
    print("Model trained and saved successfully!")

except Exception as e:
    print(f"An error occurred during model training: {e}")
