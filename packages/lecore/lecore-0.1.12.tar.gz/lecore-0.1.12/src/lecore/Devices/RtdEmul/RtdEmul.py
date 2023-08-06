from ..ModbusDev import *


class RtdEmul(ModbusDev):

    def __init__(self, com=None, reg_map=None, upg=None, visual=None):
        super().__init__()
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/"
        print(f"PATH RTD = {self.path}")
        self.def_regs = "RtdEmul_Modbus.json"

        self._com(com)
        self._reg_map(reg_map)
        self._upg(upg)
        self._visual(visual)


