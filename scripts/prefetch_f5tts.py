#!/usr/bin/env python3
"""Download the default F5-TTS and Vocos assets into Hugging Face cache."""

from cached_path import cached_path
from huggingface_hub import hf_hub_download


def main() -> None:
    print("Downloading Vocos config...")
    print(hf_hub_download(repo_id="charactr/vocos-mel-24khz", filename="config.yaml"))
    print("Downloading Vocos weights...")
    print(hf_hub_download(repo_id="charactr/vocos-mel-24khz", filename="pytorch_model.bin"))
    print("Downloading F5TTS_v1_Base checkpoint...")
    print(cached_path("hf://SWivid/F5-TTS/F5TTS_v1_Base/model_1250000.safetensors"))
    print("F5-TTS model files cached.")


if __name__ == "__main__":
    main()
