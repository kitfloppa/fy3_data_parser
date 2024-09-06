from __future__ import annotations
from typing import Optional

import io
import datetime
import struct
import numpy as np

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
        scan_start = datetime.datetime.strptime(data[33:47].decode('utf-8'), self.__config.date_time_format)
        scan_end = datetime.datetime.strptime(data[48:62].decode('utf-8'), self.__config.date_time_format)
        l0_date_creation = datetime.datetime.strptime(data[63:77].decode('utf-8'), self.__config.date_time_format)

        return Fy3MersiHeader(satellite_name, instrument, scan_start, scan_end, l0_date_creation)

    def __parse_metadata(self, stream: io.BufferedIOBase) -> Optional[Fy3MersiMetadata]:
        """
        TODO: doc
        """

        data = stream.read(self.__config.metadata_size)
            
        if len(data) != self.__config.metadata_size:
            return None
        
        frame_count = struct.unpack('i', data[:4])[0]
        day_count = datetime.date(2000, 1, 1) + datetime.timedelta(days=struct.unpack('H', data[8:10])[0])
        time_interval = struct.unpack('I', data[10:14])[0]
        time_count = struct.unpack('Q', data[14:22])[0]

        cal_signal_dn = np.zeros(5, dtype=np.uint16)
        bracket_calibrator_temp_dn = np.zeros(2, dtype=np.uint16)
        voc_temp_dn = 0
        cool_temp_voltage_dn = np.zeros(3, dtype=np.uint16)
        instrument_status_records = np.zeros(3, dtype=np.uint16)
        status_telemetry = np.zeros(2, dtype=np.uint16)
        k_mirror_motor_temp_dn = np.zeros(4, dtype=np.uint16)
        main_mirror_temp_dn = 0
        refl_mirror_temp_dn = 0
        vis_detector_temp_dn = 0
        near_ir_detector_temp_dn = 0
        swir_drv_temp_dn = 0
        vis_drv_temp_dn = 0
        ir_drv_temp_dn = np.zeros(2, dtype=np.uint16)
        obs_mode_voc = np.zeros(3, dtype=np.uint16)
        bb_temp_cnt = np.zeros(7, dtype=np.uint16)
        scans_type = 0
        obs_mode = 0

        telemetry_info = data[0x43:0x43 + 0x1e3]

        buffer_17 = telemetry_info[0x3f:]
        cal_signal_dn[:2] = read_uint12(buffer_17[:3])

        buffer_1 = buffer_17[0x3:]
        cal_signal_dn[2:4] = read_uint12(buffer_1[:3])

        buffer_2 = buffer_1[0x3:]
        cal_signal_dn[4], bracket_calibrator_temp_dn[0] = read_uint12(buffer_2[:3])
        bracket_calibrator_temp_dn[1], voc_temp_dn = read_uint12(buffer_2[3:6])

        buffer_3 = telemetry_info[0x4b:]
        cool_temp_voltage_dn[:2] = read_uint12(buffer_3[:3])

        buffer_4 = buffer_3[0x3:]
        cool_temp_voltage_dn[2], instrument_status_records[0] = read_uint12(buffer_4[:3])

        buffer_5 = buffer_4[0x3:]
        instrument_status_records[1], status_telemetry[0] = read_uint12(buffer_5[:3])
        status_telemetry[1], _ = read_uint12(buffer_5[3:6])

        buffer_6 = telemetry_info[0x54:]
        k_mirror_motor_temp_dn[:2] = read_uint12(buffer_6[:3])

        buffer_7 = buffer_6[0x3:]
        k_mirror_motor_temp_dn[2:4] = read_uint12(buffer_7[:3])

        buffer_8 = buffer_7[0x3:]
        main_mirror_temp_dn, refl_mirror_temp_dn = read_uint12(buffer_8[:3])

        buffer_9 = buffer_8[0x3:]
        vis_detector_temp_dn, near_ir_detector_temp_dn = read_uint12(buffer_9[:3])

        buffer_10 = buffer_9[0x3:]
        swir_drv_temp_dn, vis_drv_temp_dn = read_uint12(buffer_10[:3])

        buffer_11 = buffer_10[0x3:]
        ir_drv_temp_dn[:] = read_uint12(buffer_11[:3])

        buffer_12 = buffer_11[0x3:]
        instrument_status_records[2], obs_mode_voc[0] = read_uint12(buffer_12[:3])
        obs_mode_voc[1:] = read_uint12(buffer_12[3:6])

        buffer_14 = telemetry_info[0x1d7:]
        bb_temp_cnt[:2] = read_uint12(buffer_14[:3])

        buffer_15 = buffer_14[0x3:]
        bb_temp_cnt[2:4] = read_uint12(buffer_15[:3])

        buffer_16 = buffer_15[0x3:]
        bb_temp_cnt[4:6] = read_uint12(buffer_16[:3])
        bb_temp_cnt[6], flags = read_uint12(buffer_16[3:6])
        scans_type = flags & 1
        obs_mode = ((flags & 0x10) >> 4)
        obs_mode = obs_mode & 1, (obs_mode >> 1) & 1, (obs_mode >> 2) & 1, (obs_mode >> 3) & 1

        return Fy3MersiMetadata(frame_count,
                                day_count,
                                time_interval,
                                time_count,
                                cal_signal_dn,
                                bracket_calibrator_temp_dn,
                                voc_temp_dn,
                                cool_temp_voltage_dn,
                                instrument_status_records,
                                status_telemetry,
                                k_mirror_motor_temp_dn,
                                main_mirror_temp_dn,
                                refl_mirror_temp_dn,
                                vis_detector_temp_dn,
                                near_ir_detector_temp_dn,
                                swir_drv_temp_dn,
                                vis_drv_temp_dn,
                                ir_drv_temp_dn,
                                obs_mode_voc,
                                bb_temp_cnt,
                                scans_type,
                                obs_mode)

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
