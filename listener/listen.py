"""
Listening Module - Speech Recognition and Text Conversion
Handles voice input recognition and conversion to text
"""
import speech_recognition as sr
import logging
import time

class VoiceListener:
    """
    Voice Listener class for speech recognition and text conversion.
    
    This class manages the microphone input, speech recognition,
    and provides both single and continuous listening capabilities.
    """
    
    def __init__(self):
        """
        Initialize the speech recognition object.
        
        Sets up the recognizer and microphone, and calibrates
        for ambient noise to improve recognition accuracy.
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("Calibrating ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            print("Calibration completed.")
    
    def listen_once(self, timeout=5, phrase_time_limit=10):
        """
        Perform single listening session.
        
        Args:
            timeout (int): Time to wait for speech to start (seconds)
            phrase_time_limit (int): Maximum speech duration (seconds)
            
        Returns:
            str or None: Recognized text or None if no speech detected
        """
        try:
            print("Listening... (You can start speaking)")
            
            with self.microphone as source:
                # Capture audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Recognizing speech...")
            
            # Convert to text using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language='en-US')
            print(f"Recognized text: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected")
            return None
        except sr.UnknownValueError:
            print("Speech not recognized or unclear")
            return None
        except sr.RequestError as e:
            logging.error(f"Speech recognition service error: {e}")
            print("Could not connect to speech recognition service")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during listening: {e}")
            print("An error occurred during listening")
            return None
    
    def continuous_listen(self, on_speech_callback, exit_phrases=None):
        """
        Start continuous listening mode.
        
        This method continuously listens for speech and processes
        it through the provided callback function.
        
        Args:
            on_speech_callback (function): Function to call when speech is recognized
            exit_phrases (list): List of phrases that will exit the listening loop
        """
        if exit_phrases is None:
            exit_phrases = ['exit', 'close', 'finish', 'stop', 'quit']
        
        print("Starting continuous listening mode...")
        print("You can say the following to exit:", ', '.join(exit_phrases))
        
        while True:
            try:
                # Listen for speech
                recognized_text = self.listen_once()
                
                if recognized_text:
                    # Check for exit commands
                    if any(exit_phrase in recognized_text.lower() for exit_phrase in exit_phrases):
                        print("Exit command detected. Terminating program...")
                        break
                    
                    # Call the callback function
                    if on_speech_callback:
                        on_speech_callback(recognized_text)
                
                # Short pause
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\nProgram stopped by user.")
                break
            except Exception as e:
                logging.error(f"Error during continuous listening: {e}")
                print("An error occurred, continuing to listen...")
                time.sleep(1)

# Test section
if __name__ == "__main__":
    def test_callback(text):
        print(f"Test callback: {text}")
    
    listener = VoiceListener()
    listener.continuous_listen(test_callback) 