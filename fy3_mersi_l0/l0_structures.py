from __future__ import annotations

import io
import numpy as np

from datetime import datetime


class Fy3MersiHeader:
    """
    TODO: doc
    """

    def __init__(self, satellite_name: str,
                       instrument: str,
                       scan_start: datetime,
                       scan_end: datetime,
                       l0_date_creation: datetime) -> None:
        """
        TODO: doc
        """
        
        self.__satellite_name = satellite_name
        self.__instrument = instrument
        self.__scan_start = scan_start
        self.__scan_end = scan_end
        self.__l0_date_creation = l0_date_creation

    @property
    def satellite_name(self) -> str:
        """
        TODO: doc
        """
        
        return self.__satellite_name
    
    @property
    def instrument(self) -> str:
        """
        TODO: doc
        """
        
        return self.__instrument

    @property
    def scan_start(self) -> datetime:
        """
        TODO: doc
        """
        
        return self.__scan_start
    
    @property
    def scan_end(self) -> datetime:
        """
        TODO: doc
        """

        return self.__scan_end
    
    @property
    def l0_date_creation(self) -> datetime:
        """
        TODO: doc
        """
        
        return self.__l0_date_creation
    

class Fy3MersiMetadata:
    """
    TODO: doc
    """

    def __init__(self, data: bytes) -> None:
        """
        TODO: doc
        """
        
        self.__data = data

    @property
    def data(self) -> bytes:
        """
        TODO: doc
        """
        
        return self.__data


class Fy3MersiDnBlock:
    """
    TODO: doc
    """

    def __init__(self, type: bytes, data: np.ndarray) -> None:
        """
        TODO: doc
        """
        
        self.__type = type
        self.__data = data

    @property
    def type(self) -> bytes:
        """
        TODO: doc
        """
        
        return self.__type
    
    @property
    def data(self) -> np.ndarray:
        """
        TODO: doc
        """
        
        return self.__data


class Fy3MersiDnBlocks:
    """
    TODO: doc
    """

    def __init__(self, name: str, blocks: list[Fy3MersiDnBlock]) -> None:
        """
        TODO: doc
        """

        self.__name = name
        self.__blocks = blocks

    @property
    def name(self) -> list[Fy3MersiDnBlock]:
        """
        TODO: doc
        """
        
        return self.__name
    
    @property
    def blocks(self) -> list[Fy3MersiDnBlock]:
        """
        TODO: doc
        """
        
        return self.__blocks


class Fy3MersiTransportBlock:
    """
    TODO: doc
    """

    def __init__(self, metadata: Fy3MersiMetadata, dn_data_blocks: list[Fy3MersiDnBlocks]) -> None:
        """
        TODO: doc
        """
        
        self.__metadata = metadata
        self.__dn_data_blocks = dn_data_blocks

    @property
    def metadata(self) -> Fy3MersiMetadata:
        """
        TODO: doc
        """
        
        return self.__metadata
    
    @property
    def dn_data_blocks(self) -> list[Fy3MersiDnBlocks]:
        """
        TODO: doc
        """
        
        return self.__dn_data_blocks
        

class Fy3MersiFile:
    """
    TODO: doc
    """

    def __init__(self, header: Fy3MersiHeader, transport_blocks: list[Fy3MersiTransportBlock]) -> None:
        """
        TODO: doc
        """
        
        self.__header = header
        self.__transport_blocks = transport_blocks
    
    @property
    def header(self) -> Fy3MersiHeader:
        """
        TODO: doc
        """

        return self.__header
    
    @property
    def transport_blocks(self) -> list[Fy3MersiTransportBlock]:
        """
        TODO: doc
        """

        return self.__transport_blocks


if __name__ == "__main__":
    pass
