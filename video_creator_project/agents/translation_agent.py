from deep_translator import GoogleTranslator

class TranslationAgent:
    def translate(self, text, source_language, target_language):
        if source_language == target_language:
            return text
        translator = GoogleTranslator(source=source_language, target=target_language)
        return translator.translate(text)