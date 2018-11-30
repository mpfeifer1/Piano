class PianoException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotImplementedException(PianoException):
    def __init__(self, *args, **kwargs):
        PianoException.__init__(self, *args, **kwargs)


'''Semantic Analysis Exceptions'''
class SemanticError(PianoException):
    def __init__(self, *args, **kwargs):
        PianoException.__init__(self, *args, **kwargs)

class ValidationError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class TempoError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class TimesigError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class DynamicError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class MeasureError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class RepeatError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)

class DivisionError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class NoteError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


class SignalConversionError(SemanticError):
    def __init__(self, *args, **kwargs):
        SemanticError.__init__(self, *args, **kwargs)


'''Midi Generation Exceptions'''
class MidiError(PianoException):
    def __init__(self, *args, **kwargs):
        PianoException.__init__(self, *args, **kwargs)


class SignalError(MidiError):
    def __init__(self, *args, **kwargs):
        MidiError.__init__(self, *args, **kwargs)
