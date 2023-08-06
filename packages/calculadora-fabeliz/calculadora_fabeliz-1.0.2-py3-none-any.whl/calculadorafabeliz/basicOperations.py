"""
Esta es un modulo que contiene las operaciones basicas de la calculadora
"""


class calculadora:
    """
    Clase Calculadora self, num1, num2
    """

    def suma(self, *numbers):
        """
        Metodo para retornar al suma

        Parametros: num1 Valor float o int
                    num2 Valor float o int

        Return: Valor de la sumatoria floar o int            
        """
        total = 0
        
        for number in numbers:
            total += number

        return total

    def resta(self, num1, num2):
        """
        Metodo para retornar la resta

        Parametros: num1 Valor float o int
                    num2 Valor float o int

        Return: Valor de la sumatoria floar o int            
        """
        return num1 - num2

    def multiplicacion(self, num1, num2):
        """
        Metodo para retornar la multiplicacion

        Parametros: num1 Valor float o int
                    num2 Valor float o int

        Return: Valor de la sumatoria floar o int            
        """
        return num1 * num2

    def division(self, num1, num2):
        """
        Metodo para retornar la multiplicacion

        Parametros: num1 Valor float o int
                    num2 Valor float o int

        Return: Valor de la sumatoria floar o int            
        """
        return num1 / num2
