"""
modulo para otras operaciones matematicas
"""
import math


class otrasoperaciones:
    """
    Clase para operaciones matematicas de : Log, Valor Absoluto, Raiz cuadrada
    """

    def logaritmo(self, num1):
        """
        Metodo para calcular el logaritmo
        """
        return math.log(num1)

    def absoluto(self, num1):
        """
        Metodo para calcular el logaritmo
        """
        return abs(num1)

    def raizCuadrada(self, num1):
        """
        Metodo para calcular el logaritmo
        """
        return math.sqrt(num1)

    def seno(self, num1):
        """
        Metodo para calcular el seno
        """
        return math.sin(num1)

    def coseno(self, num1):
        """
        Metodo para calcular el coseno
        """
        return math.cos(num1)

    def tangente(self, num1):
        """
        Metodo para calcular la tangente
        """
        return math.tan(num1)

    def cotangente(self, num1):
        """
        Metodo para calcular la tangente
        """
        return 1/math.tan(num1)

    def hipotenusa(self, num1, num2):
        """
        Metodo para calcular la hipotenusa
        """
        return math.hypot(num1, num2)
    
    def radian(self, num1):
        """
        Metodo para calcular el radiante
        """
        return math.radians(num1)
