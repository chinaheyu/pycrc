import unittest
from pycrc.crc import crc_msb, crc_lsb, crc, CRCTable, table_based_crc_msb, table_based_crc_lsb, crc_algorithm_definitions, CRCAlgorithm


class CRCUnitTest(unittest.TestCase):
    def test_crc_msb(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc_msb(b'123456789', *algorithm_definition[:6]), algorithm_definition[6])

    def test_crc_lsb(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc_lsb(b'123456789', *algorithm_definition[:6]), algorithm_definition[6])

    def test_crc(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc(b'123456789', *algorithm_definition[:6]), algorithm_definition[6])

    def test_table_based_crc_msb(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                crc_table = CRCTable.create_msb_table(*algorithm_definition[:2])
                self.assertEqual(table_based_crc_msb(b'123456789', algorithm_definition[0], crc_table, *algorithm_definition[2:6]), algorithm_definition[6])

    def test_table_based_crc_lsb(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                crc_table = CRCTable.create_lsb_table(*algorithm_definition[:2])
                self.assertEqual(table_based_crc_lsb(b'123456789', algorithm_definition[0], crc_table, *algorithm_definition[2:6]), algorithm_definition[6])

    def test_crc_algorithm(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            crc_algorithm = CRCAlgorithm.create_algorithm(algorithm_name)
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc_algorithm(b'123456789'), algorithm_definition[6])


if __name__ == '__main__':
    unittest.main(verbosity=2)
