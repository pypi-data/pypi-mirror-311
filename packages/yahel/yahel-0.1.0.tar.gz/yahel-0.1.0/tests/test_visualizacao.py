import unittest
import numpy as np
import matplotlib.pyplot as plt
from yahel.area_chart import criar_grafico_area
from yahel.pie_chart import criar_grafico_pizza
from yahel.heatmap import criar_mapa_calor 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestYahel(unittest.TestCase):
    def test_grafico_pizza(self):
        dados = [30, 20, 50]
        rotulos = ['A', 'B', 'C']
        grafico = criar_grafico_pizza(dados, rotulos)
        self.assertIsNotNone(grafico)

    def test_mapa_calor(self):
        dados = np.random.rand(5, 5)
        grafico = criar_mapa_calor(dados)
        self.assertIsNotNone(grafico)

    def test_grafico_area(self):
        x = range(10)
        y1 = [i**2 for i in x]
        y2 = [i**3 for i in x]
        grafico = criar_grafico_area(x, y1, y2)
        self.assertIsNotNone(grafico)

if __name__ == '__main__':
    unittest.main()

