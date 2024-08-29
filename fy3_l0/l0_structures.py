from __future__ import annotations

import io
import numpy as np

from datetime import datetime


class Fy3eHeader:
    """
    TODO: doc
    """

    def __init__(self, satellite_name: str,
                       instrument: str,
                       scan_start: datetime,
                       scan_end: datetime,
                       l0_date_creation: datetime) -> None:
        
        self.__satellite_name = satellite_name
        self.__instrument = instrument
        self.__scan_start = scan_start
        self.__scan_end = scan_end
        self.__l0_date_creation = l0_date_creation

    @property
    def satellite_name(self) -> str:
        return self.__satellite_name
    
    @property
    def instrument(self) -> str:
        return self.__instrument

    @property
    def scan_start(self) -> datetime:
        return self.__scan_start
    
    @property
    def scan_end(self) -> datetime:
        return self.__scan_end
    
    @property
    def l0_date_creation(self) -> datetime:
        return self.__l0_date_creation
    

class Fy3eMetadata:
    def __init__(self, data: bytes) -> None:
        self.__data = data


class Fy3eDnBlock:
    def __init__(self, type: bytes, data: list[int]) -> None:
        self.type = type
        self.data = data


class Fy3eDnBlocks:
    def __init__(self, blocks: list[Fy3eDnBlock]) -> None:
        self.__blocks = blocks

    @property
    def blocks(self) -> list[Fy3eDnBlock]:
        return self.__blocks


class Fy3eTransportBlock:
    def __init__(self, metadata: Fy3eMetadata, dn_data_blocks: list[Fy3eDnBlocks]) -> None:
        self.metadata = metadata
        self.dn_data_blocks = dn_data_blocks
        

class Fy3eFile:
    def __init__(self, header: Fy3eHeader, transport_blocks: list[Fy3eTransportBlock]) -> None:
        self.__header = header
        self.__transport_blocks = transport_blocks

    @property
    def header(self) -> Fy3eHeader:
        return self.__header
    
    @property
    def transport_blocks(self) -> list[Fy3eTransportBlock]:
        return self.__transport_blocks


if __name__ == "__main__":
    pass