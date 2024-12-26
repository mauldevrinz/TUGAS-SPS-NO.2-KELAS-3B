![alt text](https://github.com/mauldevrinz/TUGAS-SPS-NO.2-KELAS-3B/blob/main/GUI.png)
# Voice Recorder and Translator with AI Training for ESP32

This project demonstrates how to build a PyQt6 application for voice recording and automatic translation.

## Authors
1. Andik Putra Nazwana (2042231010)
2. Andre Mahesa Bagaskara (2042231012)
3. Akhmad Maulvin Nazir Zakaria (2042231028)
4. Dwi Oktavianto Wahyu Nugroho (Supervisor)

Teknik Instrumentasi - Institut Teknologi Sepuluh Nopember

## Features

1. **Voice Recording**: Record audio input using a simple and intuitive GUI.
2. **Automatic Translation**: Translate recorded audio into a target language.
3. **Database Upload**: Store recorded and translated data into a MySQL database.
4. **Edge Impulse Integration**: Upload audio data to Edge Impulse for training deep learning models.

## Requirements

### Software
- Python 3.8+
- PyQt6
- Edge Impulse CLI
- MySQL Server

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mauldevrinz/TUGAS-SPS-NO.2-KELAS-3B
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

## Contributions
Feel free to fork this repository and submit pull requests. Suggestions and improvements are welcome!

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
