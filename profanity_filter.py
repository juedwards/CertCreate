"""
Profanity Filter Module
=======================
Filters inappropriate content from certificate names to ensure
all generated certificates remain appropriate and professional.
"""

import re

# Common profanity and inappropriate words list
# This is a basic list - in production, consider using a more comprehensive library
BLOCKED_WORDS = {
    # Common profanity (keeping this list family-friendly but effective)
    'ass', 'arse', 'asshole', 'bastard', 'bitch', 'bloody', 'bollocks',
    'bugger', 'bullshit', 'crap', 'damn', 'dick', 'dickhead',
    'fag', 'faggot', 'fuck', 'fucking', 'fucker', 'goddam', 'goddamn',
    'hell', 'homo', 'jerk', 'moron', 'nigger', 'nigga', 'piss', 'prick',
    'pussy', 'retard', 'shit', 'shitty', 'slut', 'twat', 'wanker', 'whore',
    
    # Offensive terms
    'nazi', 'hitler', 'kkk', 'racist',
    
    # Sexual terms
    'anal', 'boob', 'boobs', 'breast', 'cock', 'cum', 'dildo', 'penis',
    'porn', 'sex', 'sexy', 'vagina', 'xxx',
    
    # Drug references
    'cocaine', 'heroin', 'meth', 'crack',
    
    # Violence
    'kill', 'murder', 'rape', 'terrorist',
}

# Common character substitutions used to bypass filters
LEET_SPEAK_MAP = {
    '0': 'o',
    '1': 'i',
    '3': 'e',
    '4': 'a',
    '5': 's',
    '7': 't',
    '8': 'b',
    '@': 'a',
    '$': 's',
    '!': 'i',
    '+': 't',
}


def normalize_text(text):
    """
    Normalize text by converting leet speak and removing special characters.
    
    Args:
        text: The input text to normalize
        
    Returns:
        Normalized lowercase text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    normalized = text.lower()
    
    # Replace leet speak characters
    for leet_char, normal_char in LEET_SPEAK_MAP.items():
        normalized = normalized.replace(leet_char, normal_char)
    
    # Remove spaces and special characters for checking compound words
    # Keep only alphabetic characters
    alpha_only = re.sub(r'[^a-z]', '', normalized)
    
    return alpha_only


def contains_profanity(text):
    """
    Check if the given text contains any profanity or inappropriate content.
    
    Args:
        text: The text to check (name, school name, etc.)
        
    Returns:
        tuple: (bool, str or None) - (contains_profanity, matched_word or None)
    """
    if not text:
        return False, None
    
    # Normalize the text
    normalized = normalize_text(text)
    
    # Check for blocked words
    for word in BLOCKED_WORDS:
        if word in normalized:
            return True, word
    
    # Also check individual words in original text (handles spaces)
    words = text.lower().split()
    for original_word in words:
        normalized_word = normalize_text(original_word)
        if normalized_word in BLOCKED_WORDS:
            return True, normalized_word
    
    return False, None


def check_all_fields(**fields):
    """
    Check multiple fields for profanity at once.
    
    Args:
        **fields: Keyword arguments where key is field name and value is the text
        
    Returns:
        tuple: (is_clean, field_name or None, matched_word or None)
               is_clean is True if all fields are clean
    """
    for field_name, text in fields.items():
        has_profanity, matched = contains_profanity(text)
        if has_profanity:
            return False, field_name, matched
    
    return True, None, None


def get_polite_rejection_message():
    """
    Get a polite message for when content is rejected.
    
    Returns:
        str: A friendly, professional rejection message
    """
    return (
        "We're unable to create a certificate with the information provided. "
        "Please ensure all names are appropriate and professional. "
        "If you believe this is an error, please check your entries and try again."
    )
