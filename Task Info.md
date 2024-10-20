# Backend Engineer Trial Task

### Revised Trial Task for Experienced Django Developer

**Objective**:

Create a Django-based backend system that fetches financial data from a specific public API, stores it in a relational database, implements a basic backtesting module using this historical data, and generates reports with performance results. The focus is on Django development, API integration, and deployment. The machine learning aspect will be prepared in a simplified way, but it should not require building or deeply understanding machine learning models.

------

### Step-by-Step Breakdown

### 1. **Fetch Financial Data**

- **API to Use**: Alpha Vantage (https://www.alphavantage.co/documentation/)

- **Data to Fetch**: Daily stock prices for a specific stock symbol (e.g., AAPL) over the past 2 years.

- Required Fields

  :

  - Open price
  - Close price
  - High price
  - Low price
  - Volume

- **Storage**: Store the fetched data in a PostgreSQL database. The table structure should be clear and optimized for querying, including timestamps for the financial data.

**Deliverables for this step**:

- Django view or background task that fetches the financial data.
- Proper database schema using Django ORM for storing the financial data.
- Code should include error handling (e.g., rate limits, network issues).

### 2. **Backtesting Module**

- Goal

  : Implement a basic backtesting strategy where users can input simple parameters, such as:

  - Initial investment amount
  - Buy when the stock price dips below a moving average (e.g., 50-day average).
  - Sell when the stock price goes above a different moving average (e.g., 200-day average).

- Output

  :

  - Calculate the return on investment based on these simple buy/sell rules.
  - Generate a performance summary including total return, max drawdown, and the number of trades executed.

**Deliverables for this step**:

- A Django view or API endpoint where users can input the backtesting parameters.
- Logic to fetch the stored historical data, apply the strategy, and return the backtest result.
- Test cases to validate the backtesting logic.

### 3. **Machine Learning Integration**

- Pre-Trained Model Integration

  :

  - You don’t need to build or train a new machine learning model from scratch. Instead, use a simple pre-trained machine learning model (such as a linear regression model) to predict future stock prices based on historical data.
  - The focus here is on integration, not ML development.
  - You can load the pre-trained model from a file (e.g., a `.pkl` file) and use it to generate predictions.

- Where to Integrate

  :

  - Implement a Django API endpoint that uses this pre-trained model to predict stock prices for the next 30 days based on the fetched historical data.
  - Predictions should be stored in the database alongside actual stock prices for comparison later.

**Deliverables for this step**:

- Django API endpoint that takes the stock symbol as input and returns the predicted stock prices for the next 30 days using the pre-trained model.
- Proper handling and storage of predictions alongside historical data.

### 4. **Report Generation**

- Output

  :

  - Generate a performance report after backtesting or after using the machine learning predictions.
  - The report should include the key financial metrics from the backtest and a visual comparison between the predicted and actual stock prices (use libraries like Matplotlib or Plotly for graphs).

- Report Formats

  :

  - The report should be available as downloadable PDFs and JSON responses via an API.

**Deliverables for this step**:

- A Django view or API endpoint that generates and returns the report.
- The report should include visualizations, key metrics, and predictions.

### 5. **Deployment**

- Deploy the Django project on AWS (or a cloud provider of your choice). The deployment should include:

  - Dockerized setup for the Django application.
  - Use of AWS RDS (PostgreSQL) for database storage.
  - CI/CD pipeline using GitHub Actions or another tool to automate deployment.
  - Proper handling of environment variables (use `.env` files or similar methods to ensure security).

- Write a detailed 

  ```
  README.md
  ```

   that includes:

  - How to set up the project locally (including any necessary API keys).
  - Instructions for running migrations and seeding data.
  - How to deploy to AWS or a similar cloud provider.

**Deliverables for this step**:

- Fully deployed application accessible via a public URL.
- Clear `README.md` with setup and deployment instructions.

------

### Evaluation Criteria:

1. API Integration

   :

   - Correct and efficient fetching of financial data using the specified API.
   - Proper handling of large datasets and API limits.

2. Backtesting Logic

   :

   - Robust implementation of the backtesting strategy, accurate calculation of returns and other performance metrics.
   - Code quality, clarity, and testability.

3. ML Integration

   :

   - Seamless integration of a pre-trained machine learning model for predictions.
   - Proper management of the model in Django, with clear separation of concerns (model logic vs Django views).

4. Reporting

   :

   - Clear, insightful reports with visualizations and key metrics.
   - Ability to handle both PDF generation and API responses.

5. Deployment

   :

   - Deployment should be production-ready, secure, and scalable.
   - Use of Docker and CI/CD tools to automate deployment processes.

6. Documentation

   :

   - Detailed `README.md` that clearly explains how to set up and deploy the project.
   - Documentation should be beginner-friendly for setup, but the task itself should only be solvable by advanced developers.

------

### Task is Suitable for Experienced Developers:

- The task touches on multiple areas: Django development, API integration, handling large datasets, and deployment, which ensures only highly skilled candidates will be able to solve it.
- The integration of a pre-trained ML model avoids the need for deep ML knowledge but tests a developer’s ability to handle more complex integrations and logic.
- The deployment requirement ensures the candidate is comfortable with production-grade setups, which only experienced developers can handle effectively.

This version focuses squarely on Django development but tests advanced skills in API handling, database management, backtesting logic, and real-world deployment challenges.

## ChatGPT solutions

Let's proceed with **Step 3: Machine Learning Integration** where we will integrate a pre-trained machine learning model to predict future stock prices and implement an API endpoint to handle predictions.

### Steps to Complete Step 3:

#### 1. **Pre-Trained Model Integration**:
   - **Goal**: Use a pre-trained machine learning model (like a linear regression model) to predict stock prices for the next 30 days based on historical data.
   - **Steps**:
     1. Save a pre-trained model to a `.pkl` file (if you haven't done this already).
     2. Load the pre-trained model in your Django view.
     3. Use the model to generate predictions.

#### 2. **Create the Django API Endpoint**:
   - **Goal**: Implement a Django API endpoint where users can input the stock symbol and get predictions for the next 30 days.
   - **Steps**:
     1. Create a new view to handle the prediction logic.
     2. Fetch historical data, preprocess it, and use it as input to the model for predictions.
     3. Return the predicted prices in the API response.

#### 3. **Store Predictions in the Database**:
   - **Goal**: Store the predicted stock prices in the database alongside historical data for comparison.
   - **Steps**:
     1. Define a model to store the predictions.
     2. Save the predictions after generating them.
     3. Add proper handling to compare predicted vs actual stock prices later.

---

### Step-by-Step Implementation:

#### Step 1: Pre-Trained Model Integration

1. **Save the Pre-Trained Model** (if not already done):
   If you have a pre-trained model (e.g., a linear regression model), save it using `joblib` or `pickle`. Here’s an example using `joblib`:

   ```python
   import joblib
   from sklearn.linear_model import LinearRegression
   
   # Train a simple model (assuming you've done this before)
   model = LinearRegression()
   model.fit(X_train, y_train)  # X_train and y_train should be your historical data
   
   # Save the trained model to a file
   joblib.dump(model, 'stock_model.pkl')
   ```

2. **Load the Pre-Trained Model in Django**:
   In your Django view, you can load the pre-trained model from the `.pkl` file:

   ```python
   import joblib
   
   # Load the pre-trained model
   model = joblib.load('path/to/stock_model.pkl')
   ```

#### Step 2: Create the Django API Endpoint

1. **Create the View in `views.py`**:
   Create a new Django view for generating predictions. This view will:
   
   - Accept the stock symbol as input.
   - Fetch the historical data from your database.
   - Preprocess the data to make it suitable for the model.
   - Use the loaded model to generate predictions for the next 30 days.
   
   Here’s how the view might look:
   
   ```python
   from django.http import JsonResponse
   from financials.models import StockData, StockPrediction
   import pandas as pd
   import joblib
   from datetime import datetime, timedelta
   
   # Load the pre-trained model once (to avoid loading it every time)
   model = joblib.load('path/to/stock_model.pkl')
   
   def predict_stock_prices(request, symbol='AAPL'):
       try:
           # Fetch the historical stock data for the symbol
           stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
           if not stock_data.exists():
               return JsonResponse({'error': 'No stock data available for this symbol'}, status=404)
   
           # Convert stock data to a DataFrame
           data = pd.DataFrame(list(stock_data.values('date', 'close_price')))
           data.set_index('date', inplace=True)
   
           # Preprocess data for the model (this depends on how your model expects input)
           # Here we assume the model expects a DataFrame of features
           X_input = data.tail(30)  # Example: Using the last 30 days as features for prediction
   
           # Make predictions for the next 30 days
           future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, 31)]
           predicted_prices = model.predict(X_input)
   
           # Store predictions in the database
           for date, price in zip(future_dates, predicted_prices):
               StockPrediction.objects.update_or_create(
                   symbol=symbol,
                   date=date,
                   defaults={'predicted_price': price}
               )
   
           # Return predictions as a JSON response
           predictions = [{'date': date.strftime('%Y-%m-%d'), 'predicted_price': price} for date, price in zip(future_dates, predicted_prices)]
           return JsonResponse({'predictions': predictions}, status=200)
   
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
   ```
   
2. **Add URL for the View**:
   In your `urls.py`, define a route for the prediction endpoint:

   ```python
   from django.urls import path
   from financials import views
   
   urlpatterns = [
       path('predict/<str:symbol>/', views.predict_stock_prices, name='predict_stock_prices'),
   ]
   ```

3. **Test the Endpoint**:
   Run the server and test the endpoint by hitting:

   ```
   http://127.0.0.1:8000/predict/AAPL/
   ```

#### Step 3: Store Predictions in the Database

1. **Define a Model for Storing Predictions**:
   In `models.py`, define a new model for storing the predicted stock prices:

   ```python
   from django.db import models
   
   class StockPrediction(models.Model):
       symbol = models.CharField(max_length=10)
       date = models.DateField()
       predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
       created_at = models.DateTimeField(auto_now_add=True)
   
       class Meta:
           unique_together = ('symbol', 'date')
           ordering = ['-date']
   
       def __str__(self):
           return f"{self.symbol} - {self.date} - {self.predicted_price}"
   ```

2. **Migrate the Model**:
   After adding the model, run the migrations to create the table in the database:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Save Predictions**:
   As shown in the view code above, predictions are saved in the `StockPrediction` model using `update_or_create` to ensure no duplicates are stored.

---

### Final Checklist for Step 3:

- [ ] **Pre-Trained Model**: Have you loaded a pre-trained machine learning model from a `.pkl` file?
- [ ] **API Endpoint**: Have you created an API endpoint where users can request stock price predictions for the next 30 days?
- [ ] **Store Predictions**: Are you storing the predicted stock prices in the `StockPrediction` model alongside historical data?

Once you've completed these steps, Step 3 will be fully implemented.

Let me know if you need further clarification or if there’s any part of this you want to dive deeper into!

To implement **Step 4: Report Generation**, you will need to generate a report that includes visual comparisons between predicted and actual stock prices, and allow users to download it in PDF format or get it as a JSON response via an API. Let’s break this step down into manageable tasks.

### Tasks for Step 4

1. **Generate a Performance Report**:
   - Use the key financial metrics from your backtesting results or machine learning predictions.
   - Include visualizations (e.g., line charts) comparing predicted stock prices vs actual stock prices.
   - Use **Matplotlib** or **Plotly** for creating charts.

2. **PDF and JSON Response**:
   - Allow users to download the report as a PDF.
   - Provide the report as a JSON response via an API.

---

### Step-by-Step Breakdown:

#### Step 1: Generate the Visualization

We will create a graph that compares predicted stock prices with actual stock prices. Using **Matplotlib** or **Plotly** will help generate the charts. Here’s an example of how to create a graph with Matplotlib:

##### Code Example (with Matplotlib):
```python
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from financials.models import StockPrediction, StockData

def generate_report(request, symbol='AAPL'):
    # Fetch actual stock prices and predicted prices
    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    # Convert to DataFrames
    actual_df = pd.DataFrame(list(actual_data.values('date', 'close_price')))
    predicted_df = pd.DataFrame(list(predicted_data.values('date', 'predicted_price')))

    # Create a line plot for actual vs predicted prices
    plt.figure(figsize=(10, 6))
    plt.plot(actual_df['date'], actual_df['close_price'], label='Actual Prices', color='blue')
    plt.plot(predicted_df['date'], predicted_df['predicted_price'], label='Predicted Prices', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Stock Prices for {symbol}: Actual vs Predicted')
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Send the plot as an image in the HTTP response
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={symbol}_stock_report.png'

    return response
```

#### Step 2: Generate a PDF Report

To generate the report in PDF format, you can use the **ReportLab** library. Here's how to generate a PDF containing the chart:

##### Code Example (with ReportLab):
1. **Install the necessary library**:
   ```bash
   pip install reportlab
   ```

2. **Create the PDF Generation Function**:
```python
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

def generate_pdf_report(request, symbol='AAPL'):
    # Create a PDF response object
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    
    # Set the title and add text
    pdf.setTitle(f'{symbol} Stock Report')
    pdf.drawString(100, 750, f'Stock Prices Report for {symbol}')

    # Fetch data from the database and plot the chart (using the Matplotlib plot as above)
    # After generating the chart, save it to an image file and then add it to the PDF

    # Add image (the chart) to the PDF
    pdf.drawImage('/path/to/saved/chart.png', 100, 500, width=400, height=300)

    # Add key metrics (example)
    pdf.drawString(100, 450, "Key Metrics:")
    pdf.drawString(100, 430, f"Total Return: {total_return:.2f}%")
    pdf.drawString(100, 410, f"Max Drawdown: {max_drawdown:.2f}%")
    pdf.drawString(100, 390, f"Number of Trades: {number_of_trades}")

    # Finalize and close the PDF document
    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    # Return the PDF as a downloadable file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={symbol}_stock_report.pdf'

    return response
```

#### Step 3: Return a JSON Response

If you want to provide the report as a JSON response, include the key metrics and predicted prices:

```python
import json
from django.http import JsonResponse

def report_json(request, symbol='AAPL'):
    # Fetch stock prices and predictions
    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    # Convert to dictionaries
    actual_prices = list(actual_data.values('date', 'close_price'))
    predicted_prices = list(predicted_data.values('date', 'predicted_price'))

    # Include key metrics (example: total return, drawdown)
    report = {
        'symbol': symbol,
        'actual_prices': actual_prices,
        'predicted_prices': predicted_prices,
        'metrics': {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'number_of_trades': number_of_trades
        }
    }

    return JsonResponse(report)
```

#### Step 4: Add URL Routes

Add routes in `urls.py` to generate the report in different formats (PDF, JSON, or image):

```python
from django.urls import path
from financials import views

urlpatterns = [
    path('report/<str:symbol>/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('report/<str:symbol>/json/', views.report_json, name='report_json'),
    path('report/<str:symbol>/image/', views.generate_report, name='generate_report'),
]
```

---

#### Step 5: Testing

1. **PDF Report**:
   Access the PDF report via:
   
   ```bash
   http://127.0.0.1:8000/report/AAPL/pdf/
   ```
   
2. **JSON Report**:
   Access the JSON report via:
   
   ```bash
   http://127.0.0.1:8000/report/AAPL/json/
   ```
   
3. **Image Report**:
   Access the image chart via:
   
   ```bash
   http://127.0.0.1:8000/report/AAPL/image/
   ```

---

Let me know how this goes! Once you generate the reports and confirm that they work as expected, we can move on to **Step 5: Deployment**.

To complete **Step 5: Deployment**, you will need to Dockerize your Django application, configure AWS for hosting your database (using RDS for PostgreSQL), and set up CI/CD for automated deployment. I'll walk you through each step.

### Steps for Deployment:

#### 1. **Dockerizing Your Django Application**

You’ll first need to create a `Dockerfile` and a `docker-compose.yml` file to run your Django app in a containerized environment.

##### **Dockerfile**:
Create a `Dockerfile` in the root directory of your project.

```Dockerfile
# Base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Expose the port that Django will run on
EXPOSE 8000

# Set environment variables (for production use .env files)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

##### **docker-compose.yml**:
Create a `docker-compose.yml` file to run Django and PostgreSQL together.

```yaml
version: '3'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: blockhouse_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123456
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DEBUG: 'True'
      DATABASE_URL: postgres://postgres:123456@db:5432/blockhouse_db

volumes:
  postgres_data:
```

##### **.env File**:
Create a `.env` file to securely store your environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://postgres:123456@db:5432/blockhouse_db
```

##### Build and Run Docker:

Run the following commands to build and run the Docker containers:
```bash
docker-compose build
docker-compose up
```

#### 2. **Set up AWS RDS for PostgreSQL**

1. **Create an RDS Instance**:
   - Go to the AWS RDS Console and create a PostgreSQL instance.
   - Configure your security group to allow access to the instance on port 5432 from your server’s IP.

2. **Modify Your Django `settings.py`**:
   Update your database settings to use the RDS instance:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blockhouse_db',
        'USER': 'your_rds_username',
        'PASSWORD': 'your_rds_password',
        'HOST': 'your_rds_endpoint',
        'PORT': '5432',
    }
}
```

#### 3. **Set Up CI/CD Pipeline with GitHub Actions**

Create a `.github/workflows/deploy.yml` file to automate deployment with GitHub Actions:

```yaml
name: Django CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        ports:
          - 5432:5432
        env:
          POSTGRES_DB: blockhouse_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: 123456

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run migrations
      run: python manage.py migrate
    - name: Run tests
      run: python manage.py test
