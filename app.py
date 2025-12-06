import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from textblob import TextBlob
import email.utils

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="StockBytes India", page_icon="⚡", layout="centered")

# Your Stock List
STOCKS = dict(sorted({
    "ABB.NS": "ABB India",
    "ABBOTT.NS": "Abbott India",
    "AAVAS.NS": "AAVAS Financiers",
    "ADANIESOL.NS": "Adani Energy Solutions",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIGREEN.NS": "Adani Green",
    "ADANIPOWER.NS": "Adani Power",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ADANITOTAL.NS": "Adani Total Gas",
    "ADITYABIRLA.NS": "Aditya Birla Capital",
    "AB_REAL_ESTATE": "A B Real Estate",
    "AFCONS_INFRASTR": "Afcons Infrastr.",
    "AHERA.NS": "Ahera Industries",
    "ALEMBICLTD.NS": "Alembic Pharma",
    "ALKEM.NS": "Alkem Laboratories",
    "ALLIED_BLENDERS": "Allied Blenders",
    "AMARA_RAJA_ENER": "Amara Raja Ener.",
    "ANGELONE.NS": "Angel One",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "APOLLO.MED": "Apollo Medicals",
    "ASHOKLEY.NS": "Ashok Leyland",
    "ASAHI_INDIA_GLAS": "Asahi India Glas",
    "ASIANPAINT.NS": "Asian Paints",
    "ATHER_ENERGY": "Ather Energy",
    "AUROBINDO.NS": "Aurobindo Pharma",
    "AVENUESUPER.NS": "Avenue Supermarts",
    "AXISBANK.NS": "Axis Bank",
    "BATAINDIA.NS": "Bata India",
    "BANKBARODA.NS": "Bank of Baroda",
    "BAYERCROP.NS": "Bayer Crop Sci.",
    "BELRISE_INDUSTRI": "Belrise Industri",
    "BEML.NS": "BEML Ltd",
    "BERGERPAINT.NS": "Berger Paints",
    "BHARTIARTL.NS": "Bharti Airtel",
    "BHARTIHEX.NS": "Bharti Hexacom",
    "BHEL.NS": "BHEL",
    "BLS_INTERNAT": "BLS Internat.",
    "BLUEDART.NS": "Blue Dart Expres",
    "BOSCHLTD.NS": "Bosch",
    "BPCL.NS": "Bharat Petroleum Corporation Ltd",
    "BRITANNIA.NS": "Britannia Industries",
    "BROOKFIELD_INDIA": "Brookfield India",
    "CAMS_SERVICES": "Cams Services",
    "CAPLIN_POINT_LAB": "Caplin Point Lab",
    "CAPRI_GLOBAL": "Capri Global",
    "CARBORUNDUM_UNI": "Carborundum Uni.",
    "CASTROLIND.NS": "Castrol India",
    "CENTURY_PLYBOARD": "Century Plyboard",
    "CESC.NS": "CESC",
    "CHAMBLFERT.NS": "Chambal Fert.",
    "CHOICE_INTL": "Choice Intl.",
    "CHOLAFIN.NS": "Cholamandalam Investment & Finance",
    "CIE_AUTOMOTIVE": "CIE Automotive",
    "CIPLA.NS": "Cipla",
    "CLEAN_SCIENCE": "Clean Science",
    "COALINDIA.NS": "Coal India",
    "COLPAL.NS": "Colgate-Palmolive",
    "CONCORD_BIOTECH": "Concord Biotech",
    "COROMANDEL.NS": "Coromandel International",
    "CROMPTON_GR_CON": "Crompton Gr. Con",
    "CUBE_HIGHWAYS": "Cube Highways",
    "CUMMINSIND.NS": "Cummins India",
    "DABUR.NS": "Dabur India",
    "DEEPAKFERT.NS": "Deepak Fertilis.",
    "DEEPAKNTR.NS": "Deepak Nitrite",
    "DEVYANI.NS": "Devyani Intl.",
    "DLF.NS": "DLF Ltd",
    "DIVISLAB.NS": "Divi's Laboratories",
    "DRREDDY.NS": "Dr Reddy's Laboratories",
    "EID_PARRY": "EID Parry",
    "EICHERMOT.NS": "Eicher Motors",
    "EIH": "EIH",
    "ELGI_EQUIPMENTS": "Elgi Equipments",
    "EMBASSY_DEVELOP": "Embassy Develop",
    "ETERNAL.NS": "Eternal Ltd",
    "FSN.NS": "FSN E-Commerce (Nykaa)",
    "FORCE_MOTORS": "Force Motors",
    "FORTIS.NS": "Fortis Healthcare",
    "GAIL.NS": "GAIL (India)",
    "GABRIEL_INDIA": "Gabriel India",
    "GALLANTT_ISPAT_L": "Gallantt Ispat L",
    "GENINSUR.NS": "Gen Insur",
    "GODAWARI_POWER": "Godawari Power",
    "GODREJ_AGROVET": "Godrej Agrovet",
    "GODREJCP.NS": "Godrej Consumer Products",
    "GODREJPROP.NS": "Godrej Properties",
    "GRANULES.NS": "Granules India",
    "GMRINFRA.NS": "GMR Airports",
    "HAVELLS.NS": "Havells India",
    "HCLTECH.NS": "HCL Technologies",
    "HDFCBANK.NS": "HDFC Bank",
    "HDFCLIFE.NS": "HDFC Life Insurance",
    "HDFCAMC.NS": "HDFC Asset Management",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "HINDALCO.NS": "Hindalco Industries",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "HINDZINC.NS": "Hindustan Zinc",
    "HITACHIENERGY.NS": "Hitachi Energy",
    "HPCL.NS": "Hindustan Petroleum",
    "HYUNDAI.NS": "Hyundai Motor India",
    "ICICIBANK.NS": "ICICI Bank",
    "ICICILOMBARD.NS": "ICICI Lombard",
    "ICICIPRULI.NS": "ICICI Prudential Life",
    "IDBI.NS": "IDBI Bank",
    "IFCI": "IFCI",
    "INDHOTEL.NS": "Indian Hotels Company",
    "INDIANB.NS": "Indian Bank",
    "INDIGO.NS": "InterGlobe Aviation",
    "INDEGENE": "Indegene",
    "INFY.NS": "Infosys",
    "IOB.NS": "Indian Overseas Bank",
    "IOC.NS": "Indian Oil Corporation",
    "IRFC.NS": "IRFC",
    "JSWENERGY.NS": "JSW Energy",
    "JSWINFRA.NS": "JSW Infrastructure",
    "JSWSTEEL.NS": "JSW Steel",
    "JINDALSTAIN.NS": "Jindal Stainless",
    "JINDALSTEL.NS": "Jindal Steel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "LUPIN.NS": "Lupin",
    "MAZDOCK.NS": "Mazagon Dock",
    "M&M.NS": "Mahindra & Mahindra",
    "MANKIND.NS": "Mankind Pharma",
    "MARICO.NS": "Marico",
    "MARUTI.NS": "Maruti Suzuki",
    "MAXHEALTH.NS": "Max Healthcare",
    "MRF.NS": "MRF Ltd",
    "MUTHOOTFIN.NS": "Muthoot Finance",
    "NMDC.NS": "NMDC Ltd",
    "NTPC.NS": "NTPC Limited",
    "NTPCGREEN.NS": "NTPC Green Energy",
    "NESTLEIND.NS": "Nestle India",
    "OIL.NS": "Oil India",
    "ONGC.NS": "Oil & Natural Gas Corporation",
    "ONE97.NS": "One 97 Communications (Paytm)",
    "PBFINTECH.NS": "PB Fintech (PolicyBazaar)",
    "PERSISTENT.NS": "Persistent Systems",
    "PIDILITIND.NS": "Pidilite Industries",
    "POWERFIN.NS": "Power Finance Corporation",
    "POWERGRID.NS": "Power Grid Corporation",
    "PRESTIGE.NS": "Prestige Estates",
    "RAILVIKAS.NS": "Rail Vikas Nigam",
    "RELIANCE.NS": "Reliance Industries",
    "RECLTD.NS": "REC Ltd",
    "SAMVARDHAN.NS": "Samvardhana Motherson",
    "SHREECEM.NS": "Shree Cement",
    "SHRIRAMFIN.NS": "Shriram Finance",
    "SBIN.NS": "State Bank of India",
    "SBILIFE.NS": "SBI Life Insurance",
    "SBICARD.NS": "SBI Cards",
    "SUNPHARMA.NS": "Sun Pharma Industries",
    "SUZLON.NS": "Suzlon Energy",
    "SWIGGY.NS": "Swiggy",
    "TATASTEEL.NS": "Tata Steel",
    "TATAPOWER.NS": "Tata Power Company",
    "TATAMOTORS.NS": "Tata Motors",
    "TCS.NS": "Tata Consultancy Services",
    "TECHM.NS": "Tech Mahindra",
    "TITAN.NS": "Titan Company",
    "TORNTPWR.NS": "Torn Power",
    "TORNTPHARM.NS": "Torrent Pharmaceuticals",
    "TUBEINV.NS": "Tube Investments",
    "TVSMOTOR.NS": "TVS Motor Company",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "UNIONBANK.NS": "Union Bank of India",
    "UNOMINDA.NS": "Uno Minda",
    "VARUNBEV.NS": "Varun Beverages",
    "VEDANTA.NS": "Vedanta",
    "VODAFONEIDEA.NS": "Vodafone Idea",
    "WAAREE.NS": "Waaree Energies",
    "WIPRO.NS": "Wipro",
    "ZYDUSLIFE.NS": "Zydus Lifesciences",
}.items(), key=lambda x: x[0].upper()))

