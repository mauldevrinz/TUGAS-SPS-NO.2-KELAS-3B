import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
    QTextEdit, QLabel
)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sounddevice as sd
import queue
import soundfile as sf
import pyttsx3
from googletrans import Translator
import speech_recognition as sr
from datetime import datetime
import mysql.connector
import requests
from scipy.signal import butter, lfilter
import noisereduce as nr

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024


import numpy as np
from scipy.signal import butter, lfilter

class RealTimePlot(QWidget):
    def __init__(self, title, xlabel, ylabel):
        super().__init__()
        self.figure = Figure(figsize=(3, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.grid()

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def band_pass_filter(self, data, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    def update_plot(self, x_data, y_data):
        filtered_y_data = self.band_pass_filter(y_data, lowcut=300, highcut=3000, fs=44100, order=5)
        self.ax.clear()
        self.ax.plot(x_data, filtered_y_data, color='blue')
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.canvas.draw()

def record_and_process_audio(duration=5):
    print("Recording...")
    audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")

    # Reduce noise
    noise_reduced_audio = nr.reduce_noise(y=audio.flatten(), sr=44100)
    return noise_reduced_audio

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Noise Reduction")
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = RealTimePlot("Audio Signal", "Time (s)", "Amplitude")
        self.setCentralWidget(self.plot_widget)

        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.plot_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_recording(self):
        audio_data = record_and_process_audio()
        time_axis = np.linspace(0, len(audio_data) / 44100, num=len(audio_data))
        self.plot_widget.update_plot(time_axis, audio_data)

class TTSWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, tts_engine, text):
        super().__init__()
        self.tts_engine = tts_engine
        self.text = text

    def run(self):
        self.tts_engine.say(self.text)
        self.tts_engine.runAndWait()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANDIK, REY, MAULVIN")
        self.setGeometry(100, 100, 900, 700)

        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.audio_data = []
        self.stream = None

        self.translator = Translator()
        self.tts_engine = pyttsx3.init()
        self.configure_tts()

        self.main_layout = QVBoxLayout()
        self.label = QLabel("LIVE RECORDING - KELOMPOK 1 3B", self)
        self.label.setFont(QFont("Bahnschrift Condensed", 25))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Text box untuk nama pengisi suara dipindahkan ke atas tombol start
        self.name_text_box = QTextEdit()
        self.name_text_box.setPlaceholderText("Masukkan nama pengisi suara...")
        self.name_text_box.setFixedHeight(30)
        self.main_layout.addWidget(self.name_text_box)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.stop_button)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_audio)
        button_layout.addWidget(self.play_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        button_layout.addWidget(self.reset_button)

        self.translate_button = QPushButton("Generate Translation")
        self.translate_button.clicked.connect(self.generate_translation)
        button_layout.addWidget(self.translate_button)

        self.main_layout.addLayout(button_layout)

        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Audio-to-text transcription will appear here...")
        self.text_box.setFixedHeight(60)
        self.text_box.setReadOnly(True)
        self.main_layout.addWidget(self.text_box)

        self.upload_button = QPushButton("Upload Data")
        self.upload_button.clicked.connect(self.upload_data)
        self.main_layout.addWidget(self.upload_button)

        self.time_plot = RealTimePlot("Realtime Graphic Recording", "Time (s)", "Amplitude")
        self.freq_plot = RealTimePlot("Discrete Fourier Transform", "Frequency (Hz)", "Amplitude")
        self.main_layout.addWidget(self.time_plot)
        self.main_layout.addWidget(self.freq_plot)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        self.tts_thread = None

        # Database connection
        self.db_connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Ganti dengan password MySQL Anda
                database="sps_suara"
            )
            return conn
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def configure_tts(self):
        self.tts_engine.setProperty("rate", 100)
        voices = self.tts_engine.getProperty("voices")
        for voice in voices:
            if "zira" in voice.name.lower():
                self.tts_engine.setProperty("voice", voice.id)
                break

    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.audio_queue.put(indata.copy())
            self.audio_data.append(indata.copy())

    def start_recording(self):
        self.is_recording = True
        self.audio_data = []
        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=self.audio_callback)
        self.stream.start()
        self.timer.start(50)

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.timer.stop()

    def play_audio(self):
        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0).flatten()
            sd.play(audio, samplerate=SAMPLE_RATE)

    def reset(self):
        self.audio_data = []
        self.time_plot.update_plot([], [])
        self.freq_plot.update_plot([], [])
        self.text_box.clear()

    def update_plots(self):
        if not self.audio_queue.empty():
            audio_chunk = self.audio_queue.get()
            audio = np.concatenate(self.audio_data, axis=0).flatten()

            time_axis = np.linspace(0, len(audio) / SAMPLE_RATE, num=len(audio))
            self.time_plot.update_plot(time_axis, audio)

            freq_axis = np.fft.rfftfreq(len(audio), d=1 / SAMPLE_RATE)
            fft_data = np.abs(np.fft.rfft(audio))

            self.freq_plot.update_plot(freq_axis, fft_data)

    def audio_to_text(self):
        if not self.audio_data:
            return "No audio data available"
        audio = np.concatenate(self.audio_data, axis=0).flatten()
        temp_audio_file = "temp_audio.wav"
        sf.write(temp_audio_file, audio, samplerate=SAMPLE_RATE)

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="id-ID")
            except sr.UnknownValueError:
                return "Speech not understood"
            except sr.RequestError as e:
                return f"API error: {e}"

    def generate_translation(self):
        if not self.audio_data:
            self.text_box.setText("No audio recorded.")
            return

        input_text = self.audio_to_text()
        if not input_text:
            self.text_box.setText("Audio-to-text conversion failed.")
            return

        self.text_box.setText(f"Original Text: {input_text}")
        translated_text = self.translator.translate(input_text, src="id", dest="en").text
        self.text_box.append(f"\nTranslated Text: {translated_text}")

        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.stop()
        self.tts_thread = TTSWorker(self.tts_engine, translated_text)
        self.tts_thread.start()

    def save_audio_to_file(self):
        if not self.audio_data:
            return None
        audio = np.concatenate(self.audio_data, axis=0).flatten()
        voice_actor_name = self.name_text_box.toPlainText().strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fileNameAudio = f"{voice_actor_name}_{timestamp}"
        file_path = f"C:/xampp/htdocs/sps_suara/AUDIO RECORDER/{fileNameAudio}.wav"
        sf.write(file_path, audio, samplerate=SAMPLE_RATE)
        return fileNameAudio

    def save_plots_to_file(self):
        voice_actor_name = self.name_text_box.toPlainText().strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fileNameTime = f"{voice_actor_name}_realtime_{timestamp}"
        fileNameFreq = f"{voice_actor_name}_dft_plot_{timestamp}"
        time_plot_file = f"C:/xampp/htdocs/sps_suara/REALTIME GRAFIK/{fileNameTime}.png"
        freq_plot_file = f"C:/xampp/htdocs/sps_suara/DFT GRAFIK/{fileNameFreq}.png"

        self.time_plot.figure.savefig(time_plot_file)
        self.freq_plot.figure.savefig(freq_plot_file)
        return fileNameTime, fileNameFreq
    
    def upload_to_edge_impulse(self, file_path, actor_name):
        # Set up Edge Impulse API endpoint and credentials
        edge_impulse_api_url = f"https://ingestion.edgeimpulse.com/api/training/files"
        edge_impulse_api_key = "ei_421e656d55f0c773d760d62da1160a9203e891b38653b4ba"  # Replace with your Edge Impulse API key

        # Prepare the data to send
        with open(file_path, 'rb') as f:
            audio_data = f.read()

        # Create filename with actor's name and timestamp
        actor_name = self.name_text_box.toPlainText().strip()  # Actor name from the UI
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Current timestamp in the desired format
        filename = f"{actor_name}.wav"  # Filename format: actor_name_timestamp.wav

    # Prepare files and headers
        files = {
            'data': (filename, audio_data, 'audio/wav'),  # Using the separated filename
        }
        headers = {
            'x-api-key': edge_impulse_api_key
        }
        data = {
            'label': actor_name,  # Label set to actor's name
        }

        try:
            response = requests.post(edge_impulse_api_url, files=files, headers=headers, data=data)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            self.text_box.append(f"Data berhasil diunggah ke Edge Impulse dengan sampling name: {filename}.")
        except requests.exceptions.RequestException as e:
            self.text_box.append(f"Error uploading to Edge Impulse: {e}")


    def upload_data_to_database(self, voice_actor_name, audio_file, time_plot_file, freq_plot_file):
        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO uploads (tanggal, nama, voice_recording, realtime_grafik, dft_grafik) VALUES (%s, %s, %s, %s, %s)",
                    (current_time, voice_actor_name, audio_file, time_plot_file, freq_plot_file)
                )
                self.db_connection.commit()
                self.text_box.setText(f"Data berhasil diunggah ke database pada {current_time}.")
            except mysql.connector.Error as e:
                self.text_box.setText(f"Error uploading data: {e}")
        else:
            self.text_box.setText("Tidak terhubung ke database.")

    def upload_data(self):
        voice_actor_name = self.name_text_box.toPlainText().strip()
        if not voice_actor_name:
            self.text_box.setText("Please enter a voice actor's name.")
            return

        # Save the audio file
        fileNameAudio = self.save_audio_to_file()
        if not fileNameAudio:
            self.text_box.setText("No audio recorded to upload.")
            return

        # Save the plots
        fileNameTime, fileNameFreq = self.save_plots_to_file()

        # Upload to MySQL Database
        self.upload_data_to_database(voice_actor_name, fileNameAudio, fileNameTime, fileNameFreq)

        # Upload to Edge Impulse (send the audio file)
        audio_file_path = f"C:/xampp/htdocs/sps_suara/AUDIO RECORDER/{fileNameAudio}.wav"
        self.upload_to_edge_impulse(audio_file_path, voice_actor_name)  # Pass actor name as the label


    def closeEvent(self, event):
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.stop()
        if self.db_connection:
            self.db_connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())