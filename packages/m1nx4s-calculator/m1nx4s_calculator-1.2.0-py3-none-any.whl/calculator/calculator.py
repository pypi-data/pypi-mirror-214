class Calculator:
    """
    The main package file contains a class Calculator that perform these actions:
    Addition / Subtraction.
    Multiplication / Division.
    Reset memory (Calculator must have its own memory, meaning it will manipulate starting number 0 until it is reset.).
    """

    def __init__(self):
        self.memory = 0

    def add(self, num: int | float) -> float:
        """addition operation"""
        self.memory = self.memory + num
        return self.memory

    def sub(self, num: int | float) -> float:
        """subtraction operation"""
        self.memory = self.memory - num
        return self.memory

    def mul(self, num: int | float) -> float:
        """multiplication operation"""
        self.memory = self.memory * num
        return self.memory

    def div(self, num: int | float) -> float:
        """
        division operation
        if num has digit = 0 operation, it will provide message that this operation is not possible
        """
        if num == 0:
            print("Divide by 0 Error is not possible")
        else:
            self.memory = round(self.memory / num, 2)
            return self.memory

    def reset(self):
        """reset operation"""
        self.memory = 0
