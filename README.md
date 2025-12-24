# 📈 StockBytes Pro ⚡

**StockBytes Pro** is an interactive financial dashboard built using **Python and Streamlit** that tracks **Indian stocks** by combining **live prices, financial news, and NLP-based sentiment analysis**. The goal of the project is to help users understand not just *what* the news says, but *how the market feels* about a stock.

---

## 🚀 Features

* 📊 **Live Stock Prices** for selected Indian stocks
* 📰 **Latest News Aggregation** from trusted sources like:

  * Economic Times
  * Business Standard
  * Livemint
* 🔗 **Clickable Headlines** that open the original article in a new tab
* 🤖 **NLP-Based Sentiment Analysis** on each news article
* 🔴 Visual indicators to highlight **risk / negative / alert-type news**
* 📁 **Download News Data as CSV** for further analysis
* ⚡ **Quick Compare** feature to instantly switch between peer stocks

---

## 🧠 Sentiment Analysis Logic

Each news article is processed using Natural Language Processing (NLP) to generate a **numerical sentiment score**.

* Positive sentiment → optimistic market tone
* Neutral sentiment → informational or mixed tone
* Negative / alert sentiment → risk, volatility, or negative market reaction

🔴 **Important Note:**
Red indicators do **not** mean the company is bad. They highlight **short-term market risk or negative sentiment**, even when company fundamentals may be strong.

This design choice helps users quickly focus on **market mood rather than just headlines**.

---

## 📂 CSV Export

Users can download the analyzed news data as a CSV file. Each file contains:

* Source
* Article Link
* Summary
* Sentiment Score
* Published Date

This makes it easy to open the data in **Excel**, **Google Sheets**, or use it for further modeling.

---

## ⚡ Quick Compare Feature

The **Quick Compare** menu allows instant switching between related stocks without navigating the sidebar.

Example peer comparisons:

* Reliance Industries
* Adani Enterprises
* NTPC
* Power Grid
* ONGC

This enables faster context switching and comparison.

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NLP / Sentiment Analysis
* Financial News Aggregation

---

## 🇮🇳 Use Case

StockBytes Pro is designed specifically for the **Indian stock market** and is useful for:

* Retail investors
* Finance students
* Data science learners
* Market researchers
* Portfolio & project showcases

---

## 💡 Key Learnings

* Building end-to-end data products
* Applying NLP to real-world financial news
* Designing dashboards focused on decision-making
* Understanding the difference between **fundamental strength** and **market sentiment**

---

## 🔗 Links

* **Live App:** <add-your-app-link-here>
* **GitHub Repository:** <add-your-github-link-here>

---

## 📌 Disclaimer

This project is for **educational and analytical purposes only** and should not be considered financial or investment advice.

---

⭐ If you find this project interesting, feel free to star the repository and share feedback!
