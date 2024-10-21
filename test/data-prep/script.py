import nltk
import re
import string
import docx

# Step 1: Data Extraction
doc = docx.Document('guide.docx')
text = '\n'.join([para.text for para in doc.paragraphs])

# Step 2: Convert to Lower Case
text = text.lower()

# Step 3: Tokenization
nltk.download('punkt_tab')
tokens = nltk.word_tokenize(text)

# Step 4: Punctuation Removal
tokens = [word for word in tokens if word.isalpha()]

# Step 5: Cleaning Special Characters
text = re.sub(r'[^\w\s]', '', text)  # Removes all punctuation
text = re.sub(r'\d+', '', text)       # Removes digits
text = re.sub(r'\s+', ' ', text).strip()  # Removes extra whitespace

# Note: Since we re-processed 'text', we need to re-tokenize
tokens = nltk.word_tokenize(text)

# Step 6: Remove Stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords


stop_words = set(stopwords.words('english'))
custom_stopwords = {'may', 'shall', 'must', 'every'}
stop_words.update(custom_stopwords)
filtered_tokens = [word for word in tokens if word not in stop_words]

# Step 7: Stemming and Lemmatization
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
pos_tags = nltk.pos_tag(filtered_tokens)

def get_wordnet_pos(tag):
    from nltk.corpus import wordnet
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags]

# Final Preprocessed Text
cleaned_text = ' '.join(lemmatized_tokens)

print(lemmatized_tokens[:50])  # View the first 50 tokens


with open('cleaned_tokens_guide.txt', 'w', encoding='utf-8') as f:
    for token in lemmatized_tokens:
        f.write(f"{token}\n")
