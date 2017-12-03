INVALID_AUDIO_INDEX = 1000
AUDIO_EXCEPTION = 1001


class StrypeException(Exception):
    def __init__(self, error_code, error_message, *args):
        super().__init__(str(error_code) + ': ' + error_message, *args)
        self.msg = str(error_code) + ': ' + error_message
