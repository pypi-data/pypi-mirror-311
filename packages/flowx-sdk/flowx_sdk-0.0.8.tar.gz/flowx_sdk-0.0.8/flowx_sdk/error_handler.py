from termcolor import colored #type: ignore

class CustomException(Exception):
    def __init__(self, message, hint=None) -> None:
        super().__init__(message)
        self.hint = hint

    def __str__(self) -> str:
        if self.hint:
            # Return the message with a hint in a different color
            return f"{colored(self.args[0], 'red')} {colored(f'Hint: {self.hint}', 'yellow')}"
        return self.args[0]