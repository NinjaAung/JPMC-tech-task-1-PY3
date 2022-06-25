import unittest

import pytest
from client3 import getDataPoint, getRatio

test_quotes = [  # must be paired
    {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
     'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
    {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
     'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'},
    {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
     'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
    {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
     'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'},
]

test_quotes_paired = []
temp = []

for quote in test_quotes:
    temp.append(quote)
    if len(temp) >= 2:
        test_quotes_paired.append(temp)
        temp = []


@pytest.mark.parametrize("paired_quotes", test_quotes_paired)
class TestCaseClient:

    def test_getDataPoint_calculatePrice(self, paired_quotes):
        for quote in paired_quotes:
            top_ask = quote['top_ask']
            top_bid = quote['top_bid']
            assert getDataPoint(quote) == (
                quote["stock"], top_bid["price"], top_ask["price"],  top_bid["price"] + top_ask["price"]/2)

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self, paired_quotes):
        for quote in paired_quotes:
            top_ask = quote['top_ask']
            top_bid = quote['top_bid']
            _, bid_price, ask_price, _ = getDataPoint(quote)
            assert (bid_price > ask_price) == (
                top_bid['price'] > top_ask['price'])

    def test_getRatio_calculateRatio(self, paired_quotes):
        _, _, _, price_a = getDataPoint(paired_quotes[0])
        _, _, _, price_b = getDataPoint(paired_quotes[1])
        assert getRatio(price_a, price_b) == price_a / price_b


if __name__ == '__main__':
    unittest.main()
