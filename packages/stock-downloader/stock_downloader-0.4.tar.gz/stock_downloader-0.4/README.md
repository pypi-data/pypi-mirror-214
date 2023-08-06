# stock_downloader Package

The stock_downloader package provides functionality to download and save stock market data using the Yahoo Finance API.


## Installation

You can install the package using pip:

pip install stock_downloader


## Usage

The package includes the following files:

- `__init__.py`: An empty file that marks the `stock_csv` directory as a Python package.
- `downloader.py`: Contains functions to download and save stock market data.

To use the package, you can import the necessary functions from `stock_downloader.stock_csv.downloader`:

```
    from stock_csv.downloader import run_iterations

    ticker = 'BHP.AX'
    num_iterations = 10

    run_iterations(ticker, num_iterations)
```


## Project Structure

The stock_downloader package has the following structure:

```
    stock_downloader/
    ├── stock_csv/
    │   ├── __init__.py
    │   └── downloader.py
    ├── setup.py
    ├── README.md
    └── LICENSE
```


## Development and Contribution

- Source Code: [GitHub Repository](https://github.com/AdamSierakowski/stock_downloader)
- Issue Tracker: [GitHub Issues](https://github.com/AdamSierakowski/stock_downloader/issues)


## License

This project is licensed under Creative Commons Attribution-NonCommercial 4.0 International Public License - see the LICENSE file for details.
