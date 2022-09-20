
from time import time

class Timer:

    def __init__(self) -> None:
        self.Start()

    def Start(self):
        self.Reset()

    def Reset(self) -> None:
        self.start = time()

    def Elapsed(self) -> int:
        """Returns elapsed time in seconds"""
        return time() - self.start 


def IsClose(valueA, valueB, threshold) -> bool:
    if abs(valueA- valueB) < threshold:
        return True
    return False