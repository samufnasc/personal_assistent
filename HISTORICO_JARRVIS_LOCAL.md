# Histórico de Desenvolvimento — J.A.R.V.I.S Local

Este documento registra todos os passos, configurações e correções realizadas para configurar, testar e evoluir o assistente de voz local **J.A.R.V.I.S_Local**.

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
  * Remoção/comentamento de pacotes incompatíveis com Python 3.12.
  * Instalação de pacotes essenciais (`fastapi`, `uvicorn`, `websockets`, `pydantic`, `groq`, `requests`, `google-generativeai`, etc.).

### 3. Configuração do Frontend (HUD) e Terminal de Comandos
* **Correção de Entrada de Texto:** Ajustado o terminal de comandos do HUD para que pressionar a tecla `Enter` ou clicar em `EXECUTE` envie instantaneamente o comando, atualize o painel de chat (`Comm Transcript`) e exiba o feedback em tempo real.
* **Controle de Microfone:** Adicionado o botão `MIC` na barra de ferramentas do terminal para acionar a escuta por voz sob demanda (`START_LISTENING`).

### 4. Roteamento de IA & Cadeia de Fallback (Multi-Provider)
* **Ordem de Fallback Configurada em `llm_router.py`:**
  1. **`gemini-3.5-flash-lite`** (Primeira IA de consulta / nuvem primária)
  2. **Groq** (`openai/gpt-oss-120b` / `llama-3.3-70b-versatile`)
  3. **Ollama Local** (`llama3:8b`)
* **Correções de Robustez:** Ajustado `_split_messages_for_gemini` para evitar `TypeError: contents must not be empty` quando mensagens de sistema estivessem presentes sem turns de usuário.

### 5. Palavras de Despertar (Wake Words) Expandidas
* Adicionadas novas frases de ativação em `wakeword.py`:
  * `'Hello Jarvis'`
  * `'Hey Jarvis'`
  * `'It\'s time to project Jarvis'`

### 6. Autenticação e Reconhecimento de Voz (Samuel)
* **Correção de Biometria por Voz:** Quando a câmera/vídeo IP está inacessível no boot, o JARVIS solicita a identificação por voz. Adicionada a identificação para **Samuel** e **Sam** (`kaustav_aliases` em `main.py`), garantindo acesso administrativo imediato ("Sir").

---

## 🚀 Próximos Passos & O Que Pode Ser Melhorado
1. **Integrações de Clima e Sensores:** Configurar a chave de API da OpenWeatherMap no arquivo `.env` para eliminar o erro 401 de clima no widget de sensores.
2. **Câmera IP / Visão Computacional:** Conectar uma webcam ou stream IP compatível para habilitar o reconhecimento facial automático no boot (evitando o fallback de voz).
3. **APIs do Google (Gmail / Calendar / Fit):** Configurar o arquivo `credentials.json` do Google OAuth para habilitar os agentes de calendário e e-mail.
4. **Otimização do Ollama:** Iniciar o serviço local do Ollama (`ollama serve`) para testes offline completos da camada local de visão (`llava`) e raciocínio.

---
*Atualizado em: 1 de novembro de 2026*
