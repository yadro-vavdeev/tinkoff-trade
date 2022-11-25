from decimal import Decimal

from tinkoff.invest.schemas import InstrumentIdType
from tinkoff.invest.services import Services
from tinkoff.invest.utils import quotation_to_decimal


def get_future_detail(services: Services, figi_id: str):
    try:
        return get_future_detail.cache[figi_id]
    except AttributeError:
        get_future_detail.cache = {}
        return get_future_detail(**dict(locals().items()))
    except KeyError:
        get_future_detail.cache[figi_id] = services.instruments.future_by(
            id=figi_id,
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI
        ).instrument
        return get_future_detail.cache[figi_id]


def get_figi_by_ticker(services: Services, ticker: str) -> str:
    ticker = ticker.casefold()
    try:
        return get_figi_by_ticker.cache[ticker]
    except AttributeError:
        get_figi_by_ticker.cache = {}
        return get_figi_by_ticker(**dict(locals().items()))
    except KeyError:
        for instrument in services.instruments.find_instrument(query=ticker).instruments:
            if instrument.ticker.casefold() == ticker:
                get_figi_by_ticker.cache[ticker] = instrument.figi
                return instrument.figi
        for instrument in services.instruments.currencies().instruments:
            if instrument.ticker.casefold() == ticker:
                get_figi_by_ticker.cache[ticker] = instrument.figi
                return instrument.figi
        raise KeyError(f"Ticker '{ticker}' not found")


def get_contango(services: Services, ticker: str, future_ticker: str) -> Decimal:
    ticker_figi = get_figi_by_ticker(services, ticker)
    future_ticker_figi = get_figi_by_ticker(services, future_ticker)

    # максимальная цена по которой возможно продать фьючерс (шорт)
    future_price = quotation_to_decimal(services.market_data.get_order_book(
        figi=future_ticker_figi,
        depth=1,
    ).bids[0].price)

    # минимальная цена по которой возможно купить акции
    base_asks = services.market_data.get_order_book(
        figi=ticker_figi,
        depth=50,
    ).asks
    base_price = 0
    basic_asset_size_in_future = quotation_to_decimal(
        get_future_detail(services, future_ticker_figi).basic_asset_size
    )
    for ask in base_asks:
        max_buy = min(ask.quantity, basic_asset_size_in_future)
        base_price += max_buy * quotation_to_decimal(ask.price)
        basic_asset_size_in_future -= max_buy
        if not basic_asset_size_in_future:
            break
    else:
        raise RuntimeError("Low liquidity")

    return (future_price - base_price) / base_price
