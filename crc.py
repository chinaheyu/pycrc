def reflect(data: int, width: int) -> int:
    reflected_data = 0
    for _ in range(width):
        reflected_data = (reflected_data << 1) | (data & 1)
        data >>= 1
    return reflected_data


def crc_remainder(data: int, data_width: int, width: int, polynomial: int, initial_value: int = 0) -> int:
    crc_register = initial_value
    bit_mask = (1 << width) - 1
    top_bit = (1 << (width - 1))
    if data_width > width:
        crc_register ^= data >> (data_width - width)
    else:
        crc_register ^= data << (width - data_width)
    for i in range(data_width):
        remain_bit = data_width - width - i
        if remain_bit > 0:
            next_bit = (data >> (remain_bit - 1)) & 1
        else:
            next_bit = 0
        if crc_register & top_bit:
            crc_register = (((crc_register << 1) | next_bit) ^ polynomial) & bit_mask
        else:
            crc_register = (crc_register << 1 | next_bit) & bit_mask
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


def create_crc_table(width: int, polynomial: int) -> list[int]:
    crc_table = []
    for i in range(256):
        crc_table.append(crc(i.to_bytes(1), width, polynomial))
    return crc_table


def table_based_crc(data: bytes, width: int, crc_table: list[int], initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    crc_register = initial_value
    bit_mask = (1 << width) - 1
    for byte in data:
        if input_reflected:
            byte = reflect(byte, 8)
        if width < 8:
            crc_index = byte ^ (crc_register << (8 - width))
            crc_register = crc_table[crc_index] ^ (crc_register << 8) & bit_mask
        else:
            crc_index = byte ^ (crc_register >> (width - 8))
            crc_register = crc_table[crc_index] ^ (crc_register << 8) & bit_mask
    if result_reflected:
        crc_register = reflect(crc_register, width)
    return crc_register ^ final_xor_value


class CRCAlgorithm:
    __algorithm_definitions__ = {
        "crc5_usb": (5, 0x05, 0x1f, True, True, 0x1f),
        "crc8": (8, 0xD5, 0, False, False, 0),
        "crc8_autosar": (8, 0x2F, 0xff, False, False, 0xff),
        "crc8_bluetooth": (8, 0xA7, 0, True, True, 0),
        "crc8_ccitt": (8, 0x07, 0, False, False, 0x55),
        "crc8_gsm_b": (8, 0x49, 0, False, False, 0xff),
        "crc8_sae_j1850": (8, 0x1D, 0xff, False, False, 0xff),
        "crc15_can": (15, 0x4599, 0, False, False, 0),
        "crc16_kermit": (16, 0x1021, 0, True, True, 0),
        "crc16_ccitt_true": (16, 0x1021, 0, True, True, 0),
        "crc16_xmodem": (16, 0x1021, 0, False, False, 0),
        "crc16_autosar": (16, 0x1021, 0xffff, False, False, 0),
        "crc16_ccitt_false": (16, 0x1021, 0xffff, False, False, 0),
        "crc16_cdma2000": (16, 0xC867, 0xffff, False, False, 0),
        "crc16_ibm": (16, 0x8005, 0, True, True, 0),
        "crc16_modbus": (16, 0x8005, 0xffff, True, True, 0),
        "crc16_profibus": (16, 0x1DCF, 0xffff, False, False, 0xffff),
        "crc24_flexray16_a": (24, 0x5D6DCB, 0xFEDCBA, False, False, 0),
        "crc24_flexray16_b": (24, 0x5D6DCB, 0xABCDEF, False, False, 0),
        "crc32": (32, 0x04C11DB7, 0xffffffff, True, True, 0xffffffff,),
        "crc32_bzip2": (32, 0x04C11DB7, 0xffffffff, False, False, 0xffffffff),
        "crc32_c": (32, 0x1EDC6F41, 0xffffffff, True, True, 0xffffffff),
        "crc64_ecma": (64, 0x42F0E1EBA9EA3693, 0, False, False, 0),
    }
    available_crc_algorithms = list(__algorithm_definitions__.keys())

    @classmethod
    def create_algorithm(cls, name: str):
        return cls(*cls.__algorithm_definitions__[name])

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


__all__ = ['crc', 'CRCAlgorithm']
