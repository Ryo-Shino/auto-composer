chord_library = {
    "C": [60, 64, 67],
    "Dm": [62, 65, 69],
    "Em": [64, 67, 71],
    "F": [65, 69, 72],
    "G": [67, 71, 74],
    "Am": [69, 72, 76],
    "Bm-5": [71, 74, 77]
}

progressions = {
    "Lemon":["C","G","Am","F"],
    "カノン":["C","G","Am","Em","F","C","F","G"],
    "千本桜":["Am","F","G","C"],
    "Don't say lazy":["F","G","Em","Am"],
    "丸の内":["F","Em","Am","G"]
    
}

def create_chords(selected_name):
    
    progression = progressions[selected_name]

    chords = []

    for chord_name in progression:
        chords.append(chord_library[chord_name])



    return chords
     