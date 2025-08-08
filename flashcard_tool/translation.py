from googletrans import Translator
import pykakasi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JapaneseTranslator:
    def __init__(self):
        self.translator = Translator()
        self.kakasi = pykakasi.kakasi()

    def get_translation_info(self, kanji_word):
        """Get hiragana and English translation for a kanji word"""
        try:
            # Convert kanji to hiragana
            result = self.kakasi.convert(kanji_word)
            hiragana = "".join([item['hira'] for item in result])
            
            # Get English translation
            translation = self.translator.translate(kanji_word, src='ja', dest='en').text
            
            return {
                "kanji": kanji_word,
                "hiragana": hiragana,
                "english_meaning": translation
            }
        except Exception as e:
            logger.error(f"Translation error for '{kanji_word}': {e}")
            return None