
# Voice Recorder and Translator with AI Training

## Authors
1. Andik Putra Nazwana (2042231010)  
2. Andre Mahesa Bagaskara (2042231012)  
3. Akhmad Maulvin Nazir Zakaria (2042231028)  
4. Dwi Oktavianto Wahyu Nugroho (Supervisor)  

Teknik Instrumentasi - Institut Teknologi Sepuluh Nopember  

---

## Features

1. **Voice Recording**: Record audio input using a simple and intuitive GUI.
2. **Automatic Translation**: Translate recorded audio into a target language.
3. **Database Upload**: Store recorded and translated data into a MySQL database.
4. **Edge Impulse Integration**: Upload audio data to Edge Impulse for training deep learning models.
5. **Real-time Plotting**: Visualize real-time audio signal and its frequency spectrum.
6. **Noise Reduction**: Enhance audio quality by reducing background noise.
7. **Text-to-Speech (TTS)**: Convert translated text to speech output.

---

## Requirements

### Software
- Python 3.8+
- PyQt6
- MySQL Server
- Edge Impulse CLI

### Hardware
- Microphone
-  DevKit (optional for AI integration)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mauldevrinz/TUGAS-SPS-NO.2-KELAS-3B
cd TUGAS-SPS-NO.2-KELAS-3B
```

### 2. Install Python Dependencies
```bash
pip install PyQt6 numpy matplotlib sounddevice soundfile pyttsx3 googletrans==4.0.0-rc1 speechrecognition mysql-connector-python noisereduce
```

### 3. Set Up MySQL Database

Create a MySQL database and table to store the recordings and translations:
```sql
CREATE DATABASE sps_suara;
USE sps_suara;

CREATE TABLE uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
    nama VARCHAR(255),
    voice_recording VARCHAR(255),
    realtime_grafik VARCHAR(255),
    dft_grafik VARCHAR(255)
);
```

### 4. Configure Edge Impulse
Install the Edge Impulse CLI and log in:
```bash
npm install -g edge-impulse-cli
edge-impulse-login
```

---

## Usage

1. **Run the Application**
   ```bash
   python main.py
   ```

2. **Start Recording**
   - Enter the voice actor's name in the provided text box.
   - Click "Start Recording" to begin capturing audio.
   
3. **Stop Recording**
   - Click "Stop Recording" to end the recording session.

4. **View Real-time Plots**
   - Observe the time-domain and frequency-domain representations of the audio signal.

5. **Translate and Convert to Text**
   - Click "Generate Translation" to transcribe and translate the recorded audio.
   - The transcription and translation appear in the text box.

6. **Upload Data**
   - Click "Upload Data" to save audio, plots, and translations to:
     - MySQL database
     - Edge Impulse platform for further AI training.

---

## MAIN GUI
![alt text](https://github.com/mauldevrinz/TUGAS-SPS-NO.2-KELAS-3B/blob/main/GUI.png)

## File Structure

```
TUGAS-SPS-NO.2-KELAS-3B/
|-- main.py               # Main application script
|-- requirements.txt      # List of dependencies
|-- README.md             # Documentation
|-- database.sql          # SQL script for database setup
|-- audio_data/           # Folder for storing audio files
|-- plots/                # Folder for storing generated plots
```

---

## Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, please create an issue or submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.


