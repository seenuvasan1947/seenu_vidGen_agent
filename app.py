import google.generativeai as genai
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment

# Configure the Gemini API (replace with your actual API key)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Languages supported by both GoogleTranslator and gTTS
SUPPORTED_LANGUAGES = set(GoogleTranslator().get_supported_languages()) & set(gTTS.lang.tts_langs().keys())

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

def generate_response_and_image_description(prompt):
    model = genai.GenerativeModel('gemini-pro')
    full_prompt = f"""{prompt}

Additionally, provide a single sentence in English that describes an image that would be suitable for this content. Separate the main content and the image description with a line of 10 dashes (----------).

Main content:"""
    response = model.generate_content(full_prompt)
    content, image_desc = response.text.split('----------')
    return content.strip(), image_desc.strip()

def translate_text(text, source_language, target_language):
    if source_language == target_language:
        return text
    translator = GoogleTranslator(source=source_language, target=target_language)
    return translator.translate(text)

def text_to_speech(text, language, output_file="output.mp3"):
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)
    print(f"Audio saved as {output_file}")
    return output_file

def get_image_folder():
    while True:
        folder = input("Enter the folder path containing your images: ")
        if os.path.isdir(folder):
            image_files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                return [os.path.join(folder, f) for f in image_files]
            else:
                print("No image files found in the specified folder. Please try again.")
        else:
            print("Invalid folder path. Please try again.")

def create_video_from_images(image_files, audio_file, duration, output_file="output.mp4"):
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration
    
    # Adjust audio speed to match target duration if necessary
    if abs(audio_duration - duration * 60) > 1:  # Allow 1 second tolerance
        speed_factor = audio_duration / (duration * 60)
        audio_clip = audio_clip.speedx(factor=speed_factor)
    
    image_clips = [ImageClip(img).set_duration(duration * 60 / len(image_files)) for img in image_files]
    video_clip = concatenate_videoclips(image_clips, method="compose")
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, fps=24)
    print(f"Video saved as {output_file}")
    return output_file

def main():
    input_type, *args = get_user_input()
    
    if input_type == "topic":
        topic, duration = args
        prompt = f"Provide detailed information about the topic or book: '{topic}'. Include key points, interesting facts, and a suggested structure for a {duration}-minute video."
        content, image_description = generate_response_and_image_description(prompt)
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
            content = translate_text(content, "english", target_language)
    else:
        target_language = source_language
    
    print(f"\nContent ({target_language.capitalize()}):")
    print(content)
    
    # Convert text to speech
    audio_file = text_to_speech(content, target_language)
    
    # Get images from user
    image_files = get_image_folder()
    
    # Create video
    output_file = create_video_from_images(image_files, audio_file, float(duration) if input_type == "topic" else 1.0)
    
    if output_file and os.path.exists(output_file):
        print("Video creation successful!")
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        print(f"Output file size: {file_size:.2f} MB")
    else:
        print("Video creation failed.")

if __name__ == "__main__":
    main()
