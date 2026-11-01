# Histórico de Desenvolvimento — J.A.R.V.I.S Local

Este documento registra todos os passos, configurações e correções realizadas para configurar e executar com sucesso o assistente de voz local **J.A.R.V.I.S_Local** dentro do projeto.

---

## 📅 Resumo das Etapas Realizadas

### 1. Clonagem e Estruturação do Projeto
* **Ação:** Criação da pasta `J.A.R.V.I.S_Local` no repositório local.
* **Repositório Base:** `https://github.com/kaustav991a/J.A.R.V.I.S`
* **Estrutura obtida:** 
  * `jarvis-backend/` (Servidor Python / FastAPI / WebSockets / IA / Visão / Daemons)
  * `jarvis-frontend/` (Interface visual HUD em React / Vite)

### 2. Configuração do Ambiente Python & Dependências (Backend)
* **Ambiente Virtual:** Criação de venv (`python -m venv venv`) utilizando Python 3.12.
* **Ajustes de Dependências:**
  * Remoção/comentamento de pacotes incompatíveis com Python 3.12 (`audioop-lts`).
  * Ajustes nas versões do PyTorch e `protobuf` para evitar conflitos com pacotes Google AI.
  * Criação de `requirements-core.txt` e instalação dos pacotes essenciais (`fastapi`, `uvicorn`, `websockets`, `pydantic`, `groq`, `requests`, `aiofiles`, `aiogram`, `colorama`, `rich`, `psutil`, `pyaudio`, `pyautogui`, `pyperclip`, `pyyaml`).
* **Instalação de Módulos Runtime Faltantes:**
  * `playwright` (+ instalação dos binários de navegadores via `playwright install`)
  * `zeroconf`
  * `SpeechRecognition`
  * `opencv-python` (`cv2`)
  * `deepface`
  * `werkzeug`

### 3. Configuração do Frontend (HUD)
* **Ação:** Acesso à pasta `jarvis-frontend/` e execução de `npm install` para instalar as dependências do React e Vite.

### 4. Configuração de Credenciais
* **Chave Groq:** Cópia e configuração da chave da API do Groq obtida em `API_groq.txt` para o arquivo `.env` localizado em `J.A.R.V.I.S_Local/jarvis-backend/.env`.

### 5. Execução e Validação
* **Backend:** Iniciado com sucesso via Uvicorn na porta `8000` (`http://127.0.0.1:8000`).
* **Frontend:** Iniciado com sucesso via Vite na porta `5173` (`http://localhost:5173`).
* **Validação:** Acessado o HUD no navegador e testada a comunicação entre cliente e servidor.

---
*Gerado em: 31 de outubro de 2026*
