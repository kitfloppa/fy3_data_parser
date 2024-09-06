from __future__ import annotations

import h5py
import numpy as np

from collections import defaultdict
from .l0_structures import Fy3MersiFile
from .utils import get_data_by_name


class Hdf5Converter:
    def __init__(self) -> None:
        pass

    def convert(self, file: Fy3MersiFile, out: h5py.File) -> None:
        engineering_grp = out.create_group('Engineering', track_order=True)
        time_grp = out.create_group('Time', track_order=True)
        telemetry_grp = out.create_group('Telemetry', track_order=True)
        ancillary_grp = out.create_group('Ancillary', track_order=True)
        data_grp = out.create_group('Data', track_order=True)

        # Dataset with DN Earth data
        blocks = defaultdict(list)
        for transport_block in file.transport_blocks:
            for block in transport_block.dn_data_blocks:
                blocks[block.name].append(block)

        datasets = dict()
        for name in blocks.keys():
            data = []
            for val in blocks[name]:
                data.append(np.stack([block.data for block in val.blocks]))

            data = np.array(data)

            datasets[name] = data.reshape((data.shape[0] * data.shape[1]), data.shape[2])

        for name in datasets.keys():
            data_grp.create_dataset(name, data=datasets[name])
