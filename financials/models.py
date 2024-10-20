from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)  # Stock symbol (e.g., AAPL)
    date = models.DateField()  # Date of the stock data
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()  # Volume of trades

    class Meta:
        unique_together = ['symbol', 'date']  # Prevent duplicate entries
        ordering = ['-date']  # Most recent data first

    def __str__(self):
        return f'{self.symbol} - {self.date}'

class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('symbol', 'date')  # Ensures no duplicate predictions for the same date and symbol
        ordering = ['-date']  # Orders by the most recent predictions

    def __str__(self):
        return f"{self.symbol} - {self.date} - {self.predicted_price}"