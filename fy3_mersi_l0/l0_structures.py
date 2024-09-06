from __future__ import annotations

import io
import datetime
import numpy as np

class Fy3MersiHeader:
    """
    TODO: doc
    """

    def __init__(self, satellite_name: str,
                       instrument: str,
                       scan_start: datetime.datetime,
                       scan_end: datetime.datetime,
                       l0_date_creation: datetime.datetime) -> None:
        """
        TODO: doc
        """
        
        self.satellite_name = satellite_name
        self.instrument = instrument
        self.scan_start = scan_start
        self.scan_end = scan_end
        self.l0_date_creation = l0_date_creation    

class Fy3MersiMetadata:
    """
    TODO: doc
    """

    def __init__(self, frame_count: int, 
                       day_count: datetime.datetime,
                       time_interval: int,
                       time_count: int,
                       cal_signal_dn: int,
                       bracket_calibrator_temp_dn: int,
                       voc_temp_dn: int,
                       cool_temp_voltage_dn: int,
                       instrument_status_records: int,
                       status_telemetry: int,
                       k_mirror_motor_temp_dn: int,
                       main_mirror_temp_dn: int,
                       refl_mirror_temp_dn: int,
                       vis_detector_temp_dn: int,
                       near_ir_detector_temp_dn: int,
                       swir_drv_temp_dn: int,
                       vis_drv_temp_dn: int,
                       ir_drv_temp_dn: int,
                       obs_mode_voc: int,
                       bb_temp_cnt: int,
                       scans_type: int,
                       obs_mode: int) -> None:
        """
        TODO: doc
        """

        self.frame_count = frame_count
        self.day_count = day_count
        self.time_interval = time_interval
        self.time_count = time_count
        self.cal_signal_dn = cal_signal_dn
        self.bracket_calibrator_temp_dn = bracket_calibrator_temp_dn
        self.voc_temp_dn = voc_temp_dn
        self.cool_temp_voltage_dn = cool_temp_voltage_dn
        self.instrument_status_records = instrument_status_records
        self.status_telemetry = status_telemetry
        self.k_mirror_motor_temp_dn = k_mirror_motor_temp_dn
        self.main_mirror_temp_dn = main_mirror_temp_dn
        self.refl_mirror_temp_dn = refl_mirror_temp_dn
        self.vis_detector_temp_dn = vis_detector_temp_dn
        self.near_ir_detector_temp_dn = near_ir_detector_temp_dn
        self.swir_drv_temp_dn = swir_drv_temp_dn
        self.vis_drv_temp_dn = vis_drv_temp_dn
        self.ir_drv_temp_dn = ir_drv_temp_dn
        self.obs_mode_voc = obs_mode_voc
        self.bb_temp_cnt = bb_temp_cnt
        self.scans_type = scans_type
        self.obs_mode = obs_mode


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
