from unittest import TestCase
from unittest.mock import Mock

from tinkoff.invest.schemas import InstrumentIdType

from helper import get_figi_by_ticker, get_future_detail


class TestHelper(TestCase):
    def test_get_future_detail(self):
        figi_id = "XXXTEST1FIGI"
        expected_response = "FutureResponseMock"
        mock_attrs = {"instruments.future_by.return_value": Mock(instrument=expected_response)}
        services = Mock(**mock_attrs)
        future = get_future_detail(services=services, figi_id=figi_id)
        services.instruments.future_by.assert_called_once_with(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=figi_id,
        )
        self.assertEqual(future, expected_response)

    # При повторных вызовах функции get_future_detail не должно быть запросов во внешнее API
    def test_get_future_detail_cache(self):
        figi_id1 = "YYYTEST2FIGI"
        figi_id2 = "ZZZTEST2FIGI"
        services = Mock()
        for __iter in range(3):
            get_future_detail(services=services, figi_id=figi_id1)
            services.instruments.future_by.assert_called_once()
        get_future_detail(services=services, figi_id=figi_id2)
        get_future_detail(services=services, figi_id=figi_id1)
        self.assertEqual(services.instruments.future_by.call_count, 2)

    def test_get_figi_by_ticker_instrument(self):
        ticker = "UTST"
        ticker_other = "YTST"
        figi_id = "XXXTEST3FIGI"
        figi_id_other = "XXXTEST3FIGI"
        instrument_list = [
            Mock(ticker=ticker_other, figi=figi_id_other),
            Mock(ticker=ticker, figi=figi_id),
        ]
        mock_attrs = {
            "instruments.find_instrument.return_value": Mock(instruments=instrument_list),
        }
        services = Mock(**mock_attrs)
        result_figi = get_figi_by_ticker(services, ticker)
        services.instruments.find_instrument.assert_called_once_with(query=ticker.casefold())
        self.assertEqual(figi_id, result_figi)

    def test_get_figi_by_ticker_currency(self):
        ticker = "X4TST"
        ticker_other = "Z4TST"
        figi_id = "XXXTEST4FIGI"
        figi_id_other = "XXXTEST4FIGI"
        instruments_list = [
            Mock(ticker=ticker_other, figi=figi_id_other),
        ]
        currencies_list = [
            Mock(ticker=ticker_other, figi=figi_id_other),
            Mock(ticker=ticker, figi=figi_id),
        ]
        mock_attrs = {
            "instruments.find_instrument.return_value": Mock(instruments=instruments_list),
            "instruments.currencies.return_value": Mock(instruments=currencies_list)
        }
        services = Mock(**mock_attrs)
        result_figi = get_figi_by_ticker(services, ticker)
        services.instruments.currencies.assert_called_once_with()
        self.assertEqual(figi_id, result_figi)

    # При повторных вызовах функции figi_by_ticker не должно быть запросов во внешнее API
    def test_get_figi_by_ticker_cache(self):
        ticker1, figi_id1 = "ATST", "XXXTEST5FIGI"
        ticker2, figi_id2 = "BTST", "XXXTEST5FIGI"
        instrument_list = [
            Mock(ticker=ticker1, figi=figi_id1),
            Mock(ticker=ticker2, figi=figi_id2),
        ]
        mock_attrs = {
            "instruments.find_instrument.return_value": Mock(instruments=instrument_list),
        }
        services = Mock(**mock_attrs)
        for __iter in range(3):
            result_figi = get_figi_by_ticker(services, ticker1)
            self.assertEqual(figi_id1, result_figi)
        for __iter in range(3):
            result_figi = get_figi_by_ticker(services, ticker2)
            self.assertEqual(figi_id2, result_figi)
        result_figi = get_figi_by_ticker(services, ticker1)
        self.assertEqual(figi_id1, result_figi)
        self.assertEqual(services.instruments.find_instrument.call_count, 2)
