import pickle
import re
import string
from model_trainer import clean_text
from news_finder import find_related_real_news

def load_artifacts():
    try:
        with open('model.pkl', 'rb') as f:
            clf_model = pickle.load(f)
        with open('log_reg.pkl', 'rb') as f:
            log_reg_model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        return clf_model, log_reg_model, tfidf_vectorizer, True
    except Exception as e:
        print(f"Warning: Models not loaded ({e}).")
        return None, None, None, False

CLICKBAIT_KEYWORDS = [
    'shocking', 'miracle', 'doctors hate', 'secret', 'banned', 'guaranteed',
    'you won\'t believe', 'overnight', 'cures', 'exposed', 'leaked', 'conspiracy',
    'reptilian', 'illuminati', 'alien', 'mind control', 'free iphone', 'unbelievable',
    'panicked', 'scandal', '100%', 'insane', 'hidden truth', 'they don\'t want you to know'
]

def analyze_sensationalism(text):
    text_lower = text.lower()
    found_triggers = []
    
    for kw in CLICKBAIT_KEYWORDS:
        if kw in text_lower:
            found_triggers.append(kw.upper())
            
    # Remove standard 2-5 uppercase letter acronyms like ISRO, NASA, WHO, IMF, EV, AI, LVM3
    text_no_acronyms = re.sub(r'\b[A-Z0-9]{2,5}\b', '', text)
    
    caps_count = sum(1 for c in text_no_acronyms if c.isupper())
    total_letters = sum(1 for c in text_no_acronyms if c.isalpha()) or 1
    caps_ratio = caps_count / total_letters
    
    punct_count = text.count('!') + text.count('?')
    
    sensational_score = len(found_triggers) * 30 + int(caps_ratio * 80) + (punct_count * 15)
    sensational_score = min(100, sensational_score)
    
    return {
        'sensationalism_score': sensational_score,
        'flagged_words': found_triggers,
        'caps_percentage': round(caps_ratio * 100, 1),
        'dramatic_punctuation': punct_count
    }

def get_highlighted_text(text, flagged_words):
    highlighted = text
    for word in flagged_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted = pattern.sub(f'<span class="deceptive-highlight">{word}</span>', highlighted)
    return highlighted

def predict_authenticity(text, url=None):
    if not text or len(text.strip()) == 0:
        return {'error': 'Text cannot be empty'}
        
    clf_model, log_reg_model, tfidf_vectorizer, model_loaded = load_artifacts()
    cleaned = clean_text(text)
    
    if model_loaded:
        X_vec = tfidf_vectorizer.transform([cleaned])
        try:
            probs = log_reg_model.predict_proba(X_vec)[0]
            real_prob = float(probs[1]) * 100
        except Exception:
            real_prob = 50.0
    else:
        real_prob = 50.0

    sensational_info = analyze_sensationalism(text)
    sensational_score = sensational_info['sensationalism_score']
    
    # Adjust score based on sensationalism vs clean academic/journalistic tone
    if sensational_score > 20:
        real_prob = max(5.0, real_prob - (sensational_score * 0.6))
    elif sensational_score == 0 and len(text.split()) >= 5:
        real_prob = min(96.5, real_prob + 25.0)

    fake_prob = 100.0 - real_prob

    real_prob = round(real_prob, 1)
    fake_prob = round(fake_prob, 1)
    
    if real_prob >= 75.0:
        verdict = "Authentic / Real News"
        verdict_code = "REAL"
        confidence_badge = "High Credibility"
        status_color = "#10B981"
    elif real_prob >= 45.0:
        verdict = "Suspicious / Unverified News"
        verdict_code = "UNCERTAIN"
        confidence_badge = "Moderate Risk"
        status_color = "#F59E0B"
    else:
        verdict = "Likely Fake / Deceptive News"
        verdict_code = "FAKE"
        confidence_badge = "High Deception Risk"
        status_color = "#EF4444"

    related_news = find_related_real_news(text)
    highlighted_html = get_highlighted_text(text, sensational_info['flagged_words'])

    return {
        'verdict': verdict,
        'verdict_code': verdict_code,
        'real_percentage': real_prob,
        'fake_percentage': fake_prob,
        'status_color': status_color,
        'confidence_badge': confidence_badge,
        'sensationalism_score': sensational_score,
        'sensational_details': sensational_info,
        'highlighted_text': highlighted_html,
        'related_real_news': related_news['articles'],
        'search_query': related_news['search_query'],
        'word_count': len(text.split()),
        'url_analyzed': url
    }
