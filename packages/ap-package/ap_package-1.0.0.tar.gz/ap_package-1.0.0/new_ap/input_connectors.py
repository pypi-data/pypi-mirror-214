# output_connectors.py
from .apx500 import APx500
from .ap_enum import *


# from ap.setup.input_configuration import InputConfiguration
# from ap.setup.output_configuration import OutputConfiguration


class InputConnector(APx500):
    def __init__(self, apx, connector_type, channel):
        super().__init__()
        self.APx = apx
        channel = APxInputSelection.Input1 if channel == 'input1' else APxInputSelection.Input2
        _connector = eval('InputConnectorTypeEnum.' + connector_type).value
        self.APx.BenchMode.Setup.InputConnector.Type = _connector
        self.APx.BenchMode.Setup.InputSettings(channel).InputConnector.Type = _connector

        # self.input_config = InputConfiguration(self.APx)
        # self.output_config = OutputConfiguration(self.APx)

    # Configure input and output configurations
    def configure_io(self, input_config: dict, output_config: dict):
        for key, value in input_config.items():
            setattr(self.input_config, key, value)

        for key, value in output_config.items():
            setattr(self.output_config, key, value)

    # Other methods related to Connector...


class InputAnalog(InputConnector):
    def __init__(self, apx, connector_type, channel):
        super().__init__(apx, connector_type, channel)

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

    def channel(self, channel):
        """
        如果设置channles为1，那么channel可以选择 ch1或者Ch2
        :param channel: SingleInputChannelIndex.Ch1,SingleInputChannelIndex.Ch2
        :return:
        """
        _channel = eval('SingleInputChannelIndex.' + channel).value
        self.APx.BenchMode.Setup.AnalogInput.SingleInputChannel = _channel

    @property
    def termination_ch1(self):
        t = AP500.APx.BenchMode.Setup.AnalogInput.GetTermination(InputChannelIndex.Ch1)
        return str(t), int(t)

    @termination_ch1.setter
    def termination_ch1(self, value):
        """

        :param value: 【ap_enum.AnalogInputTerminationEnum】InputTermination_600
        :return:
        """
        value = eval('AnalogInputTermination.' + value).value
        APx.BenchMode.Setup.AnalogInput.SetTermination(InputChannelIndex.Ch1,
                                                       value)

    @property
    def termination_ch2(self):
        t = AP500.APx.BenchMode.Setup.AnalogInput.GetTermination(InputChannelIndex.Ch1)
        return str(t), int(t)

    @termination_ch2.setter
    def termination_ch2(self, value):
        """

                :param value: 【ap_enum.AnalogInputTerminationEnum】InputTermination_600
                :return:
                """
        value = eval('AnalogInputTermination.' + value).value
        APx.BenchMode.Setup.AnalogInput.SetTermination(InputChannelIndex.Ch2,
                                                       value)

    def eq(self):
        pass


# ... Analog 类代码 ...

class InputDigital(InputConnector):
    def __init__(self, apx, connector_type, channel):
        super().__init__(apx, connector_type, channel)

    @property
    def bit_depth(self):
        return self.APx.BenchMode.Setup.DigitalInput.BitDepth

    @bit_depth.setter
    def bit_depth(self, value):
        if value < 8:
            raise ValueError('bit depth must be greater than 8')
        self.APx.BenchMode.Setup.DigitalInput.BitDepth = value

    @property
    def input_termination(self):
        """
                75欧姆 termination
        :return: True or False
        """
        input_config = self.APx.BenchMode.Setup.DigitalInput
        if 'unbalanced' in self.connector_type.lower():
            return input_config.UnbalancedInputTermination
        else:
            return input_config.BalancedInputTermination

    @input_termination.setter
    def input_termination(self, value):
        """
        75欧姆 termination
        :param value: True or False
        :return:
        """
        input_config = self.APx.BenchMode.Setup.DigitalInput
        if not self.connector_type:
            raise ValueError('connector type must be defined')
        if 'unbalanced' in self.connector_type.lower():
            input_config.UnbalancedInputTermination = value
        else:
            input_config.BalancedInputTermination = value

    @property
    def scale_freq_by(self):
        return str(self.APx.BenchMode.Setup.DigitalInput.ScaleFreqBy)

    @scale_freq_by.setter
    def scale_freq_by(self, value):
        """

        :param value:
        :return:
        """
        self.APx.BenchMode.Setup.DigitalInput.ScaleFreqBy = eval("InputFrequencyScalingTypeEnum." + value).value


# ... Digital 类代码 ...

class InputTransducerInterface(InputConnector):
    pass


# ... TransducerInterface 类代码 ...

class InputASIO(InputConnector):
    pass
# ... ASIO 类代码 ...
