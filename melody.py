"""メロディ生成モジュール。

コード進行（コードのリスト）を受け取り、コードトーンを優先しながら
Cメジャースケール上でランダムにメロディを作る。
"""
import random

# Cメジャースケール（ド〜シ を2オクターブ分）
SCALE = [
    60, 62, 64, 65, 67, 69, 71,
    72, 74, 76, 77, 79, 81, 83,
]

# 使える音の長さ（拍）: 8分音符 / 4分音符 / 2分音符
DURATIONS = [0.5, 1.0, 2.0]

BEATS_PER_MEASURE = 4


def _next_note(current_note, chord, rng):
    """今の音の前後2音（自分自身を含む）から次の音を選ぶ。コードトーンがあれば優先。"""
    index = SCALE.index(current_note)

    candidates = [
        SCALE[i]
        for i in range(index - 2, index + 3)
        if 0 <= i < len(SCALE)
    ]

    chord_candidates = [note for note in candidates if note in chord]

    return rng.choice(chord_candidates or candidates)


def create_melody(chords, seed=None):
    """コード進行に合わせてメロディを生成する。

    chords: コードのリスト（1コード = 1小節）
    seed:   同じ値を渡すと同じメロディが再現される（None なら毎回ランダム）
    戻り値:  [(音程, 長さ), ...]
    """
    rng = random.Random(seed)

    total_beats = BEATS_PER_MEASURE * len(chords)

    melody = []
    position = 0.0          # 曲の先頭から数えた現在位置（拍）
    current_note = None

    while position < total_beats:
        # いま何小節目か → その小節のコードを使う
        measure = int(position // BEATS_PER_MEASURE)
        chord = chords[measure]

        # この小節の残り拍数。収まる音価だけ候補にする（小節をまたがない）
        remaining = (measure + 1) * BEATS_PER_MEASURE - position
        possible_durations = [d for d in DURATIONS if d <= remaining]

        if current_note is None:
            current_note = rng.choice(chord)   # 最初の音はコードトーン
        else:
            current_note = _next_note(current_note, chord, rng)

        duration = rng.choice(possible_durations)

        melody.append((current_note, duration))
        position += duration

    # 最後は「ド」で終わる
    _, last_duration = melody[-1]
    melody[-1] = (60, last_duration)

    return melody
