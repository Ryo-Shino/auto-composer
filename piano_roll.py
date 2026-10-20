"""生成結果をピアノロール風の画像にする（READMEに貼って結果を一目で伝えるため）。"""
import matplotlib

matplotlib.use("Agg")   # 画面なしで画像だけ作る
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator

BEATS_PER_MEASURE = 4
DRUM_ROWS = {"hat": 0, "snare": 1, "kick": 2}


def save_piano_roll(melody, chords, drums, path):
    total_beats = len(chords) * BEATS_PER_MEASURE

    fig, (ax_notes, ax_drums) = plt.subplots(
        2, 1,
        figsize=(max(8, total_beats * 0.45), 6),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )

    # --- コード（背景の灰色の帯） ---
    for measure, chord in enumerate(chords):
        for note in chord:
            ax_notes.add_patch(Rectangle(
                (measure * BEATS_PER_MEASURE, note - 0.4),
                BEATS_PER_MEASURE, 0.8,
                color="gray", alpha=0.35,
            ))

    # --- メロディ（青） ---
    position = 0.0
    for note, duration in melody:
        ax_notes.add_patch(Rectangle(
            (position, note - 0.4), duration * 0.95, 0.8, color="tab:blue",
        ))
        position += duration

    all_notes = [n for chord in chords for n in chord] + [n for n, _ in melody]
    ax_notes.set_ylim(min(all_notes) - 2, max(all_notes) + 2)
    ax_notes.yaxis.set_major_locator(MaxNLocator(integer=True))   # 音程は整数目盛り
    ax_notes.set_ylabel("MIDI note")
    ax_notes.set_title("Generated music (blue: melody / gray: chords)")

    # --- ドラム ---
    for measure in range(len(chords)):
        for drum_name, beat in drums:
            ax_drums.plot(
                measure * BEATS_PER_MEASURE + beat, DRUM_ROWS[drum_name],
                marker="s", markersize=4, color="tab:red", linestyle="",
            )
    ax_drums.set_yticks(list(DRUM_ROWS.values()))
    ax_drums.set_yticklabels(list(DRUM_ROWS.keys()))
    ax_drums.set_ylim(-0.7, 2.7)
    ax_drums.set_xlabel("beats")

    # --- 小節線 ---
    ax_drums.set_xlim(-0.2, total_beats)   # 0拍目の点が欠けないよう少し余白
    for ax in (ax_notes, ax_drums):
        for measure in range(len(chords) + 1):
            ax.axvline(measure * BEATS_PER_MEASURE, color="black", linewidth=0.6, alpha=0.5)

    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
