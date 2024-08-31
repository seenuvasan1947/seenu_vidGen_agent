from agents.content_agent import ContentAgent
from agents.translation_agent import TranslationAgent
from agents.speech_agent import SpeechAgent
from agents.image_agent import ImageAgent
from agents.video_agent import VideoAgent
from utils.language_utils import get_language_choice
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_user_input():
    print("Choose an option:")
    print("1. Enter a topic or book name")
    print("2. Enter text content directly")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        topic = input("Enter a topic or book name: ")
        duration = float(input("Enter the desired video length in minutes: "))
        return ("topic", topic, duration)
    elif choice == "2":
        print("Is your text in English or another language?")
        print("1. English")
        print("2. Another language")
        lang_choice = input("Enter your choice (1 or 2): ")
        
        if lang_choice == "1":
            text = input("Enter your text in English: ")
            return ("text_english", text)
        elif lang_choice == "2":
            source_language = get_language_choice("\nChoose the language of your text:")
            text = input(f"Enter your text in {source_language.capitalize()}: ")
            return ("text_other", text, source_language)
    else:
        print("Invalid choice. Please try again.")
        return get_user_input()

def main():
    # Get API key from environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    content_agent = ContentAgent(api_key)
    translation_agent = TranslationAgent()
    speech_agent = SpeechAgent()
    image_agent = ImageAgent()
    video_agent = VideoAgent()

    input_type, *args = get_user_input()
    
    if input_type == "topic":
        topic, duration = args
        content, image_description = content_agent.generate_content(topic, duration)
        source_language = "english"
    elif input_type == "text_english":
        content = args[0]
        source_language = "english"
        image_description = "An image representing the main theme of the provided text."
    else:  # text_other
        content, source_language = args
        image_description = "An image representing the main theme of the provided text."
    
    if source_language == "english":
        target_language = get_language_choice("\nChoose the language for the audio:")
        if target_language != "english":
            content = translation_agent.translate(content, "english", target_language)
    else:
        target_language = source_language
    
    print(f"\nContent ({target_language.capitalize()}):")
    print(content)
    
    # Convert text to speech
    audio_file = speech_agent.text_to_speech(content, target_language)
    
    # Get images from user
    image_files = image_agent.get_image_folder()
    
    # Create video
    output_file = video_agent.create_video(image_files, audio_file)
    
    if output_file and os.path.exists(output_file):
        print("Video creation successful!")
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        print(f"Output file size: {file_size:.2f} MB")
    else:
        print("Video creation failed.")

if __name__ == "__main__":
    main()
