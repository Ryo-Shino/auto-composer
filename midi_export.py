from midiutil import MIDIFile

TEMPO = 120          # テンポはDAW側で自由に変えられるので固定値でOK
VOLUME = 100
BEATS_PER_MEASURE = 4

# トラック番号とチャンネル
MELODY_TRACK, CHORD_TRACK, DRUM_TRACK = 0, 1, 2
MELODY_CHANNEL, CHORD_CHANNEL = 0, 1
DRUM_CHANNEL = 9      # ドラムはチャンネル9固定

DRUM_NOTES = {
    "kick": 36,
    "snare": 38,
    "hat": 42,
}


def build_midi(
    melody,
    chords,
    drums,
    export_melody=True,
    export_chords=True,
    export_drums=True,
):
    """メロディ・コード・ドラムから MIDIFile オブジェクトを作る（保存はしない）。"""

    midi = MIDIFile(3)

    for track in (MELODY_TRACK, CHORD_TRACK, DRUM_TRACK):
        midi.addTempo(track, 0, TEMPO)

    # =====================
    # メロディ
    # =====================
    if export_melody:
        melody_time = 0

        for note, duration in melody:
            midi.addNote(
                MELODY_TRACK, MELODY_CHANNEL,
                note, melody_time, duration, VOLUME,
            )
            melody_time += duration

    # =====================
    # コード（1コード = 1小節）
    # =====================
    if export_chords:
        chord_time = 0

        for chord in chords:
            for note in chord:
                midi.addNote(
                    CHORD_TRACK, CHORD_CHANNEL,
                    note, chord_time, BEATS_PER_MEASURE, 70,
                )
            chord_time += BEATS_PER_MEASURE

    # =====================
    # ドラム
    # =====================
    if export_drums:
        for measure in range(len(chords)):
            for drum_name, beat in drums:
                midi.addNote(
                    DRUM_TRACK, DRUM_CHANNEL,
                    DRUM_NOTES[drum_name],
                    measure * BEATS_PER_MEASURE + beat,
                    0.1,    # ドラムは音の長さが関係ないので短くしておく
                    VOLUME,
                )

    return midi


def save_midi(midi, path):
    """MIDIFile をファイルに保存する。"""
    with open(path, "wb") as output_file:
        midi.writeFile(output_file)


def export_midi(
    melody,
    chords,
    drums,
    export_melody=True,
    export_chords=True,
    export_drums=True,
):
    """GUI用: 保存先をダイアログで選んでMIDIを書き出す。"""

    # tkinter はGUIから呼ぶときだけ必要なので、ここで読み込む
    # （デモモードなど、画面のない環境でも他の機能が動くようにするため）
    from tkinter import Tk
    from tkinter.filedialog import asksaveasfilename

    midi = build_midi(
        melody, chords, drums,
        export_melody, export_chords, export_drums,
    )

    Tk().withdraw()

    file_name = asksaveasfilename(
        title="MIDIファイルを保存",
        defaultextension=".mid",
        filetypes=[("MIDIファイル", "*.mid")]
    )

    if file_name:
        save_midi(midi, file_name)
        print(f"{file_name} を保存しました。")
