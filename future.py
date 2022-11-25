"""
Generate code:

for ins in services.instruments.futures().instruments:
    if ins.ticker.endswith(FUTURE_TIME):
        name = re.sub(r"[^A-Z]+", "_", ins.basic_asset.upper()).strip("_")
        print(f"{name} = \"{ins.ticker[:-2]}\" # {ins.name.split('-')[1][6:]}")
"""
from enum import Enum


class Future(Enum):
    ALRS = "AL"  # Алроса
    MTSS = "MT"  # МТС
    AUD_USD = "AU"  # Курс Австралийский доллар
    GMKN = "GK"  # Норильский никель
    MTLR = "MC"  # Мечел
    SILVER = "SV"  # Серебро
    RTKM = "RT"  # Ростелеком
    AFKS = "AK"  # АФК Система
    MOEX = "ME"  # Московская биржа
    MOEXOG = "OG"  # Индекс Нефти и газа
    SBER = "SR"  # Сбер Банк (обыкновенные)
    VTBR = "VB"  # ВТБ
    NLMK = "NM"  # НЛМК
    GBP_USD = "GU"  # Курс Фунт стерлингов
    GOLD = "GD"  # Золото
    CHMF = "CH"  # Северсталь
    MGNT = "MN"  # Магнит
    NL = "Nl"  # Никель
    ROSN = "RN"  # Роснефть
    IMOEX_MINI = "MM"  # Индекс МосБиржи (мини)
    LKOH = "LK"  # Лукойл
    INVESCO_QQQ_ETF_TRUST_UNIT_SERIES = "NA"  # Nasdaq 100
    MOEXCN = "CS"  # Индекс Потребительского сектора
    RUAL = "RL"  # РУСАЛ
    RTSI = "RI"  # Индекс РТС
    CO = "Co"  # Медь
    IMOEX = "MX"  # Индекс МосБиржи
    YNDX = "YN"  # Яндекс
    DSKY = "DY"  # Детский мир
    PHOR = "PH"  # ФосАгро
    RSTI = "RE"  # Российские сети
    SNGSP = "SG"  # Сургутнефтегаз (привилегированные)
    FIVE = "FV"  # X5 RetailGroup
    IRAO = "IR"  # Интер РАО ЕЭС
    POLY = "PO"  # Polymetal
    PLT = "PT"  # Платина
    PALLADIUM = "PD"  # Палладий
    USD_CAD = "CA"  # Курс Доллар США
    TATN = "TT"  # Татнефть
    AFLT = "AF"  # Аэрофлот
    EUR_RUB__TOM = "Eu"  # Курс евро
    MREDC = "HO"  # Индекс московской недвижимости
    SPDR_S_P_ETF_TRUST = "SF"  # S&P 500
    MOEXFN = "FN"  # Индекс Финансов
    NVTK = "NK"  # Новатэк
    FEES = "FS"  # ФСК ЕЭС
    SBERP = "SP"  # Сбер Банк (привилегированные)
    EUR_USD = "ED"  # Курс евро
    TRNFP = "TN"  # Транснефть (привилегированные)
    USD000UTSTOM = "Si"  # Курс доллар
    SMLT = "SS"  # ГК Самолет
    MAGN = "MG"  # ММК
    SIBN = "SO"  # Газпром нефть
    OZON = "OZ"  # Озон
    SNGS = "SN"  # Сургутнефтегаз (обыкновенные)
    CNY_RUB = "CR"  # Курс Юань
    WHCPT = "W4"  # Индекс Пшеницы
    BRENT = "BR"  # Нефть Brent
    NG = "NG"  # Природный газ
    POSI = "PS"  # Positive Technologies
    RTSI_MINI = "RM"  # Индекс РТС (мини)
    VKCO = "ML"  # VK
    GAZP = "GZ"  # Газпром
    PIKK = "PI"  # ПИК
    HYDR = "HY"  # РусГидро
    RGBI = "RB"  # Индекс Государственных облигаций
    MOEXMM = "MA"  # Индекс Металлов и добычи
    PLZL = "PZ"  # Полюс Золото
