print(">Carregando modelos de IA...")
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
import os
import whisper
from openai import OpenAI
from gtts import gTTS
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


## duracao em segundos da gravacao
duration = 7
## linguagem da conversa
language = "pt"
## tipo(qualidade - tiny/base/small/medium/turbo/large) da IA de Speech to Text
model_type = "small"
## chave de API da OpenAI
client = OpenAI(api_key="insira_aqui_sua_chave_de_api")


allowed_extensions = [".mp3", ".mp4", ".m4a", ".wav", ".flac", ".ogg"]
sr = 44100
new_audio_filename = "input.wav"
existing_audio_file = False
audio_filename=""
output_filename = "output.mp3"
main_options_model = {
    "0": "Finalizar programa",
    "1": "Gravar novo áudio",
    "2": "Utizar áudio já existente"
}
main_options={}
model = whisper.load_model(model_type)


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
        print(f">Gravação finalizada({audio_filename})")
        write(audio_filename, sr, audio_recorded)
    else:
        existing_audio_file, audio_filename = audio_file_check()
        if not existing_audio_file:
            print("\nGravação excluída ou alterada.\nEscolha novamente sua opção!")
            continue
    

    ## Speech to Text
    print("\n>Convertendo Fala para Texto...")
    result = model.transcribe(audio_filename,
                              language=language,
                              temperature=0,
                              best_of=5,
                              beam_size=5)
    print(f">Input: {result["text"]}")


    ## GPT processa texto de input
    print("\n>Consultando ChatGPT...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": result["text"]}
        ],
        max_tokens=200,
        temperature=0.7
    )
    print(f">Resposta do ChatGPT: {response.choices[0].message.content}")  


    ## Text to Speech
    print("\n>Convertendo Texto em Fala...")
    tts = gTTS(text=response.choices[0].message.content, lang=language, tld='com.br', slow=False)
    tts.save(output_filename)
    print(f">Conversão finalizada({output_filename})")