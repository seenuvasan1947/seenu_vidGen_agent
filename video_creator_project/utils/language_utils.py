# from deep_translator import GoogleTranslator
# from gtts import gTTS
# from config import SUPPORTED_LANGUAGES

# def initialize_supported_languages():
#     global SUPPORTED_LANGUAGES
#     SUPPORTED_LANGUAGES.update(
#         set(GoogleTranslator().get_supported_languages()) & set(gTTS.lang.tts_langs().keys())
#     )

# def get_supported_languages():
#     return sorted(list(SUPPORTED_LANGUAGES))

# def display_language_options():
#     languages = get_supported_languages()
#     print("\nAvailable languages for translation and text-to-speech:")
#     for i, lang in enumerate(languages, 1):
#         print(f"{i}. {lang.capitalize()}")
#     return languages

# def get_language_choice(prompt):
#     print(prompt)
#     languages = display_language_options()
#     while True:
#         try:
#             lang_index = int(input("Enter the number of the desired language: ")) - 1
#             if 0 <= lang_index < len(languages):
#                 return languages[lang_index]
#             else:
#                 print("Invalid choice. Please try again.")
#         except ValueError:
#             print("Please enter a valid number.")

# initialize_supported_languages()


from deep_translator import GoogleTranslator
from gtts import gTTS
import gtts.lang
from config import SUPPORTED_LANGUAGES

def initialize_supported_languages():
    global SUPPORTED_LANGUAGES
    SUPPORTED_LANGUAGES = list(
        set(GoogleTranslator().get_supported_languages()) & set(gtts.lang.tts_langs().keys())
    )

def get_supported_languages():
    return sorted(list(SUPPORTED_LANGUAGES))

def display_language_options():
    languages = get_supported_languages()
    print("\nAvailable languages for translation and text-to-speech:")
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang.capitalize()}")
    return languages

def get_language_choice(prompt):
    print(prompt)
    languages = display_language_options()
    while True:
        try:
            lang_index = int(input("Enter the number of the desired language: ")) - 1
            if 0 <= lang_index < len(languages):
                return languages[lang_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

initialize_supported_languages()