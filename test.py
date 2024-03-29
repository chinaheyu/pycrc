import unittest
from crc import crc, crc_algorithm_definitions, CRCAlgorithm


class CRCUnitTest(unittest.TestCase):
    def test_crc(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc(b'123456789', *algorithm_definition[:6]), algorithm_definition[6])

    def test_table_based_crc(self):
        for algorithm_name, algorithm_definition in crc_algorithm_definitions.items():
            crc_algorithm = CRCAlgorithm.create_algorithm(algorithm_name)
            with self.subTest(algorithm_name=algorithm_name):
                self.assertEqual(crc_algorithm(b'123456789'), algorithm_definition[6])


if __name__ == '__main__':
    unittest.main(verbosity=2)
