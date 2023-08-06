import unittest
import os
from time import sleep

# try:
#     import lecore.VisualModbus as VM
# except ImportError:
#     import src.lecore.VisualModbus as VM

import src.lecore.Devices.RtdEmul as RE

pth = os.path.dirname(os.path.abspath(__file__))


class TestSimple(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create instance of looger class
        """

        # com_file = pth + "/ComSettings.json"
        # rtd.com(com_file)
        # regs_file = pth + "/RtdEmul_Modbus.json"
        # rtd.reg_map(regs_file)
        rtd = RE.RtdEmul()

        # vm = VM.VisualMbApp(visual=pth + '/VisualSettings.json', upgrade=pth + '/UpgradeSettings.json', com=com_file,
        #                     reg_map=regs_file)

        # cls.vm = vm
        cls.rtd = rtd

    def setUp(self) -> None:
        """
        Insert just some delay between tests
        """
        sleep(0.1)

    def test001_rtd_emul_setup(self):
        """
        """
        pass

    def test0003_rtd_visual(self):
        self.rtd.visual(10)


    # def test003_modbus_visual(self):
    #
    #     self.vm.handle()


if __name__ == '__main__':
    unittest.main()

