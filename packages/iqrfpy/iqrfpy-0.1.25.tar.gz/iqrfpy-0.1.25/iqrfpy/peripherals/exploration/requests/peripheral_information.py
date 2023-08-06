from typing import Optional, Union
from iqrfpy.enums.commands import ExplorationRequestCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['PeripheralInformationRequest']


class PeripheralInformationRequest(IRequest):

    def __init__(self, nadr: int, per: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None, msgid: Optional[str] = None):
        super().__init__(
            nadr=nadr,
            pnum=per,
            pcmd=ExplorationRequestCommands.PERIPHERALS_ENUMERATION_INFORMATION,
            m_type=ExplorationMessages.PERIPHERAL_INFORMATION,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'per': self._pnum.value if isinstance(self._pnum, Peripheral) else self._pnum}
        return super().to_json()
