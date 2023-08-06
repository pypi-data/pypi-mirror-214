#import Numpy 
import numpy as np

class Multiplication:
    """Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.

    :param multiplier: The multiplier
    :type multuplier: int
    """
    def __init__(self, multiplier):
        self.multiplier = multiplier

        
    def multiply(self, number):
        """Multiply a given number by a multiplier

        : param number: The number to multiply
        :type number: int

        :param multiplier: The multiplier
        :type multiplier: int
        """
        return np.dot(number, self.multiplier)

multiplication = Multiplication(2)

print(multiplication.multiply(5))
