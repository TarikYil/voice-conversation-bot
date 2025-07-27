"""
Greeting Module - Voice User Welcome
Handles initial greeting and text-to-speech functionality
"""
import pyttsx3
import logging

def init_tts_engine():
    """
    Initialize and configure the TTS engine.
    
    Sets up the text-to-speech engine with appropriate
    voice settings for optimal speech quality.
    
    Returns:
        pyttsx3.Engine or None: Configured TTS engine or None if initialization fails
    """
    try:
        engine = pyttsx3.init()
        
        # Configure speech rate
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)
        
        # Configure volume level
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 0.9)
        
        return engine
    except Exception as e:
        logging.error(f"Failed to initialize TTS engine: {e}")
        return None

def greet_user():
    """
    Greet the user with voice welcome message.
    
    This function provides the initial voice greeting when
    the bot starts up, welcoming the user to the voice assistant.
    """
    try:
        engine = init_tts_engine()
        
        if engine is None:
            print("TTS engine failed to initialize. Providing text greeting.")
            print("Hello! Welcome to your voice assistant bot!")
            return
        
        greeting_message = "Hello! Welcome to your voice assistant bot. I'm ready to talk with you."
        
        print(f"Assistant: {greeting_message}")
        engine.say(greeting_message)
        engine.runAndWait()
        
        print("Greeting completed. Transitioning to listening mode...")
        
    except Exception as e:
        logging.error(f"Error during greeting: {e}")
        print("An error occurred during greeting, but continuing...")

def speak_text(text):
    """
    Speak any text using Windows TTS subprocess.
    
    This function uses Windows native text-to-speech capabilities
    to convert text to speech with better performance than pyttsx3.
    
    Args:
        text (str): The text to be spoken
    """
    try:
        print(f"Speaking with Windows TTS: {text}")
        
        # Method 1: Windows built-in TTS
        import subprocess
        import os
        
        # PowerShell TTS command
        powershell_cmd = f'''
Add-Type -AssemblyName System.Speech;
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$speak.Rate = 0;
$speak.Volume = 100;
$speak.Speak("{text.replace('"', "'")}");
'''
        
        print("Running PowerShell TTS...")
        result = subprocess.run([
            "powershell", "-Command", powershell_cmd
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Windows TTS successful")
        else:
            print(f"PowerShell TTS error: {result.stderr}")
            # Fallback: Old method
            _fallback_tts(text)
        
    except subprocess.TimeoutExpired:
        print("TTS timeout - using fallback")
        _fallback_tts(text)
    except Exception as e:
        print(f"Windows TTS error: {e}")
        _fallback_tts(text)

def _fallback_tts(text):
    """
    Fallback TTS method using pyttsx3.
    
    This is used when Windows native TTS fails or times out.
    
    Args:
        text (str): The text to be spoken
    """
    try:
        print("Using fallback TTS...")
        engine = init_tts_engine()
        if engine:
            engine.say(text)
            engine.runAndWait()
            print("Fallback TTS completed")
    except Exception as e:
        print(f"Fallback TTS error: {e}")
        print(f"Text: {text}")

if __name__ == "__main__":
    greet_user() 