def getgrammar():
    return r'''
        start: (id "=" rhs)* compose

        digit: "0"
            | "1"
            | "2"
            | "3"
            | "4"
            | "5"
            | "6"
            | "7"
            | "8"
            | "9"

        accidental: "#" | "b"
        
        compose: "compose"i "{" composeitems* "}"

        notename: ("a".."g" | "A".."G") accidental? number

        rest: "--"

        number: digit+

        instrument: "trumpet"i | "piano"i | "tuba"i | "acousticgrandpiano"i

        division: number "/" number

        chord: "(" notename+ ")"

        tuple: "tuplet("i (chord|note|id)+ ")"

        note: division notename
            | division (chord | id)
            | division (tuple | id)
            | division rest

        inlinedynamic: "mf"i
            | "mp"i
            | "f"i+
            | "p"i+

        dynamic: "Dynamic("i (inlinedynamic | id) ")"

        noteitem: (note|id) ";"
            | inlinedynamic ";"

        instrumentation: (instrument | id) "{" noteitem+ "}"

        measure: "Measure"i "{" (instrumentation | id)* "}"

        tempo: "Tempo("i number ")"

        timesig: "Timesig("i division ")"

        repeat: "Repeat"i composeitems+ "Endr"i

        composeitems: id
            | tempo
            | timesig
            | dynamic
            | measure
            | repeat

        id: /[$][a-zA-Z]+[a-zA-Z0-9_\-]*/

        rhs: instrument
            | tempo
            | timesig
            | dynamic
            | measure
            | repeat
            | instrumentation
            | note
            | tuple
            | chord
            | inlinedynamic
            | id

        INLINECOMMENT: "//" /[^\n]/*
        COMMENTBLOCK: "/*" /(.*[\n])*.*/ "*/"
        WHITESPACE: " " | "\t" | "\n"

        %ignore INLINECOMMENT
        %ignore COMMENTBLOCK
        %ignore WHITESPACE
'''