```

This pipeline will:
- Install dependencies.
- Run migrations and tests on every push to the `main` branch.

#### 4. **Deploying to AWS**

1. **EC2 Setup**:
   - Create an EC2 instance and configure security groups to allow SSH and HTTP traffic.
   - Install Docker on your EC2 instance and pull the Docker image from your repository.

2. **Pull Docker Image**:
   - Push your Docker image to a registry (e.g., Docker Hub or AWS ECR).
   - SSH into your EC2 instance, pull the image, and run it.

3. **Run the Application**:
   Run Docker on EC2:

```bash
docker run -d -p 8000:8000 your-docker-image
```

#### 5. **Create `README.md`**

Create a `README.md` that includes instructions for:
- **Setting up the project locally**:
  - Installation of dependencies, setting up environment variables, running migrations, and starting the server.
- **Seeding data**:
  Provide information on how to fetch the data using the API keys and store it in the database.
- **Deploying to AWS**:
  Provide step-by-step instructions on how to deploy the project to AWS, including EC2 and RDS setup.

### Example `README.md`:

```markdown
# Blockhouse Django Project

## Setup Locally

1. Clone the repository.
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following variables:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgres://postgres:123456@localhost:5432/blockhouse_db
   ```
5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Fetching Data
1. Use the `fetch_financial_data` endpoint to fetch stock data:
   ```
   /fetch/AAPL/
   ```

## Deployment Instructions

### Dockerized Setup
1. Build and run Docker:
   ```bash
   docker-compose build
   docker-compose up
   ```

### AWS Deployment
1. Set up an EC2 instance and RDS.
2. Run the Docker container on EC2.
```

---

This will give you a fully dockerized, AWS-hosted application with a CI/CD pipeline for automated deployments. Let me know if you need more details on any specific step!