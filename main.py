import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('S&P500上位株価可視化アプリ')

st.sidebar.write("""
# S&P500上位株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 30)

st.write(f"""
### 過去 **{days}日間** の株価
""")

#キャッシュに情報取得
@st.cache

#df にyfで情報取得する関数
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

tickers2 = [
    'AAPL',
    'META',
    'GOOGL',
    'MSFT',
    'AMZN',
    'V',
    'JPM',
    'JNJ',
    'WMT',
    'MA',
    'PG',
    'BAC',
    'INTC',
    'T',
    'UNH',
    'XOM',
    'HD',
    'DIS',
    'KO'
]

for w in tickers2 :
    tkr = yf.Ticker(w)
    if tkr == '':
        st.error (w , "というティッカーシンボルで情報が取得出来ません")

try: 
    tickers = {
    'apple': 'AAPL',
    'facebook': 'META',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'amazon': 'AMZN',
    'Visa':'V',
    'JPMorgan Chase':'JPM',
    'Johnson & Johnson':'JNJ',
    'Walmart':'WMT',
    'Mastercard':'MA',
    'Procter & Gamble':'PG',
    'Bank of America':'BAC',
    'Intel':'INTC',
    'AT&T':'T',
    'UnitedHealth Group':'UNH',
    'ExxonMobil':'XOM',
    'The Home Depot':'HD',
    'The Walt Disney Company':'DIS',
    'The Coca-Cola Company':'KO'
}

    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 2000.0, (0.0, 2000.0)
    )

    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 
        'amazon', 
        'facebook', 
        'apple',
        'Visa',
        'JPMorgan Chase',
        'Johnson & Johnson',
        'Walmart',
        'Mastercard',
        'Procter & Gamble',
        'Bank of America',
        'Intel',
        'AT&T',
        'UnitedHealth Group',
        'ExxonMobil',
        'The Home Depot',
        'The Walt Disney Company',
        'The Coca-Cola Company']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
         "なにかエラーが起きているようです。"
    )