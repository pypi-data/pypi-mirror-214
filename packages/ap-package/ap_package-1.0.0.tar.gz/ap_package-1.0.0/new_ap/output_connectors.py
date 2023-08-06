# output_connectors.py
from .apx500 import APx500
from .ap_enum import *
# from ap.setup.input_configuration import InputConfiguration
# from ap.setup.output_configuration import OutputConfiguration


class OutputConnector(APx500):
    def __init__(self, apx, connector_type):
        super().__init__()
        self.APx = apx
        _connector = eval('APxConnectorType.' + connector_type).value
        self.APx.BenchMode.Setup.OutputConnector.Type = _connector

        # self.input_config = InputConfiguration(self.APx)
        # self.output_config = OutputConfiguration(self.APx)

    # Configure input and output configurations
    def configure_io(self, input_config: dict, output_config: dict):
        for key, value in input_config.items():
            setattr(self.input_config, key, value)

        for key, value in output_config.items():
            setattr(self.output_config, key, value)

    # Other methods related to Connector...


class Analog(OutputConnector):
    def __init__(self, apx, connector_type):
        super().__init__(apx, connector_type)

    def change_channel(self, channel: int):
        """
        切换通道
        :param channel:
        :return:
        """
        if channel not in (1, 2):
            print('请输入正确的通道数')
            return
        self.APx.BenchMode.Setup.AnalogOutput.ChannelCount = channel

    def eq(self):
        pass


# ... Analog 类代码 ...

class Digital(OutputConnector):
    def __init__(self, apx, connector_type):
        super().__init__(apx, connector_type)

    @property
    def output_ample_rate(self):
        return self.APx.BenchMode.Setup.DigitalOutput.SampleRate.Text

    @output_ample_rate.setter
    def output_ample_rate(self, value):
        """

        :param value: 12KHZ
        :return:
        """
        self.APx.BenchMode.Setup.DigitalOutput.SampleRate.Text = value


# ... Digital 类代码 ...

class TransducerInterface(OutputConnector):
    pass


# ... TransducerInterface 类代码 ...

class ASIO(OutputConnector):
    pass
# ... ASIO 类代码 ...
