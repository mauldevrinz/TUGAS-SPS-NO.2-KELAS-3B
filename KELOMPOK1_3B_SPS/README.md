![alt text](https://github.com/atok99/kel.3_sps-edge-impuls-voice-command/blob/main/GUI.jpg?raw=true)
# Voice Recorder and Translator with AI Training for ESP32

This project demonstrates how to build a PyQt6 application for voice recording and automatic translation, which can upload the recorded data to MySQL and Edge Impulse for deep learning processing. The trained model will be converted into an Arduino library for ESP32, enabling it to classify audio inputs intelligently.

## Authors
1. Rizal Khoirul Atok (2042231013)
2. Egga Terbyd Fabryan (2042231029)
3. Valencia Christina Setiowardhani (2042231055)
4. Ahmad Radhy (Supervisor)

Teknik Instrumentasi - Institut Teknologi Sepuluh Nopember

## Features

1. **Voice Recording**: Record audio input using a simple and intuitive GUI.
2. **Automatic Translation**: Translate recorded audio into a target language.
3. **Database Upload**: Store recorded and translated data into a MySQL database.
4. **Edge Impulse Integration**: Upload audio data to Edge Impulse for training deep learning models.
5. **ESP32 Integration**: Deploy the trained model to ESP32 for real-time audio classification.

## Requirements

### Software
- Python 3.8+
- PyQt6
- Edge Impulse CLI
- MySQL Server
- Arduino IDE with ESP32 Core

### Hardware
- ESP32
- Microphone module INMP441 (for ESP32, optional for GUI testing)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/atok99/kel.3_sps-edge-impuls-voice-command
cd pyqt6-voice-ai
```

### 2. Install Python Dependencies
```bash
pip install PyQt6 pyaudio mysql-connector-python edge-impulse-cli googletrans==4.0.0-rc1
```

### 3. Set Up MySQL Database
Create a MySQL database and table to store the recordings and translations:
```sql
CREATE DATABASE voice_ai;
USE voice_ai;

CREATE TABLE recordings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    translation TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Configure Edge Impulse
Install the Edge Impulse CLI and log in:
```bash
npm install -g edge-impulse-cli
edge-impulse-login
```

### 5. Prepare ESP32
Install the ESP32 core in Arduino IDE and ensure necessary libraries are installed.

## Usage

### 1. Run the PyQt6 Application
Start the GUI application:
```bash
python main.py
```

### 2. Record and Translate
- Use the GUI to record audio.
- Automatically translate the audio after recording.

### 3. Upload to MySQL
- Save the recordings and translations to the MySQL database using the GUI.

### 4. Upload to Edge Impulse
- Use the GUI or command line to upload recordings to Edge Impulse for training:
```bash
edge-impulse-uploader recordings/yourfile.wav
```

### 5. Train the Model
- Train a model on Edge Impulse using the uploaded data.

### 6. Export and Deploy to ESP32
- Download the trained model as an Arduino library.
- Include the library in your ESP32 Arduino project.
- Use the model to classify real-time audio inputs.

## Project Structure
```
pyqt6-voice-ai/
├── main.py              # PyQt6 GUI Application
├── recorder.py          # Voice recording logic
├── translator.py        # Translation logic
├── database.py          # MySQL interaction
├── edge_impulse.py      # Edge Impulse integration
├── recordings/          # Saved audio files
└── README.md            # Project documentation
```

## Future Improvements
- Add support for more languages in the translator.
- Enhance the GUI for better user experience.
- Optimize the trained model for low-latency performance on ESP32.

## Contributions
Feel free to fork this repository and submit pull requests. Suggestions and improvements are welcome!

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
