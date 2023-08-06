import telebot
import pandas_datareader as pdr
import os
import yfinance as yf


class StockPriceBot:
    """A bot that can be used to get stock prices and set price alerts."""

    def __init__(self, bot_token):
        """Initializes the bot with the given token."""
        self.bot = telebot.TeleBot(bot_token)
        self.reminders = {}

    def get_price(self, ticker):
        """Gets the current price of the given stock."""
        data = yf.download(tickers=ticker, period='1d', interval='1d')
        if data.empty:
            raise ValueError(f"No data available for {ticker}.")
        else:
            return data["Adj Close"].iloc[-1]

    def set_reminder(self, user_id, ticker, upper_limit, lower_limit):
        """Sets a price alert for the given user and stock.

        Args:
            user_id: The ID of the user.
            ticker: The symbol of the stock.
            upper_limit: The upper limit of the price alert.
            lower_limit: The lower limit of the price alert.

        Raises:
            ValueError: If the user or stock does not exist.
        """
        if user_id not in self.reminders:
            self.reminders[user_id] = {}
        self.reminders[user_id][ticker] = {"upper_limit": upper_limit, "lower_limit": lower_limit}

    def remove_reminder(self, user_id, ticker):
        """Removes a price alert for the given user and stock.

        Args:
            user_id: The ID of the user.
            ticker: The symbol of the stock.

        Raises:
            ValueError: If the user or stock does not exist.
        """
        if user_id not in self.reminders:
            raise ValueError(f"No price alert was found for {ticker}.")
        del self.reminders[user_id][ticker]

    def list_reminders(self, user_id):
        """Lists all active price alerts for the given user.

        Args:
            user_id: The ID of the user.

        Raises:
            ValueError: If the user does not exist.
        """
        if user_id not in self.reminders:
            return []
        else:
            return self.reminders[user_id]

    def run(self):
        """Starts the bot."""
        self.bot.polling()


if __name__ == "__main__":
    # Get the bot token from the environment variable.
    bot_token = os.environ["BOT_TOKEN"]

    # Create a new bot instance.
    bot = StockPriceBot(bot_token)

    # Start the bot.
    bot.run()
