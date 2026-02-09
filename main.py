import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
import os
import whisper


allowed_extensions = [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm", ".flac", ".oga", ".ogg"]
sr = 44100 ## frequencia em Hz
duration = 5 ## segundos
new_audio_filename = "input.wav"
existing_audio_file = False
audio_filename=""
main_options_model = {
    "0": "Finalizar programa",
    "1": "Gravar novo áudio",
    "2": "Utizar áudio já existente"
}
main_options={}


def audio_file_check():
    existing_audio_file = False
    audio_filename = ""

    for file in os.listdir():
        if  os.path.isfile(file)  and  Path(file).stem=="input"  and  Path(file).suffix.lower() in allowed_extensions  and  os.path.getsize(file)<25*1024*1024 :
            audio_filename = file
            existing_audio_file = True
            break
        else:
            continue
    
    return existing_audio_file, audio_filename


while True:    
    ## Criar opcoes
    existing_audio_file, audio_filename = audio_file_check()
    if existing_audio_file:
        main_options = main_options_model.copy()
    else:
        main_options = main_options_model.copy()
        del main_options["2"]


    ## Permitir usuario selecionar opcao
    print("\nOpções: ")
    for key, value in main_options.items():
        print(f"{key} - {value}")
    resposta = input("\t> ")
    while resposta not in main_options.keys():
        print(f"\n{resposta} não é uma opção válida!")
        print("\nOpções: ")
        for key, value in main_options.items():
            print(f"{key} - {value}")
        resposta = input("\t> ")


    ## Processar opcao
    if resposta == "0":
        break
    elif resposta == "1":
        existing_audio_file, audio_filename = audio_file_check()
        while existing_audio_file:
            os.remove(audio_filename)
            existing_audio_file, audio_filename = audio_file_check()

        audio_filename = new_audio_filename
        print("\n>Gravando...")
        audio_recorded = sd.rec(int(duration * sr), samplerate=sr, channels=2)
        sd.wait()
        print(">Gravação finalizada")
        write(audio_filename, sr, audio_recorded)
    else:
        existing_audio_file, audio_filename = audio_file_check()
        if not existing_audio_file:
            print("\nGravação excluída ou alterada.\nEscolha novamente sua opção!")
            continue
    

    ## Transcrever gravacao desejada
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_filename)
    print(f"\n{result["text"]}")


# todo voice to text
# todo processar text
# todo text to voice