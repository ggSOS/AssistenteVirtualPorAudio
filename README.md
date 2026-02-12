# Assistente Virtual por Voz (Whisper + ChatGPT + TTS)

Assistente virtual por voz em Python que:

* 🎤 grava áudio do microfone
* 🧠 converte fala em texto (Whisper)
* 🤖 processa com ChatGPT
* 🔊 responde em áudio (Text-to-Speech)

Fluxo:

```
Speech -> Whisper -> ChatGPT -> gTTS -> Audio
```

---

## Funcionalidades

* Gravação de áudio via microfone
* Reconhecimento de fala com Whisper
* Processamento de linguagem natural com ChatGPT
* Resposta falada via Google TTS
* Opção de usar áudio existente
* Menu interativo no terminal

---

## Arquitetura

```
input.wav
   ↓
Whisper (Speech-to-Text)
   ↓
ChatGPT API
   ↓
gTTS (Text-to-Speech)
   ↓
output.mp3
```

---

## Requisitos

* Python 3.10+
* ffmpeg instalado
* Microfone funcionando
* Conexão com internet

---

## Instalação

### 1.Clonar projeto

```bash
git clone <repo>
cd projeto
```

---

### 2.Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### 3.Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4.Instalar ffmpeg

Site oficial do [ffmpeg](https://www.ffmpeg.org/download.html)

Testar:

```bash
ffmpeg -version
```

---

### 5.Configurar chave OpenAI

Linux/Mac:

```bash
export OPENAI_API_KEY="sua-chave"
```

Windows:

```powershell
setx OPENAI_API_KEY "sua-chave"
```

---

## Execução

```bash
python main.py
```

---

## Menu

```
0 - Finalizar programa
1 - Gravar novo áudio
2 - Utilizar áudio existente
```

---

## Configurações editáveis

No topo do `main.py`:

```python
duration = 7              # segundos de gravação
language = "pt"           # idioma
model_type = "small"      # whisper model
```

Modelos Whisper:

```
tiny | base | small | medium | large
```

---

## Modelos utilizados

* Whisper — Speech Recognition
* GPT-4o-mini — NLP
* gTTS — Text-to-Speech

---

## Avisos importantes

* Whisper pode errar com áudio ruidoso
* gTTS requer internet
* Modelos maiores usam mais RAM
* Respostas longas podem falhar no TTS

---

# Licença

Projeto educacional.