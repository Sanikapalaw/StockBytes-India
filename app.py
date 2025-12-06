import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from textblob import TextBlob
import email.utils

# --- 1. APP CONFIGURATION ---
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

# --- 2. NEWS ENGINE ---
@st.cache_data(ttl=600)
def fetch_news(company_name, time_period_days):
    """
    Fetch limited (10) relevant news articles.
    """
    # 1. Set Time Parameter for Google
    if time_period_days == 365:
        time_param = "when:1y"
    elif time_period_days == 180:
        time_param = "when:6m"
    else:
        time_param = "when:30d"

    # 2. Search Query (Strict Financial Focus)
    query = f'{company_name} share price target buy sell results {time_param}'
    query = query.replace(" ", "+")
    
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')

        articles = []
        cutoff_date = datetime.now() - timedelta(days=time_period_days)

        for item in items:
            title = item.title.text.strip()
            source = item.source.text if item.source else "Google News"
            summary = item.description.text if item.description else ""
            summary_clean = BeautifulSoup(summary, "html.parser").get_text()
            link = item.link.text
            
            # Date Parsing
            published_str = item.pubDate.text if item.pubDate else None
            is_recent = False
            
            if published_str:
                try:
                    pub_date = email.utils.parsedate_to_datetime(published_str).replace(tzinfo=None)
                    if pub_date >= cutoff_date:
                        is_recent = True
                except:
                    is_recent = True 

            if is_recent:
                # Basic Sentiment
                blob = TextBlob(summary_clean)
                sentiment_score = blob.sentiment.polarity

                articles.append({
                    "title": title,
                    "source": source,
                    "link": link,
                    "summary": summary_clean.strip(),
                    "published": published_str,
                    "sentiment": sentiment_score
                })

            # LIMIT: STRICTLY 10 ARTICLES MAX
            if len(articles) >= 10: 
                break

        return articles

    except Exception as e:
        st.error(f"Error: {e}")
        return []

# --- 3. UI LAYOUT ---
st.title("StockBytes India ⚡🇮🇳")
st.caption("Quick, relevant news headlines for Indian Stocks.")

# Sidebar
st.sidebar.header("Controls")
time_options = {"Last 1 Month": 30, "Last 6 Months": 180, "Last 1 Year": 365}
selected_time_label = st.sidebar.selectbox("History:", list(time_options.keys()), index=2)
selected_days = time_options[selected_time_label]

search_query = st.sidebar.text_input("Find Stock:")
filtered_stocks = {k: v for k, v in STOCKS.items() if search_query.lower() in k.lower() or search_query.lower() in v.lower()}
selected_ticker = st.sidebar.selectbox("Select Stock:", options=["--- Select ---"] + list(filtered_stocks.keys()))

# Main Area
if selected_ticker != "--- Select ---":
    company_name = STOCKS[selected_ticker]
    is_valid_ticker = ".NS" in selected_ticker or ".BO" in selected_ticker

    # 1. Minimalist Header (Price + Name)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📰 {company_name}")
    with col2:
        # Just a tiny price check - no charts
        if is_valid_ticker:
            try:
                stock_data = yf.download(selected_ticker, period="1d", progress=False)
                if not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    if isinstance(current_price, pd.Series): current_price = current_price.iloc[0]
                    st.metric("Live Price", f"₹{current_price:.2f}")
            except:
                st.write("")

    st.markdown("---")

    # 2. The News List
    news_articles = fetch_news(company_name, selected_days)

    if news_articles:
        for article in news_articles:
            # Simple Emoji for Sentiment
            score = article['sentiment']
            if score > 0.05: emoji = "🟢"
            elif score < -0.05: emoji = "🔴"
            else: emoji = "⚪"

            with st.expander(f"{emoji} {article['source']} | {article['title']}"):
                st.write(article['summary'])
                st.caption(f"📅 {article['published']} | Sentiment: {score:.2f}")
                st.markdown(f"[🔗 Read Source]({article['link']})")
        
        # Download
        st.markdown("---")
        df = pd.DataFrame(news_articles)
        st.download_button("📥 Save Headlines (CSV)", data=df.to_csv(index=False), file_name=f"{company_name}_headlines.csv")
        
    else:
        st.info(f"No recent news found for {company_name} in the last {selected_days} days.")

else:
    st.info("👈 Select a stock from the sidebar to fetch news.")
