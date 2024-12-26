import pyttsx3

# Inisialisasi TTS engine
engine = pyttsx3.init()

# Dapatkan daftar suara
voices = engine.getProperty("voices")

# Cetak informasi tentang suara
print("Daftar suara yang tersedia:")
for index, voice in enumerate(voices):
    print(f"Voice {index}:")
    print(f" - ID: {voice.id}")
    print(f" - Name: {voice.name}")
    print(f" - Languages: {voice.languages}")
    print(f" - Gender: {voice.gender}")
    print(f" - Age: {voice.age}")
