# apx500.py
from AudioPrecision.API import *
from System.IO import Directory, Path

from .ap_enum import ChangeMode, APxConnectorType, BenchModeMeterTypeEnum
from .output_connectors import Analog, Digital, TransducerInterface, ASIO
from .input_connectors import InputDigital, InputAnalog, InputTransducerInterface, InputASIO
from .query import Query
from .generator import Generator
from .decorators import handle_exceptions
from .references import References
from .measurement.acoustic_response import AcousticResponse
from .measurement.continuous_sweep import ContinuousSweep
from .measurement.fft import Fft
from .measurement.meters import Meters
from .measurement.recorder import Recorder
from .measurement.sweep import Sweep
from .measurement.transfer_function import TransferFunction
from .input_config import InputConfiguration
from .input_switcher import InputSwitcher


class APx500:
    def __init__(self):
        # 都是一些类
        self.output_configuration = None
        self.input_configuration = None
        self.APx = None
        self.output_connector_instance = None  # 添加 connector_instance 属性
        self.input_connector_instance = None
        self.query = None
        self.generator = None
        self.analyzer = None
        self.input_switcher = None
        self.meter= None

    def open_project(self, file_path):
        """
        打开工程
        :param file_path: 工程路径
        :return:  APx500_Application
        """
        filename = file_path
        directory = Directory.GetCurrentDirectory()
        fullpath = Path.Combine(directory, filename)
        self.APx = APx500_Application()
        self.APx.OpenProject(fullpath)
        self.generator = Generator(self.APx)
        self.reference = References(self.APx)
        self.input_configuration = InputConfiguration(self.APx)
        self.input_switcher = InputSwitcher(self.APx)
        self.meter = Meters(self.APx)

        return self.APx

    def close_project(self):
        """
        关闭工程
        :return:
        """
        if self.APx is not None:
            self.APx.Exit()

    def change_mode(self, mode='bench_mode'):
        """
        切换到bench mode模式
        :return:
        """
        try:
            mode = eval('ChangeMode.' + mode).value
        except AttributeError as e:
            print(e)
            print(' 请输入正确的模式')
            return
        self.APx.OperatingMode = mode

    def output_change_connector(self, connector_type: str):
        """
        output connector 切换
        :param connector_type:【ap_enum.APxConnectorType.name】 "AnalogUnbalanced"/"DigitalUnbalanced"
        :return:
        """
        copy_connector_type = connector_type
        if "unbalanced" in connector_type.lower():
            connector_type = connector_type.lower().split("unbalanced")[0]
        elif "balanced" in connector_type.lower():
            connector_type = connector_type.lower().split("balanced")[0]
        else:
            connector_type = connector_type.lower()

        connector_class = {
            'analog': Analog,
            'digital': Digital,
            'transducerinterface': TransducerInterface,
            'asio': ASIO,
            "digitaloptical": Digital
        }.get(connector_type.lower())

        if not connector_class:
            raise ValueError(f"Invalid connector_type: {copy_connector_type}")

        self.output_connector_instance = connector_class(self.APx, copy_connector_type)
        self.query = Query(self.APx)
        return self.output_connector_instance

    def input_change_connector(self, connector_type: str, input_channel):
        """
        input connector 切换
        :param connector_type:  【ap_enum.InputConnectorTypeEnum.name】 "AnalogUnbalanced"/"DigitalUnbalanced"
        :param input_channel: "input1"/"input2"
        :return:
        """
        copy_connector_type = connector_type
        if "unbalanced" in connector_type.lower():
            connector_type = connector_type.lower().split("unbalanced")[0]
        elif "balanced" in connector_type.lower():
            connector_type = connector_type.lower().split("balanced")[0]
        else:
            connector_type = connector_type.lower()

        connector_class = {
            'analog': InputAnalog,
            'digital': InputDigital,
            'transducerinterface': InputTransducerInterface,
            'asio': InputASIO
        }.get(connector_type.lower())

        if not connector_class:
            raise ValueError(f"Invalid connector_type: {copy_connector_type}")

        self.input_connector_instance = connector_class(self.APx, copy_connector_type, input_channel)
        self.query = Query(self.APx)
        return self.input_connector_instance
