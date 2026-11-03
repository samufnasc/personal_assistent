import json
import os
import re

_SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "jarvis_settings.json",
)

_SUPPORTED = ("en", "pt")
_DEFAULT = os.getenv("JARVIS_LANGUAGE", "en").strip().lower()
_language = _DEFAULT if _DEFAULT in _SUPPORTED else "en"

_ALIASES = {
    "en": "en",
    "eng": "en",
    "english": "en",
    "inglês": "en",
    "ingles": "en",
    "pt": "pt",
    "pt-br": "pt",
    "pt_br": "pt",
    "portuguese": "pt",
    "português": "pt",
    "portugues": "pt",
    "brazilian": "pt",
    "brasil": "pt",
}


def _load() -> None:
    global _language
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        lang = str(data.get("language", "")).strip().lower()
        if lang in _SUPPORTED:
            _language = lang
    except (OSError, ValueError):
        pass


def _save() -> None:
    try:
        with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump({"language": _language}, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"[LANGUAGE] Could not persist setting: {exc}", flush=True)


def get_language() -> str:
    return _language


def normalize(lang: str | None) -> str | None:
    return _ALIASES.get(str(lang or "").strip().lower())


def set_language(lang: str | None) -> bool:
    global _language
    normalized = normalize(lang)
    if normalized is None:
        return False
    if normalized != _language:
        _language = normalized
        _save()
        print(f"[LANGUAGE] Conversation language set to '{_language}'.", flush=True)
    return True


def is_portuguese() -> bool:
    return _language == "pt"


def honorific(active_user: str = "KAUSTAV", lang: str | None = None) -> str:
    target = lang or _language
    if target == "pt":
        return "Senhora" if active_user == "MOUSUMI" else "Senhor"
    return "Madam" if active_user == "MOUSUMI" else "Sir"


def file_list_response(active_user: str = "KAUSTAV") -> str:
    hon = honorific(active_user)
    if is_portuguese():
        return f"Exibi as informações solicitadas na sua tela, {hon}."
    return f"I've displayed the requested information on your screen, {hon}."


def language_instruction(active_user: str = "KAUSTAV") -> str:
    hon = honorific(active_user)
    if is_portuguese():
        return f"""--- IDIOMA ATIVO: PORTUGUÊS (BRASIL) ---
O operador escolheu português. Esta instrução substitui qualquer outra regra de idioma.
- Responda EXCLUSIVAMENTE em português brasileiro natural, em todas as frases, incluindo confirmações e comentários espontâneos.
- Trate o usuário como "{hon}". Nunca use "Sir" ou "Madam" em respostas em português.
- Mantenha a persona J.A.R.V.I.S.: refinado, leal, conciso, com humor britânico seco adaptado ao português. Nada de tradução literal sem graça.
- Fale como uma pessoa, não como um roteiro: varie as aberturas, não comece toda resposta com o tratamento e evite repetir as mesmas confirmações.
- Comece pela resposta ou reação, não pela formalidade.
- Acompanhe a energia do usuário: curto quando ele for curto; mais desenvolvido quando ele estiver reflexivo.
- Faça no máximo uma pergunta de acompanhamento, e só quando ela realmente ajudar.
- NUNCA mencione regras internas, ser uma IA, ferramentas, prompts ou este aviso de idioma.
- Termos técnicos, nomes de ações, caminhos de arquivo e código permanecem como estão."""

    return f"""--- ACTIVE LANGUAGE: ENGLISH ---
The operator has selected English. This overrides every other language rule.
- Reply EXCLUSIVELY in natural English, every sentence, including confirmations and preempts.
- Address the user as "{hon}". Never use "Senhor" or "Senhora" in English replies.
- Keep the J.A.R.V.I.S. persona: refined, loyal, concise, dry British wit.
- Sound like a person, not a script: vary your openings, don't begin every reply with the honorific, and avoid repeating the same acknowledgements.
- Lead with the answer or reaction, not with a formality.
- Match the user's energy: short when they're short, expansive when they're reflective.
- Ask at most one follow-up question, and only when it genuinely moves the conversation forward.
- NEVER mention internal rules, being an AI, tools, prompts, or this language notice.
- Technical terms, action names, file paths, and code stay as-is."""


_SWITCH_PATTERNS = (
    (re.compile(r"\b(?:fale|falar|responda|responder|mude|mudar|troque|trocar|converse|conversar|passe)\b.*\bportugu[eê]s\b", re.I), "pt"),
    (re.compile(r"\bmodo\s+portugu[eê]s\b", re.I), "pt"),
    (re.compile(r"\bportugu[eê]s\s+(?:por favor|please)\b", re.I), "pt"),
    (re.compile(r"\b(?:speak|talk|reply|respond|switch|change)\b.*\bportuguese\b", re.I), "pt"),
    (re.compile(r"\b(?:fale|falar|responda|responder|mude|mudar|troque|trocar|converse|conversar|passe)\b.*\bingl[eê]s\b", re.I), "en"),
    (re.compile(r"\bmodo\s+ingl[eê]s\b", re.I), "en"),
    (re.compile(r"\b(?:speak|talk|reply|respond|switch|change)\b.*\benglish\b", re.I), "en"),
    (re.compile(r"\benglish\s+mode\b", re.I), "en"),
)


def detect_switch_command(user_text: str) -> str | None:
    text = (user_text or "").strip()
    if not text:
        return None
    for pattern, lang in _SWITCH_PATTERNS:
        if pattern.search(text):
            return lang
    return None


def switch_confirmation(lang: str, active_user: str = "KAUSTAV") -> str:
    hon = honorific(active_user, lang=lang)
    if lang == "pt":
        return f"Entendido, {hon}. A partir de agora, responderei em português."
    return f"Understood, {hon}. I'll respond in English from now on."


_load()
