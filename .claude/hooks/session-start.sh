#!/bin/bash
# Prepara as skills /watch e /insta (análise de vídeos) nas sessões do Claude Code na nuvem.
# Idempotente: nas sessões seguintes só confere o que já está instalado.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

SKILLS="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/skills"
aviso() { echo "[session-start] $*" >&2; }

# ffmpeg/ffprobe: quadros e áudio dos vídeos.
if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get install -y -qq --no-install-recommends ffmpeg >/dev/null 2>&1 \
    || { apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq --no-install-recommends ffmpeg >/dev/null 2>&1; } \
    || aviso "não consegui instalar o ffmpeg"
fi

# yt-dlp atualizado (o Instagram quebra versões antigas); no máximo uma vez por dia.
CARIMBO="$HOME/.cache/session-start/yt-dlp"
if ! command -v yt-dlp >/dev/null 2>&1 || [ -z "$(find "$CARIMBO" -mtime -1 2>/dev/null)" ]; then
  if python3 -m pip install --quiet --disable-pip-version-check --upgrade --user yt-dlp >/dev/null 2>&1; then
    mkdir -p "$(dirname "$CARIMBO")" && touch "$CARIMBO"
  else
    aviso "não consegui instalar/atualizar o yt-dlp"
  fi
fi

# O proxy deste ambiente usa a CA do sistema (SSL_CERT_FILE); o certifi do yt-dlp não a conhece.
mkdir -p "$HOME/.config/yt-dlp"
if [ ! -f "$HOME/.config/yt-dlp/config" ]; then
  echo "--compat-options no-certifi" > "$HOME/.config/yt-dlp/config"
fi

# Cookies do Instagram (opcional): segredo INSTAGRAM_COOKIES_B64 = cookies.txt em base64.
if [ -n "${INSTAGRAM_COOKIES_B64:-}" ]; then
  mkdir -p "$HOME/.config/insta" && chmod 700 "$HOME/.config/insta"
  COOKIES="$HOME/.config/insta/cookies.txt"
  if (umask 077 && printf '%s' "$INSTAGRAM_COOKIES_B64" | base64 -d > "$COOKIES" 2>/dev/null); then
    if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
      echo "export INSTAGRAM_COOKIES_FILE=\"$COOKIES\"" >> "$CLAUDE_ENV_FILE"
      echo "export WATCH_COOKIES_FILE=\"$COOKIES\"" >> "$CLAUDE_ENV_FILE"
    fi
  else
    rm -f "$COOKIES"
    aviso "INSTAGRAM_COOKIES_B64 não é um base64 válido"
  fi
fi

# Chave do Gemini nas "Credenciales de API" do ambiente: o proxy injeta o cabeçalho
# x-goog-api-key; a sessão só precisa saber que o motor Gemini está disponível.
if [ -z "${GEMINI_API_KEY:-}" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export GEMINI_API_KEY="proxy-injected"' >> "$CLAUDE_ENV_FILE"
  export GEMINI_API_KEY="proxy-injected"
fi

# /watch sem o assistente de primeira execução: Gemini se houver GEMINI_API_KEY,
# senão quadros + transcrição (Groq/OpenAI se houver chave).
if [ -f "$SKILLS/watch/scripts/setup.py" ]; then
  python3 "$SKILLS/watch/scripts/setup.py" --engine auto --backend auto >/dev/null 2>&1 \
    || aviso "não consegui configurar a skill /watch"
fi
