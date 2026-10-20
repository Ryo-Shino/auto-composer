"""簡易シンセサイザー。

DAWやSoundFontがなくても聴けるように、numpy だけで
メロディ・コード・ドラムを WAV ファイルに書き出す。
（音色はシンプルだが「何が生成されたか」を耳で確認するには十分）
"""
import wave

import numpy as np

SAMPLE_RATE = 44100
BEATS_PER_MEASURE = 4


def _midi_to_freq(note):
    """MIDIノート番号 → 周波数(Hz)。A4(69) = 440Hz。"""
    return 440.0 * 2 ** ((note - 69) / 12)


def _add(buffer, sound, start_sec):
    """buffer の start_sec の位置に sound を足し込む（はみ出した分は切り捨て）。"""
    start = int(start_sec * SAMPLE_RATE)
    end = min(start + len(sound), len(buffer))
    if start < end:
        buffer[start:end] += sound[: end - start]


# =====================
# 音色
# =====================

def _tone(note, duration_sec, harmonics=(1.0, 0.3), attack=0.01, release=0.08):
    """サイン波＋倍音の単純な音。アタックとリリースでプチプチ音を防ぐ。"""
    length = int((duration_sec + release) * SAMPLE_RATE)
    t = np.arange(length) / SAMPLE_RATE
    freq = _midi_to_freq(note)

    wave_data = np.zeros(length)
    for i, amp in enumerate(harmonics, start=1):
        wave_data += amp * np.sin(2 * np.pi * freq * i * t)

    # エンベロープ: 立ち上がり → 保持 → 減衰
    envelope = np.ones(length)
    attack_len = int(attack * SAMPLE_RATE)
    release_len = int(release * SAMPLE_RATE)
    envelope[:attack_len] = np.linspace(0, 1, attack_len)
    envelope[-release_len:] = np.linspace(1, 0, release_len)

    return wave_data * envelope


def _kick():
    t = np.arange(int(0.3 * SAMPLE_RATE)) / SAMPLE_RATE
    # 周波数が 150Hz → 50Hz に素早く下がる（ドスッという音）
    freq = 50 + 100 * np.exp(-t / 0.04)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    return np.sin(phase) * np.exp(-t / 0.12)


def _snare(rng):
    t = np.arange(int(0.2 * SAMPLE_RATE)) / SAMPLE_RATE
    noise = rng.uniform(-1, 1, len(t)) * np.exp(-t / 0.06)
    body = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.08)
    return 0.7 * noise + 0.5 * body


def _hat(rng):
    t = np.arange(int(0.06 * SAMPLE_RATE)) / SAMPLE_RATE
    noise = rng.uniform(-1, 1, len(t))
    noise = np.diff(noise, prepend=0)   # 差分を取ると高音だけ残る
    return noise * np.exp(-t / 0.02)


# =====================
# 書き出し
# =====================

def render_wav(
    melody,
    chords,
    drums,
    path,
    tempo=120,
    export_melody=True,
    export_chords=True,
    export_drums=True,
):
    """メロディ・コード・ドラムを WAV にして保存する。"""
    rng = np.random.default_rng(0)   # ノイズも毎回同じにする（再現性のため）

    beat_sec = 60.0 / tempo
    total_sec = len(chords) * BEATS_PER_MEASURE * beat_sec + 1.0   # +1秒は余韻

    n_samples = int(total_sec * SAMPLE_RATE)
    melody_buf = np.zeros(n_samples)
    chord_buf = np.zeros(n_samples)
    drum_buf = np.zeros(n_samples)

    if export_melody:
        position = 0.0
        for note, duration in melody:
            _add(melody_buf, _tone(note, duration * beat_sec), position * beat_sec)
            position += duration

    if export_chords:
        for measure, chord in enumerate(chords):
            start_sec = measure * BEATS_PER_MEASURE * beat_sec
            for note in chord:
                _add(
                    chord_buf,
                    _tone(note - 12, BEATS_PER_MEASURE * beat_sec,
                          harmonics=(1.0, 0.15), attack=0.03, release=0.15),
                    start_sec,
                )

    if export_drums:
        sounds = {"kick": _kick(), "snare": _snare(rng), "hat": _hat(rng)}
        gains = {"kick": 1.0, "snare": 0.7, "hat": 0.35}
        for measure in range(len(chords)):
            for drum_name, beat in drums:
                start_sec = (measure * BEATS_PER_MEASURE + beat) * beat_sec
                _add(drum_buf, sounds[drum_name] * gains[drum_name], start_sec)

    # 音量バランスを取って合成
    mix = 0.35 * melody_buf + 0.12 * chord_buf + 0.5 * drum_buf

    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.9          # 音割れ防止

    samples = (mix * 32767).astype(np.int16)

    with wave.open(path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(samples.tobytes())
