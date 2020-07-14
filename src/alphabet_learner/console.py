import collections

from .ansi import ANSI


class Console:
    def __init__(self, size=5):
        self.history = collections.deque(maxlen=size)

    def undo(self):
        print(
            ANSI.UP[self.history.pop().count("\n")] + "\r" + ANSI.CLEAR, end="",
        )

    def print(self, *args, sep=" ", end="\n", flush=False):
        output = sep.join(args) + end
        self.history.append(output)
        print(output, sep="", end="", flush=flush)

    def input(self, prompt=None):
        output = input(prompt)
        self.history.append((prompt or "") + output + "\n")
        return output


console = Console()
