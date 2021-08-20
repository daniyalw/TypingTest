class TypingTestResults:
    def __init__(self):
        pass

    def wpm(self, text_entered: str, time_taken: float) -> float:
        word_count = len(text_entered.split(' '))
        _wpm = word_count/time_taken
        return _wpm

    def errors(self, orig_text: str, text_entered: str) -> int:
        errors = 0
        orig_count = len(orig_text.split(' '))
        enter_count = len(text_entered.split(' '))

        if orig_count > enter_count:
            for i in range(0, orig_count):
                try:
                    entered_word = text_entered.split(' ')[i]
                    orig_word = orig_text.split(' ')[i]
                except IndexError:
                    continue
                else:
                    if entered_word != orig_word:
                        errors += 1
        else:
            for i in range(0, enter_count):
                try:
                    entered_word = text_entered.split(' ')[i]
                    orig_word = orig_text.split(' ')[i]
                except IndexError:
                    continue
                else:
                    if entered_word != orig_word:
                        errors += 1

        return errors

    def accuracy(self, num_count: int, errors: int) -> float:
        subtracted = num_count - errors
        result = subtracted/num_count
        return result
