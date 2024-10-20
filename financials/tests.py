from django.test import TestCase
from financials.views import run_backtest
import pandas as pd

class BacktestTestCase(TestCase):
    def setUp(self):
        # Set up some sample stock data
        data = {
            'date': pd.date_range(start='2023-01-01', periods=300),
            'close_price': [100 + i * 0.1 for i in range(300)]
        }
        self.df = pd.DataFrame(data)
        self.df['50_MA'] = self.df['close_price'].rolling(window=50).mean()
        self.df['200_MA'] = self.df['close_price'].rolling(window=200).mean()

    def test_backtest_strategy(self):
        # Run the backtest
        result = run_backtest(self.df, 10000, 50, 200)

        # Assert that the total return is calculated correctly
        self.assertIn('total_return', result)
        self.assertGreaterEqual(result['total_return'], 0)

        # Assert that number of trades is correct
        self.assertGreaterEqual(result['number_of_trades'], 0)
