import unittest
from datetime import datetime
from arrendatools.plantillas.filters.fechas import dias_del_año, formato_fecha, aplicar_timedelta, trimestre, dias_entre


class TestFunciones(unittest.TestCase):

    def test_dias_del_año(self):
        self.assertEqual(dias_del_año(2023), 365)
        self.assertEqual(dias_del_año(2024), 366)
        self.assertEqual(dias_del_año(2000), 366)

    def test_formato_fecha(self):
        fecha_actual = datetime.now().isoformat()
        self.assertEqual(formato_fecha(fecha_actual), formato_fecha(fecha_actual, 'medium', 'Europe/Madrid', 'es_ES'))
        self.assertEqual(formato_fecha(fecha_actual, 'full'), formato_fecha(fecha_actual, 'full', 'Europe/Madrid', 'es_ES'))
        self.assertEqual(formato_fecha(fecha_actual, tzinfo='America/New_York'), formato_fecha(fecha_actual, 'medium', 'America/New_York', 'es_ES'))

    def test_aplicar_timedelta(self):
        fecha = '2023-06-14T12:00:00'
        self.assertEqual(aplicar_timedelta(fecha, dias=1), '2023-06-15T12:00:00')
        self.assertEqual(aplicar_timedelta(fecha, semanas=2), '2023-06-28T12:00:00')
        self.assertEqual(aplicar_timedelta(fecha, horas=-3), '2023-06-14T09:00:00')

    def test_trimestre(self):
        self.assertEqual(trimestre('2023-01-01'), '1T 2023')
        self.assertEqual(trimestre('2023-05-01', delta=1), '3T 2023')
        self.assertEqual(trimestre('2023-12-31', delta=-2), '3T 2023')

    def test_dias_entre(self):
        self.assertEqual(dias_entre('2023-01-01', '2023-12-31'), 364)
        self.assertEqual(dias_entre('2023-01-01', '2024-01-01'), 365)
        self.assertEqual(dias_entre('2023-06-01', '2024-01-01'), 214)
        self.assertEqual(dias_entre('2024-01-01', '2025-01-01'), 366)


if __name__ == '__main__':
    unittest.main()
