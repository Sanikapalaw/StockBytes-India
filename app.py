import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import yfinance as yf
from textblob import TextBlob
import email.utils

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="StockBytes Pro", page_icon="⚡", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# --- 2. DATA: STOCKS & SECTOR MAPPING ---
SECTORS = {
    "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS"],
    "Auto": ["TATAMOTORS.NS", "MARUTI.NS", "M&M.NS", "ASHOKLEY.NS", "HEROMOTOCO.NS"],
    "Energy": ["RELIANCE.NS", "ADANIENT.NS", "NTPC.NS", "POWERGRID.NS", "ONGC.NS"],
    "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
    "Consumer": ["ITC.NS", "HINDUNILVR.NS", "TITAN.NS", "NESTLEIND.NS"]
}

STOCKS = {
    "ABB.NS": "ABB India", "ABBOTT.NS": "Abbott India", "AAVAS.NS": "AAVAS Financiers",
    "ADANIESOL.NS": "Adani Energy", "ADANIENT.NS": "Adani Enterprises", "ADANIGREEN.NS": "Adani Green",
    "ADANIPOWER.NS": "Adani Power", "ADANIPORTS.NS": "Adani Ports", "ADANITOTAL.NS": "Adani Total Gas",
    "ADITYABIRLA.NS": "Aditya Birla Cap", "AB_REAL_ESTATE": "AB Real Estate",
    "AMARA_RAJA_ENER": "Amara Raja", "ANGELONE.NS": "Angel One", "APOLLOHOSP.NS": "Apollo Hosp",
    "ASHOKLEY.NS": "Ashok Leyland", "ASIANPAINT.NS": "Asian Paints", "ATHER_ENERGY": "Ather Energy",
    "AUROBINDO.NS": "Aurobindo Pharma", "AVENUESUPER.NS": "DMart", "AXISBANK.NS": "Axis Bank",
    "BAJFINANCE.NS": "Bajaj Finance", "BAJAJFINSV.NS": "Bajaj Finserv",
    "BANKBARODA.NS": "Bank of Baroda", "BATAINDIA.NS": "Bata India", "BEL.NS": "Bharat Electronics",
    "BERGERPAINT.NS": "Berger Paints", "BHARTIARTL.NS": "Bharti Airtel", "BHEL.NS": "BHEL",
    "BPCL.NS": "BPCL", "BRITANNIA.NS": "Britannia", "CIPLA.NS": "Cipla", "COALINDIA.NS": "Coal India",
    "COLPAL.NS": "Colgate", "DABUR.NS": "Dabur", "DIVISLAB.NS": "Divis Lab", "DLF.NS": "DLF",
    "DRREDDY.NS": "Dr Reddy", "EICHERMOT.NS": "Eicher Motors", "GAIL.NS": "GAIL",
    "GODREJCP.NS": "Godrej CP", "GRASIM.NS": "Grasim", "HCLTECH.NS": "HCL Tech",
    "HDFCBANK.NS": "HDFC Bank", "HDFCLIFE.NS": "HDFC Life", "HEROMOTOCO.NS": "Hero MotoCorp",
    "HINDALCO.NS": "Hindalco", "HINDUNILVR.NS": "HUL", "ICICIBANK.NS": "ICICI Bank",
    "ITC.NS": "ITC Ltd", "IOC.NS": "Indian Oil", "INDUSINDBK.NS": "IndusInd Bank",
    "INFY.NS": "Infosys", "JSWSTEEL.NS": "JSW Steel", "KOTAKBANK.NS": "Kotak Bank",
    "LT.NS": "Larsen & Toubro", "M&M.NS": "M&M", "MARUTI.NS": "Maruti Suzuki",
    "NESTLEIND.NS": "Nestle", "NTPC.NS": "NTPC", "ONGC.NS": "ONGC", "POWERGRID.NS": "Power Grid",
    "RELIANCE.NS": "Reliance Ind", "SBIN.NS": "SBI", "SBILIFE.NS": "SBI Life",
    "SUNPHARMA.NS": "Sun Pharma", "TATAMOTORS.NS": "Tata Motors", "TATASTEEL.NS": "Tata Steel",
    "TCS.NS": "TCS", "TECHM.NS": "Tech Mahindra", "TITAN.NS": "Titan",
    "ULTRACEMCO.NS": "UltraTech", "UPL.NS": "UPL", "WIPRO.NS": "Wipro", "ZOMATO.NS": "Zomato"
}
STOCKS = dict(sorted(STOCKS.items(), key=lambda x: x[1]))

def get_peers(current_ticker):
    for sector, tickers in SECTORS.items():
        if current_ticker in tickers:
            return [t for t in tickers if t != current_ticker][:4] 
    return []

# --- 3. DUAL NEWS FETCHING ---

def fetch_google_news(company_name):
    """Source 1: Google RSS"""
    query = f'{company_name} share price target buy sell results when:1y'
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    articles = []
    try:
        response = requests.get(rss_url, timeout=5)
        soup = BeautifulSoup(response.content, features="xml")
        for item in soup.findAll('item')[:10]:
            try: pub_date_dt = email.utils.parsedate_to_datetime(item.pubDate.text).replace(tzinfo=None)
            except: pub_date_dt = datetime.now()
            articles.append({
                "source_type": "Google", "title": item.title.text.strip(),
                "source": item.source.text if item.source else "Google News",
                "link": item.link.text, "summary": BeautifulSoup(item.description.text, "html.parser").get_text(),
                "published_dt": pub_date_dt, "published_str": pub_date_dt.strftime('%d %b %Y')
            })
    except: pass
    return articles

