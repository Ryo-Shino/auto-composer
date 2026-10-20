"""自動作曲アプリのテスト（標準ライブラリの unittest だけで動きます）。

実行方法（リポジトリ直下で）:
    python -m unittest -v
"""
import os
import tempfile
import unittest
import wave

from chord import chord_library, create_chords, progressions
from drums import create_drums, drum_patterns
from melody import BEATS_PER_MEASURE, SCALE, create_melody
from synth import SAMPLE_RATE, render_wav

PROGRESSION_NAMES = list(progressions)
DRUM_NAMES = list(drum_patterns)
SEEDS = [0, 1, 42]


class ChordTests(unittest.TestCase):

    def test_progressions_use_only_known_chords(self):
        """進行に書かれたコード名が、すべて chord_library に存在する。"""
        for name in PROGRESSION_NAMES:
            for chord_name in progressions[name]:
                with self.subTest(progression=name, chord=chord_name):
                    self.assertIn(chord_name, chord_library)

    def test_create_chords_returns_one_chord_per_measure(self):
        for name in PROGRESSION_NAMES:
            with self.subTest(progression=name):
                self.assertEqual(len(create_chords(name)), len(progressions[name]))


class MelodyTests(unittest.TestCase):

    def test_fills_exactly_all_measures(self):
        """メロディの合計拍数が「4拍 × コード数」とぴったり一致する。"""
        for name in PROGRESSION_NAMES:
            for seed in SEEDS:
                with self.subTest(progression=name, seed=seed):
                    chords = create_chords(name)
                    melody = create_melody(chords, seed=seed)
                    total = sum(duration for _, duration in melody)
                    self.assertEqual(total, BEATS_PER_MEASURE * len(chords))

    def test_notes_do_not_cross_barlines(self):
        for name in PROGRESSION_NAMES:
            for seed in SEEDS:
                with self.subTest(progression=name, seed=seed):
                    melody = create_melody(create_chords(name), seed=seed)
                    position = 0.0
                    for _, duration in melody:
                        measure = int(position // BEATS_PER_MEASURE)
                        self.assertLessEqual(
                            position + duration, (measure + 1) * BEATS_PER_MEASURE
                        )
                        position += duration

    def test_stays_in_scale(self):
        for name in PROGRESSION_NAMES:
            with self.subTest(progression=name):
                melody = create_melody(create_chords(name), seed=1)
                self.assertTrue(all(note in SCALE for note, _ in melody))

    def test_ends_on_c(self):
        for name in PROGRESSION_NAMES:
            with self.subTest(progression=name):
                melody = create_melody(create_chords(name), seed=1)
                self.assertEqual(melody[-1][0], 60)

    def test_same_seed_gives_same_melody(self):
        chords = create_chords("Lemon")
        self.assertEqual(
            create_melody(chords, seed=42), create_melody(chords, seed=42)
        )

    def test_different_seeds_give_different_melodies(self):
        chords = create_chords("カノン")
        melodies = {tuple(create_melody(chords, seed=s)) for s in range(10)}
        self.assertGreater(len(melodies), 1)


class DrumTests(unittest.TestCase):

    def test_hits_fit_inside_one_measure(self):
        """次の小節にはみ出す拍（4以上）がない。"""
        for name in DRUM_NAMES:
            for _, beat in create_drums(name):
                with self.subTest(pattern=name, beat=beat):
                    self.assertGreaterEqual(beat, 0)
                    self.assertLess(beat, BEATS_PER_MEASURE)

    def test_drum_names_are_supported(self):
        for name in DRUM_NAMES:
            for drum_name, _ in create_drums(name):
                with self.subTest(pattern=name, drum=drum_name):
                    self.assertIn(drum_name, {"kick", "snare", "hat"})


class ExportTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_render_wav_creates_playable_file(self):
        chords = create_chords("Lemon")
        melody = create_melody(chords, seed=1)
        path = os.path.join(self.tmp.name, "test.wav")

        render_wav(melody, chords, create_drums("8ビート"), path, tempo=120)

        with wave.open(path) as wav_file:
            self.assertEqual(wav_file.getframerate(), SAMPLE_RATE)
            duration_sec = wav_file.getnframes() / wav_file.getframerate()
        # 4小節 × 4拍 × 0.5秒 + 余韻1秒 = 9秒
        self.assertAlmostEqual(duration_sec, 9.0, delta=0.01)

    def test_render_wav_is_reproducible(self):
        chords = create_chords("Lemon")
        melody = create_melody(chords, seed=1)
        drums = create_drums("Trapビート")
        first = os.path.join(self.tmp.name, "a.wav")
        second = os.path.join(self.tmp.name, "b.wav")

        render_wav(melody, chords, drums, first)
        render_wav(melody, chords, drums, second)

        with open(first, "rb") as a, open(second, "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_build_midi_runs_with_all_tracks(self):
        try:
            import midiutil  # noqa: F401
        except ImportError:
            self.skipTest("midiutil がインストールされていません")
        from midi_export import build_midi, save_midi

        chords = create_chords("Lemon")
        melody = create_melody(chords, seed=1)
        midi = build_midi(melody, chords, create_drums("8ビート"))

        path = os.path.join(self.tmp.name, "test.mid")
        save_midi(midi, path)
        with open(path, "rb") as f:
            self.assertEqual(f.read(4), b"MThd")   # MIDIファイルの先頭の印


if __name__ == "__main__":
    unittest.main()
