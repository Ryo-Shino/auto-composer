import random

#ドラムパターン
drum_patterns = {

    "8ビート":[
        ("kick",0),
        ("hat",0),
        ("hat",1),
        ("snare",1),
        ("kick",2),
        ("hat",2),
        ("kick",2.5),
        ("snare",3),
        ("hat",3),
    ],

    "ダンスビート":[
        ("kick",0),
        ("hat",0),
        ("hat",0.5),
        ("kick",1),
        ("snare",1),
        ("hat",1.5),
        ("kick",2),
        ("hat",2.5),
        ("kick",3),
        ("snare",3),
        ("hat",3.5),
    ],

    "Trapビート":[
        ("kick",0),
        ("hat",0),
        ("hat",0.25),
        ("hat",0.5),
        ("hat",0.75),
        ("kick",1),
        ("hat",1),
        ("hat",1.125),
        ("hat",1.25),
        ("hat",1.375),
        ("hat",1.5),
        ("hat",1.625),
        ("hat",1.75),
        ("hat",1.875),
        ("kick",2),
        ("hat",2),
        ("hat",2.25),
        ("hat",2.5),
        ("hat",2.75),
        ("snare",3),
        ("kick",3),
        ("hat",3),
        ("hat",3.125),
        ("hat",3.25),
        ("hat",3.375),
        ("hat",3.5),
        ("hat",3.625),
        ("hat",3.75),
        ("hat",3.875),

    ]
}

def create_drums(selected_name):

    return drum_patterns[selected_name]
