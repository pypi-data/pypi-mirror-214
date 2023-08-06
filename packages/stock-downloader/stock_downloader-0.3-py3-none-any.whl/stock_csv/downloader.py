import yfinance as yf
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the default logging level
logger.addHandler(logging.FileHandler('log.txt'))


def download_data(ticker, enable_logging=False):
    """
    Download stock market data for a given ticker.

    Args:
        ticker (str): Ticker symbol of the stock to download data for.
        enable_logging (bool, optional): Enable logging. Defaults to False.

    Returns:
        pandas.DataFrame: DataFrame containing the downloaded stock data.
    """
    if enable_logging:
        logger.info(f"Downloading data for {ticker}...")
    try:
        data = yf.download(
            tickers=ticker,
            interval='1d',
            period='2y',
            auto_adjust=False
        )
        if enable_logging:
            logger.info(f"Data downloaded successfully for {ticker}")
        return data
    except Exception as e:
        if enable_logging:
            logger.error(f"Error downloading data for {ticker}: {str(e)}")
        return None


def save_data(ticker, data, enable_logging=False):
    """
    Save stock market data to a CSV file.

    Args:
        ticker (str): Ticker symbol of the stock.
        data (pandas.DataFrame): DataFrame containing the stock data.
        enable_logging (bool, optional): Enable logging. Defaults to False.
    """
    if data is not None:
        folder_path = 'data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f'{folder_path}/price-history-{ticker}.csv'
        data.to_csv(file_path, header=True)
        if enable_logging:
            logger.info(f"Data saved for {ticker} at {file_path}")


def run_iterations(ticker, num_iterations, enable_logging=False):
    """
    Run multiple iterations of downloading and saving stock market data.

    Args:
        ticker (str): Ticker symbol of the stock.
        num_iterations (int): Number of iterations to perform.
        enable_logging (bool, optional): Enable logging. Defaults to False.
    """
    for _ in range(num_iterations):
        stock_data = download_data(ticker, enable_logging=enable_logging)
        save_data(ticker, stock_data, enable_logging=enable_logging)