def fetch_yahoo_news(ticker_symbol):
    """Source 2: Yahoo Finance"""
    if ".NS" not in ticker_symbol and ".BO" not in ticker_symbol: return []
    articles = []
    try:
        stock = yf.Ticker(ticker_symbol)
        for item in stock.news:
            pub_date_dt = datetime.fromtimestamp(item.get('providerPublishTime', 0))
            articles.append({
                "source_type": "Yahoo", "title": item.get('title', ''),
                "source": f"Yahoo ({item.get('publisher', '')})",
                "link": item.get('link', ''), "summary": item.get('title', ''),
                "published_dt": pub_date_dt, "published_str": pub_date_dt.strftime('%d %b %Y')
            })
    except: pass
    return articles

@st.cache_data(ttl=600)
def get_combined_news(ticker, company_name):
    # Fetch from both
    g_news = fetch_google_news(company_name)
    y_news = fetch_yahoo_news(ticker)
    
    # Merge
    all_news = g_news + y_news
    all_news.sort(key=lambda x: x['published_dt'], reverse=True)
    
    # Remove Duplicates
    seen, unique = set(), []
    for art in all_news:
        if art['title'] not in seen:
            seen.add(art['title'])
            # Add Sentiment
            blob = TextBlob(art['summary'])
            art['sentiment'] = blob.sentiment.polarity
            unique.append(art)
    return unique[:20]

# --- 4. SIDEBAR UI ---
st.sidebar.header("❤️ Watchlist")
if st.session_state.watchlist:
    for saved in st.session_state.watchlist:
        if st.sidebar.button(f"{STOCKS.get(saved, saved)}", key=f"fav_{saved}"):
            st.session_state.selected_ticker = saved
            st.rerun()
    if st.sidebar.button("Clear All"):
        st.session_state.watchlist = []
        st.rerun()
else:
    st.sidebar.caption("No favorites yet.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Search")
search = st.sidebar.text_input("Type stock name:")
filtered = {k: v for k, v in STOCKS.items() if search.lower() in k.lower() or search.lower() in v.lower()}

index = 0
if 'selected_ticker' in st.session_state and st.session_state.selected_ticker in filtered:
    index = list(filtered.keys()).index(st.session_state.selected_ticker) + 1

selected_ticker = st.sidebar.selectbox("Select Stock:", ["--- Select ---"] + list(filtered.keys()), index=index)
if selected_ticker != "--- Select ---":
    st.session_state.selected_ticker = selected_ticker

# --- 5. MAIN DASHBOARD ---
st.title("StockBytes Pro ⚡🇮🇳")

if selected_ticker != "--- Select ---":
    company_name = STOCKS[selected_ticker]
    
    # Header Area
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.subheader(f"{company_name}")
    
    with c2:
        if selected_ticker in st.session_state.watchlist:
            if st.button("💔 Unwatch"): st.session_state.watchlist.remove(selected_ticker); st.rerun()
        else:
            if st.button("❤️ Watch"): st.session_state.watchlist.append(selected_ticker); st.rerun()

    # Live Price Check
    if ".NS" in selected_ticker:
        try:
            data = yf.download(selected_ticker, period="1d", progress=False)
            if not data.empty:
                price = data['Close'].iloc[-1]
                if isinstance(price, pd.Series): price = price.iloc[0]
                c3.metric("Live Price", f"₹{price:.2f}")
        except: pass
    
    # Quick Compare Buttons
    peers = get_peers(selected_ticker)
    if peers:
        st.markdown("##### ⚡ Quick Compare:")
        cols = st.columns(len(peers))
        for idx, peer_ticker in enumerate(peers):
            peer_name = STOCKS.get(peer_ticker, peer_ticker)
            if cols[idx].button(peer_name, key=f"peer_{peer_ticker}"):
                st.session_state.selected_ticker = peer_ticker
                st.rerun()
    
    st.markdown("---")

    # MAIN CONTENT: Just the News List
    with st.spinner("Scanning Google & Yahoo Finance..."):
        news_list = get_combined_news(selected_ticker, company_name)

    if news_list:
        st.subheader(f"Latest News ({len(news_list)} Articles)")
        st.caption("Aggregated from Google News & Yahoo Finance")
        
        for article in news_list:
            s = article['sentiment']
            # Determine Color/Emoji
            if s > 0.05:
                emoji = "🟢"
            elif s < -0.05:
                emoji = "🔴"
            else:
                emoji = "⚪"
            
            # Source Badge
            source_badge = "Google" if article['source_type'] == "Google" else "Yahoo"
            
            with st.expander(f"{emoji} [{source_badge}] {article['title']}"):
                st.caption(f"{article['published_str']} | {article['source']}")
                st.write(article['summary'])
                st.markdown(f"[🔗 Read Full Article]({article['link']})")
        
        # Download Button
        df = pd.DataFrame(news_list).drop(columns=['published_dt']) if news_list else pd.DataFrame()
        st.download_button("📥 Download News CSV", df.to_csv(index=False), f"{company_name}.csv")
    else:
        st.info("No recent news found from Google or Yahoo.")
else:
    st.info("👈 Select a stock to start.")
