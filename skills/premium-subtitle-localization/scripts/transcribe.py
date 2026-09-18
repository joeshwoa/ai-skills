#!/usr/bin/env python3
"""
transcribe.py — generate a source-language SRT from a video's audio, when
no existing subtitle file was found (see find_subtitles.py / SKILL.md
Step 1).

Uses faster-whisper (CTranslate2-based, CPU-friendly, runs fully local —
no API key, no audio leaves the machine). Two steps:
  1. ffmpeg extracts a 16kHz mono WAV (what Whisper models expect).
  2. faster-whisper transcribes it into cues, written straight to SRT.

Usage:
    python3 transcribe.py movie.mp4 out_source.srt \
        --lang ar --model small

Model size vs. quality/speed tradeoff (CPU):
    tiny/base  — fast, rough — only for a quick draft or very clean audio
    small      — good default for most content, minutes not hours on CPU
    medium     — noticeably better on accents/noisy audio, much slower on CPU
    large-v3   — best quality, CPU time can exceed the movie's own runtime

--lang is the source language hint (e.g. "ar"). Omit it to let Whisper
auto-detect — cheaper to just say it if you already know, detection can
mis-fire on movies that mix dialects/languages (code-switching, songs).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import os

from srt_utils import Cue, write_srt


def extract_audio(video_path: str, wav_path: str) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le",
        wav_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg audio extraction failed:\n{result.stderr[-2000:]}")


def transcribe_to_cues(wav_path: str, lang: str | None, model_size: str) -> list[Cue]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise SystemExit(
            "faster-whisper is not installed. Install it first:\n"
            "  pip install --break-system-packages -r requirements.txt\n"
            f"(original import error: {e})"
        )

    # CPU int8 is the practical default outside a CUDA box — adjust
    # compute_type to "float16"/"int8_float16" if a GPU is actually present.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        wav_path,
        language=lang,
        vad_filter=True,           # drop long silences instead of hallucinating text
        word_timestamps=False,
    )

    cues = []
    for i, seg in enumerate(segments, start=1):
        text = seg.text.strip()
        if not text:
            continue
        cues.append(Cue(
            index=i,
            start_ms=int(seg.start * 1000),
            end_ms=int(seg.end * 1000),
            text=text,
        ))
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})", file=sys.stderr)
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_path")
    ap.add_argument("out_srt")
    ap.add_argument("--lang", default=None, help="source language hint, e.g. ar (omit to auto-detect)")
    ap.add_argument("--model", default="small", help="tiny|base|small|medium|large-v3")
    ap.add_argument("--keep-wav", help="optional path to also save the extracted WAV")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = args.keep_wav or os.path.join(tmp, "audio.wav")
        print(f"Extracting audio -> {wav_path} ...")
        extract_audio(args.video_path, wav_path)

        print(f"Transcribing with faster-whisper ({args.model}, lang={args.lang or 'auto'}) ...")
        cues = transcribe_to_cues(wav_path, args.lang, args.model)

    if not cues:
        raise SystemExit("Transcription produced zero cues — check the audio track/language hint.")

    write_srt(cues, args.out_srt)
    print(f"{len(cues)} cues -> {args.out_srt}")
    print(
        "Read through a sample before trusting it for translation — ASR makes "
        "mistakes on names, slang, and overlapping dialogue; fix those in the "
        "source SRT before translating, or they carry into every language."
    )


if __name__ == "__main__":
    main()
