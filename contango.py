import yaml
from tinkoff.invest import Client

from future import Future
from helper import get_contango, get_figi_by_ticker, get_future_detail

with open("config.yaml") as config:
    config_from_file = yaml.load(config, Loader=yaml.FullLoader)
TOKEN = config_from_file["token"]
FUTURE_TIME = config_from_file.get("future", "M3")  # H M U Z + Year[:-1]

# Встречные сделки на поставочных фьючерсах
# Возможность забрать контанго (фьючерс стоит дороже базового актив)
# * Забирать бэквордацию - опасно по причине возможного появления дивидендов
with Client(TOKEN) as services:
    future_current_tickers = {prefix.name: prefix.value + FUTURE_TIME for prefix in Future}
    contango_profit = {}
    for ticker, future in future_current_tickers.items():
        try:
            future_detail = get_future_detail(
                services=services, figi_id=get_figi_by_ticker(services=services, ticker=future)
            )
        except KeyError:
            continue
        if future_detail.futures_type == "DELIVERY_TYPE_PHYSICAL_DELIVERY":
            try:
                contango = get_contango(services=services, ticker=ticker, future_ticker=future)
            except RuntimeError:
                continue
            if contango > 0:
                contango_profit[ticker] = contango

    print("Contango:")
    for ticker, contango in sorted(
            contango_profit.items(),
            key=lambda item: item[1], reverse=True)[:5]:
        print(f"\tTicker: {ticker} - {round(contango * 100, ndigits=5)}%")
