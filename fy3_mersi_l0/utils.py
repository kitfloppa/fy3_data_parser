from __future__ import annotations
from typing import Optional

import numpy as np

from .l0_structures import Fy3MersiFile, Fy3MersiTransportBlock, Fy3MersiDnBlocks


def read_uint12(data_chunk: bytes) -> np.ndarray:
    """
    TODO: doc
    """
    
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
    snd_uint12 = ((mid_uint8 % 16) << 8) + lst_uint8
    
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])

def get_info(file: Fy3MersiFile) -> str:
    """
    TODO: doc
    """
    
    transport_blocks_size = len(file.transport_blocks)
    blocks = ', '.join([block.name for block in file.transport_blocks[0].dn_data_blocks])

    return f"Transport blocks size: {transport_blocks_size},\nBlocks: {blocks}"

def get_block_by_name(transport_block: Fy3MersiTransportBlock, name: str) -> Optional[Fy3MersiDnBlocks]:
    """
    TODO: doc
    """
    
    for block in transport_block.dn_data_blocks:
        if block.name == name:
            return block
        
    return None

def get_all_blocks_by_name(file: Fy3MersiFile, name: str) -> list[Fy3MersiDnBlocks]:
    """
    TODO: doc
    """

    blocks = []
    for transport_block in file.transport_blocks:
        block = get_block_by_name(transport_block, name)

        if block:
            blocks.append(block)

    return blocks

def get_data_by_name(file: Fy3MersiFile, name: str) -> np.ndarray:
    """
    TODO: doc
    """
    
    data = []
    for i in get_all_blocks_by_name(file, name):
        data.append(np.stack([block.data for block in i.blocks]))

    data = np.array(data)

    return data.reshape((data.shape[0] * data.shape[1]), data.shape[2])
