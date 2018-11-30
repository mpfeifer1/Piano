def getgrammar():
    return r'''
        start: (id "=" rhs)* compose

        accidental: /[#|b]/

        compose: "compose"i "{" composeitems* "}"

        notename: ("a".."g" | "A".."G") accidental? number

        REST: "--"

        number: /[0-9]+/

        INSTRUMENT:   "acousticgrandpiano"i
                    | "brightacousticpiano"i
                    | "electricgrandpiano"i
                    | "honkytonkpiano"i
                    | "electricpiano1"i
                    | "electricpiano2"i
                    | "harpsichord"i
                    | "clavinet"i
                    | "celesta"i
                    | "glockenspiel"i
                    | "musicbox"i
                    | "vibraphone"i
                    | "marimba"i
                    | "xylophone"i
                    | "tubularbells"i
                    | "dulcimer"i
                    | "drawbarorgan"i
                    | "percussiveorgan"i
                    | "rockorgan"i
                    | "churchorgan"i
                    | "reedorgan"i
                    | "accordion"i
                    | "harmonica"i
                    | "tangoaccordion"i
                    | "acousticguitarnylon"i
                    | "acousticguitarsteel"i
                    | "electricguitarjazz"i
                    | "electricguitarclean"i
                    | "electricguitarmuted"i
                    | "overdrivenguitar"i
                    | "distortionguitar"i
                    | "guitarharmonics"i
                    | "acousticbass"i
                    | "electricbassfinger"i
                    | "electricbasspick"i
                    | "fretlessbass"i
                    | "slapbass1"i
                    | "slapbass2"i
                    | "synthbass1"i
                    | "synthbass2"i
                    | "violin"i
                    | "viola"i
                    | "cello"i
                    | "contrabass"i
                    | "tremolostrings"i
                    | "pizzicatostrings"i
                    | "orchestralharp"i
                    | "timpani"i
                    | "stringensemble1"i
                    | "stringensemble2"i
                    | "synthstrings1"i
                    | "synthstrings2"i
                    | "choiraahs"i
                    | "voiceoohs"i
                    | "synthvoice"i
                    | "orchestrahit"i
                    | "trumpet"i
                    | "trombone"i
                    | "tuba"i
                    | "mutedtrumpet"i
                    | "frenchhorn"i
                    | "brasssection"i
                    | "synthbrass1"i
                    | "synthbrass2"i
                    | "sopranosax"i
                    | "altosax"i
                    | "tenorsax"i
                    | "baritonesax"i
                    | "oboe"i
                    | "englishhorn"i
                    | "bassoon"i
                    | "clarinet"i
                    | "piccolo"i
                    | "flute"i
                    | "recorder"i
                    | "panflute"i
                    | "blownbottle"i
                    | "shakuhachi"i
                    | "whistle"i
                    | "ocarina"i
                    | "leadsquare"i
                    | "leadsawtooth"i
                    | "leadcalliope"i
                    | "leadchiff"i
                    | "leadcharang"i
                    | "leadvoice"i
                    | "leadfifths"i
                    | "leadbass"i
                    | "padnewage"i
                    | "padwarm"i
                    | "padpolysynth"i
                    | "padchoir"i
                    | "padbowed"i
                    | "padmetallic"i
                    | "padhalo"i
                    | "padsweep"i
                    | "rain"i
                    | "soundtrack"i
                    | "crystal"i
                    | "atmosphere"i
                    | "brightness"i
                    | "goblins"i
                    | "echoes"i
                    | "scifi"i
                    | "sitar"i
                    | "banjo"i
                    | "shamisen"i
                    | "koto"i
                    | "kalimba"i
                    | "bagpipe"i
                    | "fiddle"i
                    | "shanai"i
                    | "tinklebell"i
                    | "agogo"i
                    | "steeldrums"i
                    | "woodblock"i
                    | "taikodrum"i
                    | "melodictom"i
                    | "synthdrum"i
                    | "reversecymbal"i
                    | "guitarfretnoise"i
                    | "breathnoise"i
                    | "seashore"i
                    | "birdtweet"i
                    | "telephonering"i
                    | "helicopter"i
                    | "applause"i
                    | "gunshot"i

        division: number "/" number

        chord: "(" notename+ ")"

        tuple: "tuple(" (chord|notename|REST|id)+ ")"

        note: division notename
            | division (chord | id)
            | division (tuple | id)
            | division REST

        inlinedynamic: /([mM][pPfF]|[pP]+|[fF]+)/

        dynamic: "Dynamic("i (inlinedynamic | id) ")"

        noteitem: (note|id) ";"
            | inlinedynamic ";"

        instrumentation: (INSTRUMENT | id) "{" noteitem+ "}"

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

        rhs: INSTRUMENT
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
