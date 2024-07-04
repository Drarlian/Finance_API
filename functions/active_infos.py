import yfinance as yf
import pandas as pd

# PETR4.SA: Period '36mo' is invalid, must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y',
# 'ytd', 'max']


def get_infos(ticker: str):
    ticker: str = f"{ticker}.SA"  # Código do fundo imobiliário
    chamada = yf.Ticker(ticker).history(period='1y')

    fundo = yf.Ticker(ticker)

    # Obter informações detalhadas:
    info = fundo.info

    # max_value = f"Valor máximo no último ano: R${max(chamada['High'].values):.2f}"
    max_value_12m: str = f"R${max(chamada['High'].values):.2f}"

    # min_value = f"Valor minímo no último ano: R${min(chamada['Low'].values):.2f}"
    min_value_12m: str = f"R${min(chamada['Low'].values):.2f}"

    # type = f'Tipo de fundo: {info["industryKey"]}'
    type_active: str = str(info["industryKey"])

    # ---------------------------------------------------------------------------------------------------

    # Verificar e exibir Informações Relevantes:
    if 'currentPrice' in info:
        # current_price = f"Cotação: {info['currentPrice']}"
        current_price: str = f"R${info['currentPrice']}"
    else:
        current_price: str = "Cotação não disponível."

    # ---------------------------------------------------------------------------------------------------

    if 'priceToBook' in info:
        # p_vp: str = f"P/VP: {info['priceToBook']:.2f}"
        p_vp: str = f"{info['priceToBook']:.2f}"
    else:
        p_vp: str = "P/VP não disponível."

    # ---------------------------------------------------------------------------------------------------

    # Obter histórico de preços dos últimos 12 meses:
    hist = fundo.history(period="1y")

    # Calcular a variação percentual dos últimos 12 meses
    if not hist.empty:
        variation_value = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100
        # variacao_12m: str = f"Variação dos últimos 12 meses: {variation_value:.2f}%"
        variacao_12m: str = f"{variation_value:.2f}%"
    else:
        variacao_12m: str = "Histórico de preços não disponível."

    # ---------------------------------------------------------------------------------------------------

    # Calcular a média de liquidez diária dos últimos 30 dias: (Não está retornando o valor correto)
    hist_30d = fundo.history(period="1mo")
    if not hist_30d.empty:
        media_liquidez_30d: str = hist_30d['Volume'].mean()
        # media_liquidez_30d: str = f"Média de liquidez diária dos últimos 30 dias: {media_liquidez:.2f} ????????"
        media_liquidez_30d: str = f"{media_liquidez_30d:.2f}"
    else:
        media_liquidez_30d: str = "Histórico de liquidez não disponível."

    # ---------------------------------------------------------------------------------------------------

    # Obter histórico de preços dos últimos 12 meses
    new_hist = fundo.history(period="1y")
    # Obter histórico de dividendos dos últimos 12 meses:
    dividends = fundo.dividends
    if not dividends.empty:
        # Converter as datas para o mesmo fuso horário
        now = pd.Timestamp.now(tz=dividends.index.tz)
        one_year_ago = now - pd.DateOffset(years=1)

        dividends_last_12m = dividends[dividends.index > one_year_ago]
        total_dividends = dividends_last_12m.sum()
        # Dividend yield = total_dividends / currentPrice
        new_current_price = new_hist['Close'].iloc[-1] if not new_hist.empty else None
        if new_current_price:
            dividend_yield_12m: str = f'{((total_dividends / new_current_price) * 100):.2f}%'
            # print(f"Dividend Yield dos últimos 12 meses: {dividend_yield_12m:.2f}%")
        else:
            dividend_yield_12m: str = "Cotação atual não disponível para calcular o dividend yield."
    else:
        dividend_yield_12m: str = "Histórico de dividendos não disponível."

    return {"current_price": current_price, "max_value_12m": max_value_12m, "min_value_12m": min_value_12m,
            "type_active": type_active, "p_vp": p_vp, "variacao_12m": variacao_12m,
            "media_liquidez_30d": media_liquidez_30d, "dividend_yield_12m": dividend_yield_12m}


if __name__ == "__main__":
    print(get_infos('PETR4'))
