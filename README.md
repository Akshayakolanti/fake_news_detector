# VeriFact AI - Fake News Detector & Real News Finder

An AI-powered web application that detects fake news articles, calculates real vs. fake credibility percentage scores, highlights deceptive clickbait patterns, and cross-references verified real news articles.

---

## 📁 Project Structure

```
fake_news_detect(project)/
├── app.py                  # Flask Web Server & REST API
├── model_trainer.py        # ML Dataset Builder & Model Training Script
├── predictor.py            # Credibility Analysis & Scoring Engine
├── news_finder.py          # Google News RSS Real News Recommender
├── scraper.py              # URL Web Content Scraper
├── model.pkl               # Saved ML Classifier Artifact
├── log_reg.pkl             # Saved Logistic Regression Probabilities
├── vectorizer.pkl          # Saved TF-IDF Feature Extraction Model
├── requirements.txt        # Python Dependencies List
├── templates/
│   └── index.html          # Glassmorphic Web Dashboard Interface
└── static/
    ├── css/
    │   └── style.css       # Dark Theme Glassmorphism Styling
    └── js/
        └── app.js          # Dynamic Gauges, Tab Handling & API Calls
```

---

## 💻 How to Run Locally on Your PC

1. **Open Command Prompt / Terminal** in this project directory:
   ```bash
   cd c:\Users\AKSHAYA\OneDrive\Desktop\fake_news_detect(project)
   ```

2. **Install Dependencies** (if needed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the ML Model** (Already trained, but you can retrain anytime):
   ```bash
   python model_trainer.py
   ```

4. **Start the Web Application**:
   ```bash
   python app.py
   ```

5. **Open Browser**:
   Navigate to `http://127.0.0.1:5000`

---

## 🚀 Free Deployment Guide (Render.com / PythonAnywhere)

### Option A: Deploying on Render.com (Recommended - Free)
1. Push project folder to **GitHub**.
2. Sign up at [Render.com](https://render.com).
3. Click **New +** -> **Web Service**.
4. Connect your GitHub Repository.
5. Set build settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click **Deploy**. Render will generate a live public URL (e.g. `https://verifact-ai.onrender.com`).

---

## 🎤 Project Presentation & Interview Explanation Guide

### 1. Problem Statement
> "In today's digital age, fake news, rumors, and misleading health/financial scams spread rapidly on social media platforms. Users often lack an easy tool to verify claims or find authentic news sources covering the topic."

### 2. Proposed Solution
> "VeriFact AI is a Machine Learning powered web system that analyzes news text or URLs, calculates a Real vs. Fake truth probability percentage, highlights deceptive clickbait phrases, and automatically searches verified news engines (like Google News) to provide real articles for cross-verification."

### 3. Key Technical Highlights
- **ML Classifier**: Scikit-Learn TF-IDF vectorization paired with Logistic Regression.
- **NLP Heuristics**: Sensationalism index evaluating ALL-CAPS ratios, punctuation abuse, and trigger word detection.
- **Cross-Verification Engine**: Extracts key entities and queries real news feeds for verified articles.
- **Modern UI**: Full Glassmorphic Single Page Application responsive on desktop and mobile.
