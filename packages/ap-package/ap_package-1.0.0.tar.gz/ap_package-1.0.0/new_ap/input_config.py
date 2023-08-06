from .ap_enum import LowpassFilterModeAnalogEnum, SignalPathWeightingFilterTypeEnum
from .apx500 import APxInputSelection

class InputConfiguration:
    def __init__(self, apx):
        self.APx = apx

    def change_channel(self, channel: int):
        """
        切换通道
        :param channel:
        :return:
        """
        if channel not in (1, 2):
            print('请输入正确的通道数')
            return
        self.APx.BenchMode.Setup.AnalogInput.ChannelCount = channel

    def change_connector(self, connector_type):
        """
        切换连接器
        :param connector_type:
        :return:
        """
        self.APx.BenchMode.Setup.AnalogInput.ConnectorType = connector_type

    @property
    def low_pass(self):
        return str(self.APx.BenchMode.Setup.AnalogInput.LowpassFilterModeAnalog)

    @low_pass.setter
    def low_pass(self, mode):
        _mode = eval('LowpassFilterModeAnalogEnum.' + mode).value
        self.APx.BenchMode.Setup.InputSettings(
            APxInputSelection.Input1).LowpassFilterAnalog = _mode

    @property
    def weighting(self):
        return str(self.APx.BenchMode.Setup.InputSettings(APxInputSelection.Input1).WeightingFilter)

    @weighting.setter
    def weighting(self, mode):
        _mode = eval('SignalPathWeightingFilterTypeEnum.' + mode).value
        self.APx.BenchMode.Setup.InputSettings(
            APxInputSelection.Input1).WeightingFilter = _mode
