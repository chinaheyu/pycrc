from typing import Protocol


class TableBasedCRCCallable(Protocol):
    def __call__(self, data: bytes, width: int, crc_table_msb: CRCTable, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
        ...


def reflect(data: int, width: int) -> int:
    ...


def crc_remainder_msb(data: int, data_width: int, width: int, polynomial: int, initial_value: int = 0) -> int:
    ...


def crc_remainder_lsb(data: int, data_width: int, polynomial: int, initial_value: int = 0) -> int:
    ...


def crc_msb(data: bytes, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    ...


def crc_lsb(data: bytes, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    ...


def crc(data: bytes, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    ...


class CRCTable:
    item_size: int
    buffer: bytearray

    @classmethod
    def create_msb_table(cls, width: int, polynomial: int) -> 'CRCTable':
        ...

    @classmethod
    def create_lsb_table(cls, width: int, polynomial: int) -> 'CRCTable':
        ...

    def __init__(self, width: int) -> None:
        ...

    def __getitem__(self, index: int) -> int:
        ...

    def __setitem__(self, index: int, value: int) -> None:
        ...


def table_based_crc_msb(data: bytes, width: int, crc_table_msb: CRCTable, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    ...


def table_based_crc_lsb(data: bytes, width: int, crc_table_lsb: CRCTable, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> int:
    ...


crc_algorithm_definitions: dict[str, tuple[int, int, int, bool, bool, int, int]]


class CRCAlgorithm:
    available_crc_algorithms: list[str]

    crc_table: CRCTable
    table_based_crc: TableBasedCRCCallable
    width: int
    polynomial: int
    initial_value: int
    input_reflected: bool
    result_reflected: bool
    final_xor_value: int

    @classmethod
    def create_algorithm(cls, name: str) -> 'CRCAlgorithm':
        ...

    def __init__(self, width: int, polynomial: int, initial_value: int = 0, input_reflected: bool = False, result_reflected: bool = False, final_xor_value: int = 0) -> None:
        ...

    def __call__(self, data: bytes) -> int:
        ...
