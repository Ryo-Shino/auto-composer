from tkinter import *
from tkinter import ttk

from melody import create_melody 
from chord import create_chords
from drums import create_drums
from midi_export import export_midi


def generate():

    progression_name = chord_combo.get()
    drum_name = drum_combo.get()

    #コード進行を選択
    chords = create_chords(progression_name)
    #コード進行に合わせてメロディを生成
    melody = create_melody(chords)
    #ドラムパターンを選択
    drums = create_drums(drum_name)

    #midiファイルを書き出し
    export_midi(
        melody,
        chords,
        drums,
        melody_var.get(),
        chord_var.get(),
        drum_var.get()
        )

#ボタンづくりの準備
root = Tk()
root.title("自動作曲アプリ")
root.geometry("300x230")

melody_var = BooleanVar(value=True)
chord_var = BooleanVar(value=True)
drum_var = BooleanVar(value=True)

Label(root,text="コード進行").pack()

chord_combo = ttk.Combobox(
    root,
    values=[
        "Lemon",
        "カノン",
        "千本桜",
        "Don't say lazy",
        "丸の内",
    ],
    state="readonly"
)

chord_combo.current(0)
chord_combo.pack()

Label(root, text="ドラムパターン").pack()

drum_combo = ttk.Combobox(
    root,
    values=[
        "8ビート",
        "ダンスビート",
        "Trapビート",
    ],
    state="readonly"
)

drum_combo.current(0)
drum_combo.pack()

Checkbutton(
    root,
    text="メロディ",
    variable=melody_var
).pack()

Checkbutton(
    root,
    text="コード",
    variable=chord_var
).pack()

Checkbutton(
    root,
    text="ドラム",
    variable=drum_var
).pack()

#ボタンを作る
button = Button(
    root,
    text="MIDIを生成",
    command=generate
)
#ボタンを配置
button.pack(pady=20)
#ボタンが押されるまで待機
root.mainloop()
