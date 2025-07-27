# VoiceAI Assistant

A professional AI assistant bot that can converse with users through voice. The bot converts speech to text, generates responses using Google Gemini API, and reads the results aloud.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Open%20Source-orange.svg)](https://github.com/)

## Features

- **Speech Recognition**: Converts user speech to text using Google Speech Recognition
- **AI Chat**: Intelligent responses powered by Google Gemini API
- **Text-to-Speech**: Reads responses aloud using Windows TTS
- **Continuous Listening**: Uninterrupted conversation experience
- **English Support**: Full English language support
- **Error Handling**: Robust error catching and management
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Microphone (for audio input)
- Speakers/Headphones (for audio output)
- Internet connection (for Google Gemini API and Google Speech Recognition)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/voice-ai-assistant.git
cd voice-ai-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**
   - Create a `.env` file in the project root
   - Add your Google API key:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

4. **Run the application**
```bash
python main.py
```

### Getting Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click "Get API Key" button
4. Create a new API key
5. Add the key to your `.env` file

## Usage

### Basic Commands

- **Start conversation**: Just speak naturally after the greeting
- **Exit the program**: Say "exit", "close", "finish", "stop", or "quit"

### Example Interaction

```
Bot: "Hello! Welcome to your voice assistant bot. I'm ready to talk with you."
You: "What's the weather like today?"
Bot: "I don't have access to real-time weather data, but I can help you find weather information online."
```

## Project Structure

```
voice-ai-assistant/
├── main.py                  # Main entry point
├── greeting/                # Greeting module
│   └── greet.py
├── listener/                # Speech recognition module
│   └── listen.py
├── chat/                    # Google Gemini API integration
│   ├── chat.py
│   └── config.py
├── speaker/                 # Text-to-speech module
│   └── speak.py
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Configuration

### Chat Settings (`chat/config.py`)

```python
MODEL = "gemini-1.5-flash"   # Google Gemini model
MAX_TOKENS = 500             # Maximum response length
TEMPERATURE = 0.7            # Creativity level (0-1)
```

### Audio Settings

- **Listening Timeout**: 5 seconds (configurable)
- **Speech Duration**: 10 seconds maximum
- **Language**: English (en-US)

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Microphone not working | Check permissions and default microphone settings |
| API errors | Verify your Google API key in `.env` file |
| No audio output | Check volume levels and speaker connections |
| Speech recognition issues | Speak clearly in a quiet environment |

### Log Files

Errors are logged to `voice_bot.log`. Check this file when experiencing issues.

## Development

### Testing Individual Modules

```bash
# Test greeting functionality
python greeting/greet.py

# Test speech recognition
python listener/listen.py

# Test chat functionality
python chat/chat.py

# Test text-to-speech
python speaker/speak.py
```

### Customization

- **System Message**: Modify `SYSTEM_MESSAGE` in `chat/config.py`
- **Exit Commands**: Update `exit_phrases` list in `main.py`
- **Voice Settings**: Edit `_configure_voice` method in `speaker/speak.py`

## Dependencies

- `google-generativeai` - Google Gemini API integration
- `SpeechRecognition` - Speech recognition functionality
- `pyttsx3` - Text-to-speech engine
- `pyaudio` - Audio processing
- `python-dotenv` - Environment variable management

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Review the log file (`voice_bot.log`)
3. Open an [issue](https://github.com/yourusername/voice-ai-assistant/issues)

## Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for AI capabilities
- [Google Speech Recognition](https://cloud.google.com/speech-to-text) for speech processing
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio handling

---


