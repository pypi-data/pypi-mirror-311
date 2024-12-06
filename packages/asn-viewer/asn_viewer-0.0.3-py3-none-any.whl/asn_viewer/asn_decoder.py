from json import dumps
from numbers import Number
from os import PathLike
from typing import List, Set, Any, Generator, AnyStr

from asn1tools import parse_files
from asn1tools.compiler import Specification
from asn1tools.codecs import ber, type_checker, constraints_checker


class ASNDecoder(Specification):
    """
    ASN Decoder class
    Extends asn1tools.compiler.Specification
    """
    def __init__(self, spec_file: PathLike[str], object_name: str):
        self.object_name = object_name
        self.schema = parse_files([spec_file])
        self.decoded_asn_objects = []
        super().__init__(ber.compile_dict(self.schema, True),
                         ber.decode_full_length,
                         type_checker.compile_dict(self.schema, True),
                         constraints_checker.compile_dict(self.schema, True)
                         )

    def jsonify(self, data: bytes):
        return dumps(self.decode(self.object_name, data))

    @staticmethod
    def __values_match(a: str, b: Any) -> bool:
        try:
            if isinstance(b, int):
                return int(a) == b
            elif isinstance(b, float):
                return float(a) == b
            elif isinstance(b, str):
                return a == b
        except ValueError:
            return False


    def __decode_files(self, files: List[PathLike[str]]):
        for f in  files:
            try:
                with open(f, 'rb') as asn_object_b:
                    while b0 := asn_object_b.read(1):
                        b1 = asn_object_b.read(1)
                        b2 = asn_object_b.read(int.from_bytes(b1) - 0x80)
                        b3 = asn_object_b.read(int.from_bytes(b2))
                        yield self.decode(self.object_name, b0 + b1 + b2 + b3)
            except FileNotFoundError:
                # Don't care if the source file is not accessible
                continue

    def load_files(self, files: List[PathLike]):
        for r in self.__decode_files(files):
            self.decoded_asn_objects.append(r)

    def save_decoded_to_file(self, filename: PathLike[str], search_filter: dict | None = None):
        with open(filename, 'wt') as target_file:
            asn_objects = self.decoded_asn_objects if not search_filter else self.__search_data(**search_filter)
            target_file.write(
               "\n".join([dumps(u) for u in asn_objects])
            )

    def __search_data(self, **kwargs) -> list[dict]:
        return list(
            u for u in self.decoded_asn_objects
            if all(any(self.__values_match(w, u[k]) for w in v) for k, v in kwargs.items())
        )

    def print_search_result(self, **kwargs):
        print(self.__search_data(**kwargs))

    def print_file_data_json(self, search_filter: dict | None):
        asn_objects = self.decoded_asn_objects if not search_filter else self.__search_data(**search_filter)
        print(*(dumps(o) for o in asn_objects))
