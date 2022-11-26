from unittest import TestCase
from unittest.mock import Mock, patch

from tinkoff.invest.schemas import Quotation

from helper import get_contango


class TestHelperContango(TestCase):
    @patch("helper.get_figi_by_ticker")
    @patch("helper.get_future_detail")
    def test_get_contango(self, get_future_detail_mock, get_figi_by_ticker_mock):
        get_figi_by_ticker_mock.side_effect = ["XXX", "YYY"]
        future_ticker = "KIZ1"
        ticker = "KISS"
        future_bids = [Mock(price=Quotation(units=1397, nano=0))]
        get_future_detail_mock.return_value = Mock(basic_asset_size=Quotation(units=100, nano=0))
        base_asks = [
            Mock(price=Quotation(units=8, nano=0), quantity=3),
            Mock(price=Quotation(units=9, nano=0), quantity=9),
            Mock(price=Quotation(units=14, nano=0), quantity=100),
            Mock(price=Quotation(units=1000, nano=0), quantity=1000),
        ]  # 3 * 8 + 9 * 9 + 88 * 14 = 1337
        mock_attrs = {
            "market_data.get_order_book.return_value": Mock(bids=future_bids, asks=base_asks)
        }
        services = Mock(**mock_attrs)
        contango = get_contango(services, ticker, future_ticker)
        self.assertEqual((1397 - 1337) / 1337, float(contango))
        self.assertEqual(services.market_data.get_order_book.call_count, 2)

    @patch("helper.get_figi_by_ticker")
    @patch("helper.get_future_detail")
    def test_get_contango_negative(self, get_future_detail_mock, get_figi_by_ticker_mock):
        get_figi_by_ticker_mock.side_effect = ["XXX", "YYY"]
        future_ticker = "KIM3"
        ticker = "CHUN"
        future_bids = [Mock(price=Quotation(units=1337, nano=0))]
        get_future_detail_mock.return_value = Mock(basic_asset_size=Quotation(units=100, nano=0))
        base_asks = [
            Mock(price=Quotation(units=8, nano=0), quantity=9),
            Mock(price=Quotation(units=9, nano=0), quantity=10),
            Mock(price=Quotation(units=133, nano=0), quantity=80),
        ]
        mock_attrs = {
            "market_data.get_order_book.return_value": Mock(bids=future_bids, asks=base_asks)
        }
        services = Mock(**mock_attrs)
        with self.assertRaises(RuntimeError) as exc_msg:
            get_contango(services, ticker, future_ticker)
        self.assertEqual("Low liquidity", str(exc_msg.exception))
