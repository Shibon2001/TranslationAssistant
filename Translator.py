from deep_translator import GoogleTranslator
from datetime import datetime
import time
import pyttsx3


# --- Speech Function (Fixed Version) ---
def speak(text, lang_code='en'):
    """Speaks text using the closest available voice for the given language."""
    # Initialize engine fresh each time (fixes skipped lines)
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Adjust speaking speed
    engine.setProperty('volume', 1.0)

    # Try to find a voice matching the target language
    selected_voice = None
    for voice in engine.getProperty('voices'):
        if lang_code.lower() in voice.id.lower() or lang_code.lower() in voice.name.lower():
            selected_voice = voice
            break

    # Fallback to default if no match found
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    else:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

    # Speak the text
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# --- Jarvis Greeting ---
def jarvis_greet():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    greeting_msg = f"{greeting}, sir. I am Jarvis, your personal translation assistant."
    print("🤖 JARVIS: Initializing translator system...")
    time.sleep(1)
    print(f"🤖 JARVIS: {greeting_msg}")
    speak(greeting_msg)
    time.sleep(1)

    # ✅ This line will now speak properly
    intro_msg = "What can I translate for you today, sir?"
    print(f"🤖 JARVIS: {intro_msg}")
    speak(intro_msg)
    print("------------------------------------------------------------\n")
    time.sleep(1)


# --- Get Supported Languages ---
def get_language_mapping():
    languages = GoogleTranslator().get_supported_languages(as_dict=True)
    mapping = {name.title(): code for name, code in languages.items()}
    return mapping


# --- Main Translation Loop ---
def main():
    jarvis_greet()
    language_mapping = get_language_mapping()
    supported_languages = list(language_mapping.keys())

    while True:
        text = input("🗣️  Enter text to translate: ")

        while True:
            target_lang_name = input("🌐 Enter target language (full name, e.g., English, Hindi): ").title()
            if target_lang_name in supported_languages:
                target_lang = language_mapping[target_lang_name]
                break
            else:
                print("❌ Sorry, that language is not supported. Please try again.")
                print(f"Supported languages include: {', '.join(supported_languages[:10])}, ...")

        print("\n🤖 JARVIS: Translating, please wait...\n")
        speak("Translating, please wait.")
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)

        print("------------------------------------------------------------")
        print(f"Original: {text}")
        print(f"Translated ({target_lang_name}): {translated}")
        print("------------------------------------------------------------")

        # Speak the translated text in its language
        speak(translated, lang_code=target_lang)
        speak("Translation complete, sir.")
        print("🤖 JARVIS: Translation complete, sir.\n")

        # ✅ Added polite follow-up messages
        again = input("Do you want me to translate another text, sir? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            goodbye_msg = "Can I translate something else for you today, sir?"
            print(f"\n🤖 JARVIS: {goodbye_msg}")
            speak(goodbye_msg)
            time.sleep(1)

            farewell_msg = "Have a nice day, sir."
            print(f"🤖 JARVIS: {farewell_msg}")
            speak(farewell_msg)
            break

        print("\n------------------------------------------------------------\n")


# --- Run Program ---
if __name__ == "__main__":
    main()