# --- 2. SOURCE 1: GOOGLE NEWS FETCHER ---
def fetch_google_news(company_name):
    """Fetch 10 articles from Google RSS"""
    query = f'{company_name} share price target buy sell results when:1y'
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    
    articles = []
    try:
        response = requests.get(rss_url, timeout=5)
        soup = BeautifulSoup(response.content, features="xml")
        for item in soup.findAll('item')[:10]: # Limit to 10
            # Parse Date
            try:
                pub_date_str = item.pubDate.text
                # Convert to datetime object for sorting
                pub_date_dt = email.utils.parsedate_to_datetime(pub_date_str).replace(tzinfo=None)
            except:
                pub_date_dt = datetime.now()

            articles.append({
                "source_type": "Google",
                "title": item.title.text.strip(),
                "source": item.source.text if item.source else "Google News",
                "link": item.link.text,
                "summary": BeautifulSoup(item.description.text, "html.parser").get_text(),
                "published_dt": pub_date_dt, # For sorting
                "published_str": pub_date_dt.strftime('%d %b %Y') # For display
            })
    except Exception:
        pass
    return articles

# --- 3. SOURCE 2: YAHOO FINANCE FETCHER ---
def fetch_yahoo_news(ticker_symbol):
    """Fetch latest news from Yahoo Finance API"""
    articles = []
    # If the ticker isn't valid (no .NS), skip
    if ".NS" not in ticker_symbol and ".BO" not in ticker_symbol:
        return []

    try:
        stock = yf.Ticker(ticker_symbol)
        yahoo_news = stock.news
        
        for item in yahoo_news:
            # Parse Date (Yahoo gives Unix timestamp)
            timestamp = item.get('providerPublishTime', 0)
            pub_date_dt = datetime.fromtimestamp(timestamp)
            
            # Yahoo images often clutter, so we skip them and just take text
            title = item.get('title', '')
            link = item.get('link', '')
            publisher = item.get('publisher', 'Yahoo Finance')
            
            articles.append({
                "source_type": "Yahoo",
                "title": title,
                "source": f"Yahoo ({publisher})",
                "link": link,
                "summary": title, # Yahoo API often puts the summary in the title or separate
                "published_dt": pub_date_dt,
                "published_str": pub_date_dt.strftime('%d %b %Y')
            })
    except Exception:
        pass
    return articles

