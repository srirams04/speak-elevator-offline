# Voice-Activated Elevator Interface

## Overview

This project is a Voice-Activated Elevator Interface implemented using Python, designed to operate on a Raspberry Pi. The system integrates speech recognition and text-to-speech capabilities to allow users to control the elevator with voice commands. The interface is built using the `tkinter` library for the GUI, `pyttsx3` for text-to-speech, `speech_recognition` for capturing and recognizing speech, and `faster-whisper` for transcription of audio to text.

## Features

- **Voice Command Recognition**: Users can control the elevator by speaking commands. Commands can include floor numbers, door operations, and emergency alerts.
- **Text-to-Speech Feedback**: The system provides auditory feedback to the user for confirmations and alerts using the `pyttsx3` library.
- **Graphical User Interface (GUI)**: A user-friendly GUI built with `tkinter` displays the current state of the elevator, including the current floor, door status, and direction of movement.
- **Real-time Updates**: The interface dynamically updates the current floor, door status, and elevator movement direction in real-time.
- **Raspberry Pi Compatibility**: Designed to run on a Raspberry Pi, making it an accessible and affordable solution for various environments.

## Installation

### Prerequisites

- Raspberry Pi with Python installed
- Microphone for voice input
- Speaker for audio output
- Required Python libraries: `tkinter`, `pyttsx3`, `faster-whisper`, `speech_recognition`

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/voice-activated-elevator.git
   cd voice-activated-elevator
   ```

2. **Install Dependencies**:
   ```bash
   pip install pyttsx3 faster-whisper speech_recognition
   ```

3. **Run the Application**:
   ```bash
   python Voice_elevator_usingwhisper.py
   ```

## Usage

Once the application is running, the user can interact with the elevator via voice commands. The system will prompt the user to speak and will process the input to perform the corresponding action, such as moving to a specified floor, opening or closing the door, or handling emergency situations.

### Voice Commands

- **Floor Selection**: "Floor [number]" (e.g., "Floor 3")
- **Door Operations**: "Open door", "Close door"
- **Emergency**: "Emergency"

The GUI will display "Say something!" when it is ready to receive a voice command. The elevator will move to the requested floor, open/close the doors, and handle emergency situations accordingly.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- [Whisper Model](https://github.com/openai/whisper) for the speech recognition engine
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for the text-to-speech functionality
- [Raspberry Pi](https://www.raspberrypi.org) for providing an affordable platform for this project

---

Feel free to adjust the repository URL, project details, or any other information as needed. This README provides a clear and concise overview of your project, guiding users through installation, usage, and contributing.
