"""
Speech Module - Text-to-Speech Conversion
Handles text-to-speech functionality with queue management
"""
import pyttsx3
import logging
import threading
import queue
import time

class VoiceSpeaker:
    """
    Voice Speaker class for text-to-speech conversion.
    
    This class manages the TTS engine, provides queued speech processing,
    and handles both immediate and queued speech requests with proper
    resource management.
    """
    
    def __init__(self):
        """
        Initialize the TTS engine and configure voice settings.
        
        Sets up the text-to-speech engine with optimal voice configuration
        and starts a background speech processing thread.
        """
        try:
            self.engine = pyttsx3.init()
            self.is_speaking = False
            self._configure_voice()
            self.speech_queue = queue.Queue()
            self.stop_flag = threading.Event()
            
            # Background speech thread
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
            
            print("Speech engine initialized successfully!")
            
        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def _configure_voice(self):
        """
        Configure voice settings for optimal speech quality.
        
        Sets up voice selection, speech rate, and volume levels
        for the best possible speech output.
        """
        if not self.engine:
            return
        
        try:
            # List available voices and debug
            voices = self.engine.getProperty('voices')
            print(f"Found {len(voices)} voices:")
            
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} ({voice.id})")
            
            # Select first voice (most reliable)
            if voices:
                selected_voice = voices[0]
                self.engine.setProperty('voice', selected_voice.id)
                print(f"Selected voice: {selected_voice.name}")
            
            # Configure speech rate
            rate = self.engine.getProperty('rate')
            new_rate = max(150, rate - 50)
            self.engine.setProperty('rate', new_rate)
            print(f"Speech rate: {new_rate}")
            
            # Set volume to maximum
            self.engine.setProperty('volume', 1.0)
            print(f"Volume level: 1.0 (maximum)")
            
        except Exception as e:
            logging.error(f"Error during voice configuration: {e}")
    
    def _speech_worker(self):
        """
        Background worker for processing speech queue.
        
        This method runs in a separate thread and processes
        speech requests from the queue continuously.
        """
        while not self.stop_flag.is_set():
            try:
                # Get text from queue (1 second timeout)
                text = self.speech_queue.get(timeout=1)
                
                if text and self.engine:
                    self.is_speaking = True
                    print(f"Speaking: {text}")
                    
                    self.engine.say(text)
                    self.engine.runAndWait()
                    
                    self.is_speaking = False
                    print("Speech completed.")
                
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Speech worker error: {e}")
                self.is_speaking = False
    
    def speak(self, text, wait=False):
        """
        Speak text using the TTS engine.
        
        Args:
            text (str): Text to be spoken
            wait (bool): Wait until speech is finished
        """
        if not text:
            return
        
        if not self.engine:
            print(f"TTS not available. Text: {text}")
            return
        
        try:
            # Add text to queue
            self.speech_queue.put(text)
            
            # Optionally wait for completion
            if wait:
                self.wait_until_done()
                
        except Exception as e:
            logging.error(f"Error during speech: {e}")
            print(f"Speech error. Text: {text}")
    
    def speak_immediately(self, text):
        """
        Speak text immediately (bypassing queue).
        
        This method clears the current queue and speaks
        the provided text immediately.
        
        Args:
            text (str): Text to be spoken immediately
        """
        if not text or not self.engine:
            if not self.engine:
                print(f"TTS not available. Text: {text}")
            return
        
        try:
            # Clear queue
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    break
            
            # Speak immediately
            self.is_speaking = True
            print(f"Urgent speech: {text}")
            
            self.engine.say(text)
            self.engine.runAndWait()
            
            self.is_speaking = False
            print("Urgent speech completed.")
            
        except Exception as e:
            logging.error(f"Error during urgent speech: {e}")
            self.is_speaking = False
    
    def wait_until_done(self, timeout=30):
        """
        Wait until all speech is completed.
        
        Args:
            timeout (int): Maximum wait time in seconds
        """
        start_time = time.time()
        
        while (self.is_speaking or not self.speech_queue.empty()) and time.time() - start_time < timeout:
            time.sleep(0.1)
    
    def stop_all_speech(self):
        """
        Stop all speech and clear the queue.
        
        This method immediately stops any ongoing speech
        and clears all pending speech requests.
        """
        try:
            # Clear queue
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    break
            
            # Stop engine
            if self.engine:
                self.engine.stop()
            
            self.is_speaking = False
            print("All speech stopped.")
            
        except Exception as e:
            logging.error(f"Error stopping speech: {e}")
    
    def cleanup(self):
        """
        Clean up resources and stop background thread.
        
        This method ensures proper cleanup of all resources
        including the background speech thread.
        """
        self.stop_flag.set()
        self.stop_all_speech()
        
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)

# Test section
if __name__ == "__main__":
    speaker = VoiceSpeaker()
    
    try:
        print("TTS Simple Test Starting...")
        
        # Direct engine test
        if speaker.engine:
            print("Direct engine test...")
            speaker.engine.say("Test message, can you hear me?")
            speaker.engine.runAndWait()
        
        print("\nSpeaker.speak() test...")
        speaker.speak_immediately("This is the second test message")
        
        print("Test completed!")
        
    except KeyboardInterrupt:
        print("Test stopped.")
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        speaker.cleanup() 