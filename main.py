"""
Main Entry Point - Voice Conversation Bot
Orchestrates all components and manages the application lifecycle
"""
import logging
import sys
import signal
import time

# Import modules
from greeting.greet import greet_user, speak_text
from listener.listen import VoiceListener
from chat.chat import VoiceChatBot
from speaker.speak import VoiceSpeaker

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_bot.log'),
        logging.StreamHandler()
    ]
)

class VoiceConversationBot:
    """
    Main bot class that orchestrates all voice conversation components.
    
    This class manages the lifecycle of the voice conversation bot,
    including initialization, speech processing, and graceful shutdown.
    """
    
    def __init__(self):
        """
        Initialize the main bot class.
        
        Sets up signal handlers for graceful shutdown and initializes
        component references to None.
        """
        self.listener = None
        self.chatbot = None
        self.speaker = None
        self.is_running = False
        
        # Signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """
        Signal handler for clean shutdown.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        print("\nShutdown signal received...")
        self.shutdown()
        sys.exit(0)
    
    def initialize_components(self):
        """
        Initialize all bot components.
        
        Returns:
            bool: True if all components initialized successfully, False otherwise
        """
        try:
            print("Initializing bot components...")
            
            # Initialize listener
            print("1. Starting listening module...")
            self.listener = VoiceListener()
            
            # Initialize chatbot
            print("2. Starting chat module...")
            self.chatbot = VoiceChatBot()
            
            # Initialize speaker
            print("3. Starting speech module...")
            self.speaker = VoiceSpeaker()
            
            print("All components initialized successfully!")
            return True
            
        except Exception as e:
            logging.error(f"Component initialization error: {e}")
            print(f"Error initializing components: {e}")
            return False
    
    def handle_user_speech(self, user_text):
        """
        Process user speech and generate bot response.
        
        Args:
            user_text (str): The text recognized from user's speech
        """
        try:
            print(f"Processing: {user_text}")
            
            # Get response from Chat API
            bot_response = self.chatbot.get_response(user_text)
            
            print(f"Bot response: {bot_response}")
            
            if bot_response:
                print("Sending to TTS...")
                # Use WINDOWS NATIVE TTS
                speak_text(bot_response)
            else:
                # Default response in case of error
                error_message = "Sorry, an error occurred. Please try again."
                print(f"Error - Assistant: {error_message}")
                speak_text(error_message)
                
        except Exception as e:
            logging.error(f"Speech processing error: {e}")
            error_message = "A technical issue occurred. Continuing."
            print(f"Error: {error_message}")
            self.speaker.speak(error_message)
    
    def run(self):
        """
        Run the main bot loop.
        
        This method orchestrates the entire voice conversation flow,
        including initialization, greeting, and continuous listening.
        """
        try:
            print("Voice Conversation Bot Starting...")
            print("=" * 50)
            
            # Initialize components
            if not self.initialize_components():
                print("Bot failed to start!")
                return
            
            # Perform greeting
            print("\n1. Performing greeting...")
            greet_user()
            
            # Short wait
            time.sleep(2)
            
            print("\n2. Starting continuous listening mode...")
            print("=" * 50)
            print("Tips:")
            print("   • Speak clearly and audibly")
            print("   • Say 'exit', 'close' or 'finish' to quit")
            print("   • Please wait while the bot responds")
            print("=" * 50)
            
            self.is_running = True
            
            # Start continuous listening
            self.listener.continuous_listen(
                on_speech_callback=self.handle_user_speech,
                exit_phrases=['exit', 'close', 'finish', 'stop', 'quit', 'bye']
            )
            
        except KeyboardInterrupt:
            print("\n\nStopped by user.")
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            print(f"Critical error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """
        Cleanly shutdown the bot.
        
        This method ensures all resources are properly cleaned up
        and the bot stops gracefully.
        """
        if not self.is_running:
            return
        
        self.is_running = False
        
        print("\nShutting down bot...")
        
        try:
            # Clean up speaker
            if self.speaker:
                self.speaker.cleanup()
                print("Speech module closed")
            
            # Clean up other resources
            print("All resources cleaned up")
            
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
        
        print("Goodbye!")

def main():
    """
    Main function that creates and runs the voice conversation bot.
    
    This is the entry point of the application that handles
    the overall program lifecycle and error handling.
    """
    try:
        # Create and run bot instance
        bot = VoiceConversationBot()
        bot.run()
        
    except Exception as e:
        logging.error(f"Main program error: {e}")
        print(f"Program failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 