def getgrammar():
    return r'''
        start: compose
            | lhs "=" rhs compose

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

        chord: "(" notename+ ")" | lhs

        tuple: "tuplet("i (chord|note)+ ")"

        note: division notename
            | division chord
            | division tuple
            | division rest
            | lhs

        inlinedynamic: "mf"i
            | "mp"i
            | "f"i+
            | "p"i+
            | lhs

        dynamic: "Dynamic("i inlinedynamic ")"

        noteitem: note ";"
            | inlinedynamic ";"

        instrumentation: (instrument | lhs) "{" noteitem+ "}"
            | lhs

        measure: "Measure"i "{" instrumentation* "}"
            | lhs

        tempo: "Tempo("i number ")"
            | lhs

        timesig: "Timesig("i division ")"
            | lhs

        repeat: "Repeat"i composeitems+ "Endr"i

        composeitems: tempo
            | timesig
            | dynamic
            | measure
            | repeat

        lhs: "$" NAME

        rhs: composeitems
            | instrument
            | instrumentation
            | note
            | tuple
            | chord
            | tempo
            | timesig
            | inlinedynamic
            | dynamic

        COMMENT: "//" /[^\n]/*
        WHITESPACE: " " | "\t" | "\n"

        %import common.CNAME -> NAME

        %ignore COMMENT
        %ignore WHITESPACE
    '''
