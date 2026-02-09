import whisper

audio_filename = "input"

model = whisper.load_model("tiny")
result = model.transcribe(audio_filename)
print(f"\n{result["text"]}")