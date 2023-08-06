class calculator:
    """
    The main package file should contain a class Calculator that should be able to perform these actions:
    Addition / Subtraction.
    Multiplication / Division.
    Take (n) root of a number.
    Reset memory (Calculator must have its own memory, meaning it will manipulate starting number 0 until it is reset.).
    """

    def __init__(self, num1, num2):
        self.memory = 0
        self.num1 = num1
        self.num2 = num2

    def add(self):
        """addition operation"""
        return self.num1 + self.num2

    def sub(self):
        """subtraction operation"""
        return self.num1 - self.num2

    def mul(self):
        """multiplication operation"""
        return self.num1 * self.num2

    def div(self):
        """division operation"""
        """if num2 has digit = 0 operation, it will provide message that this operation is not possible"""
        if self.num2 == 0:
            print("Divide by 0 Error is not possible")
        else:
            return round(self.num1 / self.num2, 2)

    def reset(self):
        """reset operation"""
        self.memory = 0
