import requests
from django.http import JsonResponse
from financials.models import StockData
from datetime import datetime
import time

API_KEY = 'HSRNNVU7KA77QYXA'  # Replace with your Alpha Vantage API key

def fetch_financial_data(request, symbol='AAPL'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full'

    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break  # Success, exit the loop
            elif response.status_code == 429:  # Rate limit error
                retries += 1
                time.sleep(60)  # Wait 60 seconds before retrying
            else:
                return JsonResponse({'error': f'Error {response.status_code}: Failed to fetch data'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            retries += 1
            time.sleep(10)  # Wait 10 seconds before retrying
            if retries == max_retries:
                return JsonResponse({'error': f'Failed to fetch data after {max_retries} retries: {str(e)}'}, status=500)

    if retries == max_retries:
        return JsonResponse({'error': 'Failed to fetch data after multiple attempts'}, status=500)

    data = response.json().get('Time Series (Daily)', {})

    # Store the data in the database
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