from rake_nltk import Rake
import nltk
import re

# Download required datasets quietly
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

def extract_keywords(description, max_phrases=8, min_length=1, max_length=3):
    """Extract SEO keywords from description with robust error handling"""
    if not description or len(description.strip()) == 0:
        return ["No keywords found"]
    
    try:
        r = Rake(
            min_length=min_length,
            max_length=max_length,
            include_repeated_phrases=False
        )
        r.extract_keywords_from_text(description)
        phrases = r.get_ranked_phrases()
        
        # Filter out empty phrases and limit length
        return [phrase for phrase in phrases[:max_phrases] if phrase.strip()]
    
    except Exception:
        # Fallback simple keyword extraction
        words = [word.lower() for word in re.findall(r'\b\w+\b', description) 
                if len(word) > 3 and word.lower() not in nltk.corpus.stopwords.words('english')]
        return list(set(words))[:max_phrases]

def generate_meta_description(description, max_length=160):
    """Create SEO-friendly meta description with smart truncation"""
    if not description:
        return "Professional product description with key features and benefits."
    
    # Clean up description
    clean_desc = re.sub(r'\s+', ' ', description).strip()
    
    # Truncate at sentence end if possible
    if len(clean_desc) <= max_length:
        return clean_desc
    
    # Find last punctuation before max length
    last_punct = max(
        clean_desc.rfind('.', 0, max_length),
        clean_desc.rfind('!', 0, max_length),
        clean_desc.rfind('?', 0, max_length)
    )
    
    if last_punct > 0.7 * max_length:  # Only use if reasonable position
        return clean_desc[:last_punct + 1]
    
    return clean_desc[:max_length-3] + "..."

def calculate_readability(description):
    """Calculate Flesch Reading Ease score with robust fallback"""
    if not description:
        return 85  # Default good score
    
    try:
        # Split into sentences and words
        sentences = [s.strip() for s in re.split(r'[.!?]', description) if s.strip()]
        words = [word for word in re.findall(r'\b\w+\b', description) if word]
        
        # Handle edge cases
        if len(sentences) == 0 or len(words) == 0:
            return 85
            
        syllable_count = sum(count_syllables(word) for word in words)
        
        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * (len(words)/len(sentences)) - 84.6 * (syllable_count/len(words))
        
        # Ensure score is within 0-100 range
        return max(0, min(100, score))
    
    except Exception:
        return 85  # Fallback value

def count_syllables(word):
    """Approximate syllable count with enhanced rules"""
    # Handle empty words
    word = word.lower().strip()
    if len(word) <= 0:
        return 0
    
    # Special cases
    if word.endswith('es') or word.endswith('ed'):
        word = word[:-2]
    
    # Count vowel groups
    vowels = "aeiouy"
    count = 0
    prev_char_vowel = False
    
    for char in word:
        if char in vowels:
            if not prev_char_vowel:
                count += 1
            prev_char_vowel = True
        else:
            prev_char_vowel = False
    
    # Adjustments
    if word.endswith('e') and count > 1:
        count -= 1
    if count == 0:  # All words have at least one syllable
        count = 1
        
    return count