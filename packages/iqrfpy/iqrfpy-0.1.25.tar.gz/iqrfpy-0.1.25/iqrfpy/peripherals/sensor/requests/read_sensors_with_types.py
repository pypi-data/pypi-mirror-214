from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import SensorRequestCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = [
    'ReadSensorsWithTypesRequest',
    'SensorWrittenData',
]


class SensorWrittenData:

    __slots__ = '_index', '_data'

    def __init__(self, index: int, data: List[int]):
        self._validate(index=index, data=data)
        self._index = index
        self._data = data

    def _validate(self, index: int, data: List[int]):
        self._validate_index(index)
        self._validate_data(data)

    @staticmethod
    def _validate_index(index: int):
        if not (dpa_constants.SENSOR_INDEX_MIN <= index <= dpa_constants.SENSOR_INDEX_MAX):
            raise RequestParameterInvalidValueError('Index value should be between 0 and 31.')

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value: int):
        self._validate_index(value)
        self._index = value

    @staticmethod
    def _validate_data(data: List[int]):
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_pdata(self):
        return [self.index] + self.data


class ReadSensorsWithTypesRequest(IRequest):

    __slots__ = '_sensors', '_written_data'

    def __init__(self, nadr: int, sensors: Optional[List[int]] = None,
                 written_data: Optional[List[SensorWrittenData]] = None, hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(sensors)
        super().__init__(
            nadr=nadr,
            pnum=Standards.SENSOR,
            pcmd=SensorRequestCommands.READ_SENSORS_WITH_TYPES,
            m_type=SensorMessages.READ_SENSORS_WITH_TYPES,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )
        self._sensors = sensors
        self._written_data = written_data

    @staticmethod
    def _validate(sensors: Optional[List[int]] = None):
        if sensors is not None:
            if len(sensors) > 32:
                raise RequestParameterInvalidValueError('Sensors length should be at most 32 bytes.')
            if len(sensors) == 0:
                return
            if min(sensors) < 0 or max(sensors) > 31:
                raise RequestParameterInvalidValueError('Sensors values should be between 0 and 31.')

    @property
    def sensors(self):
        return self._sensors

    @sensors.setter
    def sensors(self, value: Optional[List[int]]):
        self._validate(value)
        self._sensors = value

    @property
    def written_data(self):
        return self._written_data

    @written_data.setter
    def written_data(self, value: List[SensorWrittenData]):
        self._written_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        written_data = []
        if self._written_data is not None:
            for data in self._written_data:
                written_data += data.to_pdata()
        self._pdata = Common.sensors_indexes_to_bitmap(
            self._sensors if self._sensors is not None else [i for i in range(0, 32)]
        ) + written_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'sensorIndexes': self._sensors if self._sensors is not None else -1,
        }
        if self._written_data is not None:
            self._params['writtenData'] = [data.to_pdata() for data in self._written_data]
        return super().to_json()