# --- 4. MERGE & SENTIMENT ENGINE ---
@st.cache_data(ttl=600)
def get_combined_news(ticker, company_name):
    # 1. Get from both sources
    g_news = fetch_google_news(company_name)
    y_news = fetch_yahoo_news(ticker)
    
    # 2. Combine
    all_news = g_news + y_news
    
    # 3. Sort by Date (Newest First)
    all_news.sort(key=lambda x: x['published_dt'], reverse=True)
    
    # 4. Remove Duplicates (Simple check by Title)
    seen_titles = set()
    unique_news = []
    for article in all_news:
        if article['title'] not in seen_titles:
            seen_titles.add(article['title'])
            
            # 5. Add Sentiment
            blob = TextBlob(article['summary'])
            article['sentiment'] = blob.sentiment.polarity
            unique_news.append(article)
            
    return unique_news[:15] # Return top 15 combined

# --- 5. UI LAYOUT ---
st.title("StockBytes India ⚡🇮🇳")
st.caption("Aggregated News from Google & Yahoo Finance")

# Sidebar
st.sidebar.header("Controls")
search_query = st.sidebar.text_input("Search Stock:")
filtered_stocks = {k: v for k, v in STOCKS.items() if search_query.lower() in k.lower() or search_query.lower() in v.lower()}
selected_ticker = st.sidebar.selectbox("Select Stock:", options=["--- Select ---"] + list(filtered_stocks.keys()))

if selected_ticker != "--- Select ---":
    company_name = STOCKS[selected_ticker]
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📰 {company_name}")
    with col2:
        try:
            # Minimal Price Check
            if ".NS" in selected_ticker:
                data = yf.download(selected_ticker, period="1d", progress=False)
                if not data.empty:
                    price = data['Close'].iloc[-1]
                    if isinstance(price, pd.Series): price = price.iloc[0]
                    st.metric("Live Price", f"₹{price:.2f}")
        except:
            pass
            
    st.markdown("---")

    # Fetch Data
    with st.spinner("Fetching news from Google & Yahoo..."):
        news_list = get_combined_news(selected_ticker, company_name)

    if news_list:
        for article in news_list:
            # Sentiment Logic
            s = article['sentiment']
            if s > 0.05: emoji = "🟢"
            elif s < -0.05: emoji = "🔴"
            else: emoji = "⚪"
            
            # Badge for Source
            source_badge = "G" if article['source_type'] == "Google" else "Y"
            badge_color = "blue" if source_badge == "G" else "purple"

            with st.expander(f"{emoji} [{source_badge}] {article['title']}"):
                st.caption(f"Source: {article['source']} | Date: {article['published_str']}")
                st.write(article['summary'])
                st.markdown(f"[🔗 Read Full Article]({article['link']})")
        
        # Download
        st.markdown("---")
        df = pd.DataFrame(news_list)
        # Drop the datetime object before saving to CSV (it looks messy)
        if not df.empty:
            df = df.drop(columns=['published_dt'])
        st.download_button("📥 Save News (CSV)", data=df.to_csv(index=False), file_name=f"{company_name}_news.csv")
    else:
        st.info("No recent news found.")
else:
    st.info("👈 Select a stock to view aggregated news.")
