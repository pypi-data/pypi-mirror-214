from typing import Optional, Union
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import EmbedPeripherals, Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = [
    'MorePeripheralsInformationRequest'
]


class MorePeripheralsInformationRequest(IRequest):

    def __init__(self, nadr: int, per: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None,
                 msgid: Optional[str] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.EXPLORATION,
            pcmd=per.value if isinstance(per, Peripheral) else per,
            m_type=ExplorationMessages.MORE_PERIPHERALS_INFORMATION,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'per': self._pcmd.value if isinstance(self._pcmd, Peripheral) else self._pcmd}
        return super().to_json()
