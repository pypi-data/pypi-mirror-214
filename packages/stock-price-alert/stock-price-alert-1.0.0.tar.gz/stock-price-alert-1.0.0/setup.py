from setuptools import setup, find_packages

setup(
    name='stock-price-alert',
    version='1.0.0',
    author='piritheevi',
    author_email='gkappdeveloper@gmail.com',
    description='Stock Price Bot - Python library for stock price information and alerts',
    long_description=open('reademe.txt').read(),
    url='https://github.com/your_username/stock_price_bot',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas',
        'pandas-datareader',
        'telebot',
        'yfinance',
    ],
)

