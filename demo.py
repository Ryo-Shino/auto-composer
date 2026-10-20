"""デモモード: GUIなしで1コマンドで曲を生成する。

使い方:
    python demo.py
    python demo.py --progression カノン --drums Trapビート --seed 7

output/ に sample.mid / sample.wav / piano_roll.png が出力される。
"""
import argparse
import os

from chord import create_chords, progressions
from drums import create_drums, drum_patterns
from melody import create_melody
from midi_export import TEMPO, build_midi, save_midi
from piano_roll import save_piano_roll
from synth import render_wav


def parse_args():
    parser = argparse.ArgumentParser(description="自動作曲アプリ（デモモード）")
    parser.add_argument(
        "--progression", default="Lemon", choices=list(progressions),
        help="コード進行（デフォルト: Lemon）",
    )
    parser.add_argument(
        "--drums", default="8ビート", choices=list(drum_patterns),
        help="ドラムパターン（デフォルト: 8ビート）",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="乱数シード。同じ値なら同じ曲になる（デフォルト: 42）",
    )
    parser.add_argument(
        "--out", default="output",
        help="出力フォルダ（デフォルト: output）",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)

    chords = create_chords(args.progression)
    melody = create_melody(chords, seed=args.seed)
    drums = create_drums(args.drums)

    midi_path = os.path.join(args.out, "sample.mid")
    wav_path = os.path.join(args.out, "sample.wav")
    image_path = os.path.join(args.out, "piano_roll.png")

    save_midi(build_midi(melody, chords, drums), midi_path)
    render_wav(melody, chords, drums, wav_path, tempo=TEMPO)
    save_piano_roll(melody, chords, drums, image_path)

    print(f"コード進行: {args.progression} / ドラム: {args.drums} / seed: {args.seed}")
    print(f"メロディ: {len(melody)}音, {len(chords)}小節")
    print("出力:")
    for path in (midi_path, wav_path, image_path):
        print(f"  {path}")


if __name__ == "__main__":
    main()
