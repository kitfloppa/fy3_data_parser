from __future__ import annotations
from typing import Optional

import io
import numpy as np

from datetime import datetime

from .l0_structures import *
from .utils import read_uint12


DATE_TIME_FORMAT = '%Y%m%d%H%M%S'

HEADER_SIZE = 1159544
METADATA_SIZE = 554
SV_SCAN_SIZE = 25920
VOC_SCAN_SIZE = 17280
BB_SCAN_SIZE = 8640
TRANSPORT_BLOCK_SIZE = 9216

SYNCHROSERIES_SIZE = 10
SENSORS_COUNT = 40


def parse_header(stream: io.BufferedIOBase) -> Fy3eHeader:
    data = stream.read(HEADER_SIZE)
    
    satellite_name = data[4:8].decode('utf-8')
    instrument = data[12:17].decode('utf-8')
    scan_start = datetime.strptime(data[33:47].decode('utf-8'), DATE_TIME_FORMAT)
    scan_end = datetime.strptime(data[48:62].decode('utf-8'), DATE_TIME_FORMAT)
    l0_date_creation = datetime.strptime(data[63:77].decode('utf-8'), DATE_TIME_FORMAT)

    return Fy3eHeader(satellite_name, instrument, scan_start, scan_end, l0_date_creation)

def parse_metadata(stream: io.BufferedIOBase) -> Optional[Fy3eMetadata]:
    data = stream.read(METADATA_SIZE)
        
    if len(data) != METADATA_SIZE:
        return None

    return Fy3eMetadata(data)

def parse_dn_blocks(stream: io.BufferedIOBase, num_blocks: int, block_size: int) -> Fy3eDnBlocks:
    blocks = []
    for _ in range(num_blocks):
        type = stream.read(SYNCHROSERIES_SIZE)
        data = stream.read(block_size)
        data = read_uint12(data)
        block = Fy3eDnBlock(type, data)
        blocks.append(block)

    return Fy3eDnBlocks(blocks)

def parse(stream: io.BufferedIOBase) -> Fy3eFile:
    header = parse_header(stream)

    transport_blocks = []
    while True:
        
        metadata = parse_metadata(stream)
        if metadata is None: break

        sv_scanlines = parse_dn_blocks(stream, 1, SV_SCAN_SIZE)
        voc_scanlines = parse_dn_blocks(stream, 1, VOC_SCAN_SIZE)
        bb_scanlines = parse_dn_blocks(stream, 1, BB_SCAN_SIZE)

        dn_11_scanline = parse_dn_blocks(stream, SENSORS_COUNT, TRANSPORT_BLOCK_SIZE)
        dn_12_scanline = parse_dn_blocks(stream, SENSORS_COUNT, TRANSPORT_BLOCK_SIZE)
        dn_1km_scanline = parse_dn_blocks(stream, SENSORS_COUNT, TRANSPORT_BLOCK_SIZE)

        transport_block = Fy3eTransportBlock(metadata, [sv_scanlines, voc_scanlines, bb_scanlines, dn_11_scanline, dn_12_scanline, dn_1km_scanline])
        transport_blocks.append(transport_block)

    return Fy3eFile(header, transport_blocks)
