from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from financials.models import StockData, StockPrediction
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import joblib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

API_KEY = 'HSRNNVU7KA77QYXA'  # Replace with your Alpha Vantage API key

# Fetch financial data
def fetch_financial_data(request, symbol='AAPL'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full'
    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    data = response.json().get('Time Series (Daily)', {})
    for date_str, daily_data in data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        StockData.objects.update_or_create(
            symbol=symbol,
            date=date,
            defaults={
                'open_price': daily_data['1. open'],
                'close_price': daily_data['4. close'],
                'high_price': daily_data['2. high'],
                'low_price': daily_data['3. low'],
                'volume': daily_data['5. volume'],
            }
        )

    return JsonResponse({'message': 'Successfully fetched and stored stock data'}, status=200)

# Backtest logic
def run_backtest(data, initial_investment, buy_ma, sell_ma):
    cash = initial_investment
    shares = 0
    number_of_trades = 0
    max_drawdown = 0
    peak_value = initial_investment
    total_value = initial_investment

    for i in range(sell_ma, len(data)):
        price = float(data['close_price'].iloc[i])
        ma_50 = data['50_MA'].iloc[i]
        ma_200 = data['200_MA'].iloc[i]

        if price < ma_50 and shares == 0:
            shares = cash // price
            cash -= shares * price
            number_of_trades += 1

        elif price > ma_200 and shares > 0:
            cash += shares * price
            shares = 0
            number_of_trades += 1

        total_value = cash + (shares * price)
        peak_value = max(peak_value, total_value)
        drawdown = (peak_value - total_value) / peak_value
        max_drawdown = max(max_drawdown, drawdown)

    final_value = cash + (shares * float(data['close_price'].iloc[-1]))
    total_return = (final_value - initial_investment) / initial_investment * 100

    return {
        'initial_investment': initial_investment,
        'final_value': final_value,
        'total_return': total_return,
        'number_of_trades': number_of_trades,
        'max_drawdown': max_drawdown * 100
    }

# Backtest strategy endpoint
def backtest_strategy(request, symbol='AAPL'):
    try:
        initial_investment = float(request.GET.get('initial_investment', 10000))
        buy_moving_average = int(request.GET.get('buy_moving_average', 50))
        sell_moving_average = int(request.GET.get('sell_moving_average', 200))

        stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
        if not stock_data.exists():
            return JsonResponse({'error': 'No stock data available for this symbol'}, status=404)

        data = pd.DataFrame(list(stock_data.values('date', 'close_price')))
        data.set_index('date', inplace=True)
        data['50_MA'] = data['close_price'].rolling(window=buy_moving_average).mean()
        data['200_MA'] = data['close_price'].rolling(window=sell_moving_average).mean()

        result = run_backtest(data, initial_investment, buy_moving_average, sell_moving_average)
        return JsonResponse(result, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Load pre-trained model
model_path = 'stock_model.pkl'
model = joblib.load(model_path)

# Stock price prediction
def predict_stock_prices(request, symbol='AAPL'):
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    if not stock_data.exists():
        return JsonResponse({'error': 'No stock data available for this symbol'}, status=404)

    df = pd.DataFrame(list(stock_data.values('date', 'close_price')))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['day'] = range(len(df))
    X_input = df[['day']]

    future_days = 30
    last_day = df.index[-1]
    future_dates = [last_day + timedelta(days=i) for i in range(1, future_days + 1)]

    predicted_prices = model.predict(X_input.tail(30))
    for date, price in zip(future_dates, predicted_prices):
        StockPrediction.objects.update_or_create(symbol=symbol, date=date, defaults={'predicted_price': price})

    predictions = [{'date': date.strftime('%Y-%m-%d'), 'predicted_price': price} for date, price in zip(future_dates, predicted_prices)]
    return JsonResponse({'predictions': predictions}, status=200)

# Generate chart as PNG image
def generate_report(request, symbol='AAPL'):
    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    actual_df = pd.DataFrame(list(actual_data.values('date', 'close_price')))
    predicted_df = pd.DataFrame(list(predicted_data.values('date', 'predicted_price')))

    plt.figure(figsize=(10, 6))
    plt.plot(actual_df['date'], actual_df['close_price'], label='Actual Prices', color='blue')
    plt.plot(predicted_df['date'], predicted_df['predicted_price'], label='Predicted Prices', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Stock Prices for {symbol}: Actual vs Predicted')
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={symbol}_stock_report.png'
    return response

# Generate report as PDF
def generate_pdf_report(request, symbol='AAPL'):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setTitle(f'{symbol} Stock Report')
    pdf.drawString(100, 750, f'Stock Prices Report for {symbol}')

    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    actual_df = pd.DataFrame(list(actual_data.values('date', 'close_price')))
    predicted_df = pd.DataFrame(list(predicted_data.values('date', 'predicted_price')))

    # Generate chart dynamically for PDF
    plt.figure(figsize=(10, 6))
    plt.plot(actual_df['date'], actual_df['close_price'], label='Actual Prices', color='blue')
    plt.plot(predicted_df['date'], predicted_df['predicted_price'], label='Predicted Prices', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Stock Prices for {symbol}: Actual vs Predicted')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    pdf.drawImage(ImageReader(img_buffer), 50, 400, width=500, height=300)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={symbol}_stock_report.pdf'
    return response

# Report as JSON
def report_json(request, symbol='AAPL'):
    actual_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    actual_prices = list(actual_data.values('date', 'close_price'))
    predicted_prices = list(predicted_data.values('date', 'predicted_price'))

    # Example: Include total return, drawdown, and number of trades
    total_return = 10  # Placeholder for actual value
    max_drawdown = 5  # Placeholder for actual value
    number_of_trades = 15  # Placeholder for actual value

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
