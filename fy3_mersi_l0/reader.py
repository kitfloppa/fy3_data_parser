from __future__ import annotations
from typing import Optional

import io
import numpy as np

from datetime import datetime

from .l0_structures import *
from .utils import read_uint12


class Fy3MersiBlockConfig:
    """
    TODO: doc
    """

    def __init__(self, name: str, num_blocks: int, block_size: int) -> None:
        """
        TODO: doc
        """
        
        self.__name = name
        self.__num_blocks = num_blocks
        self.__block_size = block_size

    @property
    def name(self) -> int:
        """
        TODO: doc
        """
        
        return self.__name

    @property
    def num_blocks(self) -> int:
        """
        TODO: doc
        """
        
        return self.__num_blocks
    
    @property
    def block_size(self) -> int:
        """
        TODO: doc
        """
        
        return self.__block_size


class Fy3MersiConfig:
    """
    TODO: doc
    """

    def __init__(self, date_time_format: str,
                       header_size: int,
                       metadata_size: int,
                       block_configs: list[Fy3MersiBlockConfig],
                       block_type_size: int) -> None:
        """
        TODO: doc
        """
        
        self.__date_time_format = date_time_format
        self.__header_size = header_size
        self.__metadata_size = metadata_size
        self.__block_configs = block_configs
        self.__block_type_size = block_type_size

    @property
    def date_time_format(self) -> str:
        """
        TODO: doc
        """

        return self.__date_time_format
    
    @property
    def header_size(self) -> int:
        """
        TODO: doc
        """
        
        return self.__header_size
    
    @property
    def metadata_size(self) -> int:
        """
        TODO: doc
        """
        
        return self.__metadata_size
    
    @property
    def block_configs(self) -> int:
        """
        TODO: doc
        """
        
        return self.__block_configs
    
    @property
    def block_type_size(self) -> int:
        """
        TODO: doc
        """
        
        return self.__block_type_size


FY3E_CONFIG = Fy3MersiConfig(date_time_format='%Y%m%d%H%M%S',
                             header_size=1159544,
                             metadata_size=554,
                             block_configs=[
                                Fy3MersiBlockConfig('sv_dn', num_blocks=1, block_size=25920),
                                Fy3MersiBlockConfig('voc_dn', num_blocks=1, block_size=17280),
                                Fy3MersiBlockConfig('bb_dn', num_blocks=1, block_size=8640),
                                Fy3MersiBlockConfig('11nm_dn', num_blocks=40, block_size=9216),
                                Fy3MersiBlockConfig('12nm_dn', num_blocks=40, block_size=9216),
                                Fy3MersiBlockConfig('1km_dn', num_blocks=40, block_size=9216),
                             ],
                             block_type_size=10)


class Fy3MersiReader:
    """
    TODO: doc
    """

    def __init__(self, config: Fy3MersiConfig) -> None:
        """
        TODO: doc
        """
        
        self.__config = config

    def __parse_header(self, stream: io.BufferedIOBase) -> Fy3MersiHeader:
        """
        TODO: doc
        """
        
        data = stream.read(self.__config.header_size)
        
        satellite_name = data[4:8].decode('utf-8')
        instrument = data[12:17].decode('utf-8')
        scan_start = datetime.strptime(data[33:47].decode('utf-8'), self.__config.date_time_format)
        scan_end = datetime.strptime(data[48:62].decode('utf-8'), self.__config.date_time_format)
        l0_date_creation = datetime.strptime(data[63:77].decode('utf-8'), self.__config.date_time_format)

        return Fy3MersiHeader(satellite_name, instrument, scan_start, scan_end, l0_date_creation)

    def __parse_metadata(self, stream: io.BufferedIOBase) -> Optional[Fy3MersiMetadata]:
        """
        TODO: doc
        """

        data = stream.read(self.__config.metadata_size)
            
        if len(data) != self.__config.metadata_size:
            return None

        return Fy3MersiMetadata(data)

    def __parse_dn_blocks(self, stream: io.BufferedIOBase, config: Fy3MersiBlockConfig) -> Fy3MersiDnBlocks:
        """
        TODO: doc
        """
        
        blocks = []
        for _ in range(config.num_blocks):
            type = stream.read(self.__config.block_type_size)
            data = stream.read(config.block_size)
            data = read_uint12(data)
            block = Fy3MersiDnBlock(type, data)
            blocks.append(block)

        return Fy3MersiDnBlocks(config.name, blocks)

    def parse(self, stream: io.BufferedIOBase) -> Fy3MersiFile:
        """
        TODO: doc
        """
        
        header = self.__parse_header(stream)

        transport_blocks = []
        while True:
            
            metadata = self.__parse_metadata(stream)
            if metadata is None: break

            dn_data = []
            for block in self.__config.block_configs:
                dn = self.__parse_dn_blocks(stream, block)
                dn_data.append(dn)

            transport_block = Fy3MersiTransportBlock(metadata, dn_data)
            transport_blocks.append(transport_block)

        return Fy3MersiFile(header, transport_blocks)
