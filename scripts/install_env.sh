#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3.11}"
VENV_DIR="${VENV_DIR:-.venv-f5-tts}"
INSTALL_F5TTS="${INSTALL_F5TTS:-1}"
PREFETCH_MODELS="${PREFETCH_MODELS:-0}"

log() {
  printf '%s\n' "$*"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

if [[ "$(uname -s)" != "Darwin" ]]; then
  log "This installer targets macOS. Install Python >=3.10, Node, FFmpeg, torch, torchaudio, and f5-tts manually on this OS."
  exit 2
fi

if ! need_cmd brew; then
  log "Homebrew is required: https://brew.sh"
  exit 2
fi

log "Installing/checking Homebrew dependencies..."
HOMEBREW_NO_AUTO_UPDATE="${HOMEBREW_NO_AUTO_UPDATE:-1}" brew install python@3.11 ffmpeg node

if ! need_cmd node; then
  log "node was not found after Homebrew install."
  exit 3
fi

if ! need_cmd ffmpeg || ! need_cmd ffprobe; then
  log "ffmpeg/ffprobe was not found after Homebrew install."
  exit 3
fi

if [[ "$INSTALL_F5TTS" == "1" ]]; then
  if [[ ! -x "$PYTHON_BIN" ]]; then
    log "Python 3.11 not found at $PYTHON_BIN"
    exit 3
  fi

  if [[ ! -d "$VENV_DIR" ]]; then
    log "Creating F5-TTS venv at $VENV_DIR..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
  fi

  # shellcheck source=/dev/null
  source "$VENV_DIR/bin/activate"
  python -m pip install --upgrade pip setuptools wheel
  pip install torch torchaudio f5-tts

  f5-tts_infer-cli --help >/dev/null
  log "F5-TTS CLI is available."

  if [[ "$PREFETCH_MODELS" == "1" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    python "$SCRIPT_DIR/prefetch_f5tts.py"
  fi
fi

log "Environment ready."
