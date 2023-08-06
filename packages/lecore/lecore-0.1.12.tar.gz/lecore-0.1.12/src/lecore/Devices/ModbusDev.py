import os
from lecore.VisualModbus.MbClient import MbClient
from lecore.VisualModbus.RegMap import RegMap
from lecore.VisualModbus.MbUpgrade import MbUpgrade
from lecore.VisualModbus.VisualMbApp import VisualMbApp


class ModbusDev:

    def __init__(self):
        self.mb = MbClient()
        self.regs = RegMap(self.mb, 1)
        self.path = ""
        self.upg = None
        self.vis = None
        self.def_com = "ComSettings.json"
        self.def_visual = "VisualSettings.json"
        self.def_upg = "UpgradeSettings.json"
        self.def_regs = "None"
        self.slave = None
        self._com_file = ""
        self._reg_file = ""
        self._upg_file = ""
        self._vis_file = ""

    def open(self, slave=None, comport=None, baud_rate=None, parity=None, stop_bits=None, timeout=None, client=None):
        if slave is not None:
            self.slave = slave
            self.regs.slave = slave

        if client:
            self.mb = client
            return

        if None not in [comport, baud_rate, parity, stop_bits, timeout]:
            self.close()
            if comport is not None:
                self.mb.s['comport'] = comport
            if baud_rate is not None:
                self.mb.s['baud_rate'] = baud_rate
            if parity is not None:
                self.mb.s['parity'] = parity
            if stop_bits is not None:
                self.mb.s['stop_bits'] = stop_bits
            if timeout is not None:
                self.mb.s['timeout'] = timeout
            self.mb.open()

    def close(self):
        self.mb.close()

    def visual(self, timeout):
        self.close()
        self.vis.handle()

    def _visual(self, settings):
        self._vis_file = self.__path_complete(settings, self.def_visual)
        self.vis = VisualMbApp(self._vis_file, self._upg_file, self._com_file, self.slave, self._reg_file)
        self.regs.slave = self.vis.slave
        self.slave = self.vis.slave

    def _upg(self, settings):
        self._upg_file = self.__path_complete(settings, self.def_upg)
        self.upg = MbUpgrade(self._upg_file, self.mb, self.slave)

    def _com(self, settings):
        self._com_file = self.__path_complete(settings, self.def_com)
        self.mb.open(self._com_file)

    def _reg_map(self, reg_map):
        self._reg_file = self.__path_complete(reg_map, self.def_regs)
        self.regs.load(self._reg_file)

    def __path_complete(self, arg, default):
        if arg is None:
            ret = self.path + default
        elif "/" in arg or '\\' in arg:
            ret = arg
        else:
            ret = self.path + arg
        return ret

    # def visual(self, settings):

