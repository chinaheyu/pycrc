from typing import List
import unittest


def reflect(data: int, width: int) -> int:
    reflected_data = 0
    for _ in range(width):
        reflected_data = (reflected_data << 1) | (data & 1)
        data >>= 1
    return reflected_data


def crc_remainder(data: int, data_width: int, width: int, polynomial: int, initial_value: int = 0) -> int:
    crc_register = initial_value
    result_mask = (1 << width) - 1
    ms_bit = 1 << (width - 1)
    msb_lshift = width - data_width
    if msb_lshift > 0:
        crc_register ^= data << msb_lshift
    else:
        crc_register ^= data >> -msb_lshift
    for i in range(data_width):
        remain_bit = data_width - width - i
        if remain_bit > 0:
            next_bit = (data >> (remain_bit - 1)) & 1
        else:
            next_bit = 0
        if crc_register & ms_bit:
            crc_register = (((crc_register << 1) | next_bit) ^ polynomial)
        else:
            crc_register = (crc_register << 1 | next_bit)
        crc_register &= result_mask
    return crc_register


def crc(data: bytes, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    crc_register = initial_value
    for byte in data:
        if input_reflected:
            byte = reflect(byte, 8)
        crc_register = crc_remainder(byte, 8, width, polynomial, crc_register)
    if result_reflected:
        crc_register = reflect(crc_register, width)
    return crc_register ^ final_xor_value


def create_crc_table(width: int, polynomial: int) -> List[int]:
    crc_table = []
    for i in range(256):
        crc_table.append(crc_remainder(i, 8, width, polynomial))
    return crc_table


def table_based_crc(data: bytes, width: int, crc_table: List[int], initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    crc_register = initial_value
    result_mask = (1 << width) - 1
    msb_lshift = width - 8
    for byte in data:
        if input_reflected:
            byte = reflect(byte, 8)
        if msb_lshift > 0:
            crc_index = byte ^ (crc_register >> msb_lshift)
        else:
            crc_index = byte ^ (crc_register << -msb_lshift)
        crc_register = crc_table[crc_index] ^ (crc_register << 8) & result_mask
    if result_reflected:
        crc_register = reflect(crc_register, width)
    return crc_register ^ final_xor_value


crc_algorithm_definitions = {
    "crc5_usb": (5, 0x05, 0x1f, True, True, 0x1f, 0x19),
    "crc8": (8, 0xD5, 0, False, False, 0, 0xBC),
    "crc8_autosar": (8, 0x2F, 0xff, False, False, 0xff, 0xDF),
    "crc8_bluetooth": (8, 0xA7, 0, True, True, 0, 0x26),
    "crc8_ccitt": (8, 0x07, 0, False, False, 0x55, 0xA1),
    "crc8_gsm_b": (8, 0x49, 0, False, False, 0xff, 0x94),
    "crc8_sae_j1850": (8, 0x1D, 0xff, False, False, 0xff, 0x4B),
    "crc15_can": (15, 0x4599, 0, False, False, 0, 0x059E),
    "crc16_kermit": (16, 0x1021, 0, True, True, 0, 0x2189),
    "crc16_ccitt_true": (16, 0x1021, 0, True, True, 0, 0x2189),
    "crc16_xmodem": (16, 0x1021, 0, False, False, 0, 0x31C3),
    "crc16_autosar": (16, 0x1021, 0xffff, False, False, 0, 0x29B1),
    "crc16_ccitt_false": (16, 0x1021, 0xffff, False, False, 0, 0x29B1),
    "crc16_cdma2000": (16, 0xC867, 0xffff, False, False, 0, 0x4C06),
    "crc16_ibm": (16, 0x8005, 0, True, True, 0, 0xBB3D),
    "crc16_modbus": (16, 0x8005, 0xffff, True, True, 0, 0x4B37),
    "crc16_profibus": (16, 0x1DCF, 0xffff, False, False, 0xffff, 0xA819),
    "crc24_flexray16_a": (24, 0x5D6DCB, 0xFEDCBA, False, False, 0, 0x7979BD),
    "crc24_flexray16_b": (24, 0x5D6DCB, 0xABCDEF, False, False, 0, 0x1F23B8),
    "crc32": (32, 0x04C11DB7, 0xffffffff, True, True, 0xffffffff, 0xCBF43926),
    "crc32_bzip2": (32, 0x04C11DB7, 0xffffffff, False, False, 0xffffffff, 0xFC891918),
    "crc32_c": (32, 0x1EDC6F41, 0xffffffff, True, True, 0xffffffff, 0xE3069283),
    "crc64_ecma": (64, 0x42F0E1EBA9EA3693, 0, False, False, 0, 0x6C40DF5F0B497347),
}


available_crc_algorithms = list(crc_algorithm_definitions.keys())


class CRCAlgorithm:
    @classmethod
    def create_algorithm(cls, name: str) -> 'CRCAlgorithm':
        return cls(*crc_algorithm_definitions[name][:6])

    def __init__(self, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> None:
        self.crc_table = create_crc_table(width, polynomial)
        self.width = width
        self.polynomial = polynomial
        self.initial_value = initial_value
        self.input_reflected = input_reflected
        self.result_reflected = result_reflected
        self.final_xor_value = final_xor_value

    def __call__(self, data: bytes) -> int:
        return table_based_crc(data, self.width, self.crc_table, self.initial_value, self.input_reflected, self.result_reflected, self.final_xor_value)


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


__all__ = ['crc', 'CRCAlgorithm']
