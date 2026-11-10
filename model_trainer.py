import pickle
import re
import string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_dataset():
    data = [
        # REAL NEWS (Label 1)
        ("NASA successfully launches new Mars rover mission to study ancient lake bed", 1),
        ("Scientists discover new species of deep sea fish in the Pacific Ocean Mariana Trench", 1),
        ("Global stock markets reach record high following strong economic and earnings reports", 1),
        ("World Health Organization publishes updated guidelines on nutrition and cardiovascular health", 1),
        ("Reserve Bank of India announces new digital currency framework for commercial transactions", 1),
        ("Electric vehicle sales surpass traditional combustion engine cars in Scandinavia", 1),
        ("Tech giant announces 10 billion investment in renewable solar energy infrastructure", 1),
        ("Prime Minister addresses parliament regarding international trade agreements and employment", 1),
        ("ISRO successfully places communication satellites into low earth orbit rocket mission space", 1),
        ("New cancer treatment shows promising 85 percent efficacy in Phase III clinical trials", 1),
        ("United Nations hosts global climate summit with leaders committing to net zero targets", 1),
        ("Archaeologists unearth 3000 year old ancient city in Egypt near Luxor valley", 1),
        ("Supreme Court delivers landmark judgment on data privacy and digital rights", 1),
        ("Major breakthrough in nuclear fusion energy reported by national research laboratory", 1),
        ("High speed rail network expansion connects major metropolitan cities reducing travel time", 1),
        ("Government approves new national education policy focusing on skill development", 1),
        ("Artificial Intelligence tool assists doctors in early detection of diabetic retinopathy", 1),
        ("Global ocean cleanup initiative removes over 100 tons of plastic from Pacific Ocean", 1),
        ("Central bank lowers benchmark interest rates to boost manufacturing and consumer spending", 1),
        ("Astronomers detect water vapor signatures in atmosphere of exoplanet light years away", 1),
        ("Indian Space Research Organisation prepares for upcoming Gaganyaan human spaceflight mission", 1),
        ("Automobile manufacturers agree on standardizing EV charging connectors across Europe", 1),
        ("New agricultural technology increases crop yield while reducing water consumption", 1),
        ("International Monetary Fund projects steady economic growth for emerging markets", 1),
        ("Nobel Prize in Physics awarded for pioneering experiments in quantum entanglement", 1),
        ("Ministry of Health launches nationwide vaccination campaign against seasonal influenza", 1),
        ("Breakthrough battery tech allows smartphones to charge in under 5 minutes", 1),
        ("Metropolitan city inaugurates new solar-powered metro line serving commuters daily", 1),
        ("Researchers develop bio-degradable alternative to single-use plastic packaging", 1),
        ("Global alliance formed to protect endangered rainforest ecosystems in South America", 1),

        # FAKE NEWS (Label 0)
        ("SHOCKING: Drinking boiled lemon water completely cures all forms of cancer in 24 hours!", 0),
        ("Secret alien spaceship discovered hidden inside moon crater leaked government documents prove", 0),
        ("Miracle pill allows you to lose 30 kgs in 3 days without diet or exercise doctors hate this secret", 0),
        ("CONFIRMED: Government introducing microchips in currency notes to track every citizen daily", 0),
        ("Famous celebrity secret scandal exposed clicked this link before video gets deleted forever", 0),
        ("Drinking salt water every morning permanently eliminates diabetes experts don't want you to know", 0),
        ("BREAKING: Scientists confirm Earth will lose gravity for 5 minutes this Friday night stay indoors", 0),
        ("Secret illuminati meeting leaked script reveals exact date of global internet shutdown", 0),
        ("Ancient banana peel remedy cures baldness overnight guaranteed results 100 percent natural", 0),
        ("Billionaire giving away free iPhones to anyone who shares this post in 10 groups immediately", 0),
        ("5G towers proven to emit mind control signals according to anonymous whistleblower scientist", 0),
        ("Eating raw onions cured 100 percent of patients from viral infections overnight official report suppressed", 0),
        ("NASA hides second sun approaching earth that will cause 3 days of total darkness worldwide", 0),
        ("Local man becomes billionaire in 2 days using this simple secret app that banks banned", 0),
        ("ALERT: Tap water contaminated with mind-altering chemicals buy special water filters now", 0),
        ("Hollywood actor found alive in secret island 10 years after fake death conspiracy revealed", 0),
        ("Putting garlic in your ears overnight completely restores 100 percent hearing loss instantly", 0),
        ("Government planning to replace all paper money with social credit points next month leak confirms", 0),
        ("Alien mummy discovered in backyard garden tests show 99 percent non-human DNA", 0),
        ("Shocking truth about toothpaste ingredients that poison your brain revealed by whistleblower", 0),
        ("Miracle magnetic bracelet cures chronic arthritis pain in 10 minutes buy 1 get 1 free today", 0),
        ("Secret underground city built for elites to survive upcoming asteroid impact NASA coverup", 0),
        ("Drinking vinegar before sleep burns 5 pounds of body fat while you sleep proven miracle method", 0),
        ("BREAKING: World leaders secretly reptilian shapeshifters footage caught on live broadcast", 0),
        ("This 5-second morning ritual eliminates all joint pain forever pharmacy companies panicked", 0),
        ("Mobile phones emit dangerous radiation that turns water into toxic poison when charging", 0),
        ("Mysterious giant sea creature washes shore on beach predicted in ancient prophecy", 0),
        ("Government adding tracking nano-bots to public tap water supply to monitor sleep cycles", 0),
        ("Celebrity exposes secret wealth formula on live television talk show host banned from airing", 0),
        ("Eating 3 cloves of raw garlic every hour renders you immune to all viral diseases forever", 0),
    ]

    df = pd.DataFrame(data, columns=['text', 'label'])
    return df

def train_and_save():
    df = build_dataset()
    df['cleaned_text'] = df['text'].apply(clean_text)

    X = df['cleaned_text']
    y = df['label']

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, stop_words='english', sublinear_tf=True)
    X_tfidf = vectorizer.fit_transform(X)

    clf = LogisticRegression(C=2.0, random_state=42)
    clf.fit(X_tfidf, y)

    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)

    with open('log_reg.pkl', 'wb') as f:
        pickle.dump(clf, f)

    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    print("Model retrained successfully with LogisticRegression!")

if __name__ == '__main__':
    train_and_save()
