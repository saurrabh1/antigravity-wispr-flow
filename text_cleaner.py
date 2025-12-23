import re

class TextCleaner:
    def __init__(self):
        self.filler_words = [
            r'\bum\b', r'\buh\b', r'\blike\b', r'\byou know\b',
            r'\bso\b', r'\bactually\b', r'\bbasically\b', r'\bkind of\b'
        ]

    def clean(self, text):
        if not text:
            return ""

        cleaned_text = text
        
        # Remove filler words (case insensitive)
        for pattern in self.filler_words:
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)

        # Remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # Capitalize first letter
        if cleaned_text:
            cleaned_text = cleaned_text[0].upper() + cleaned_text[1:]

        # Ensure it ends with punctuation if it looks like a sentence
        if cleaned_text and cleaned_text[-1] not in ['.', '!', '?', ',']:
            cleaned_text += '.'

        return cleaned_text
