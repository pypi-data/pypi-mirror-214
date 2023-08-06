from ..ap_enum import BenchModeMeterTypeEnum, APxInputSelectionEnum


class Meters:
    def __init__(self, apx):
        self.Apx = apx

    @property
    def enabled(self):
        return self.APx.BenchMode.Meters.Enabled

    @enabled.setter
    def enabled(self, status):
        self.APx.BenchMode.Meters.Enabled = status

    def get_meter_unit(self, mode, input_channel):
        """

        :param mode:
        :param input_channel: APxInputSelectionEnum
        :return:
        """
        mode = eval('BenchModeMeterTypeEnum.' + mode).value
        input_channel = eval('APxInputSelectionEnum.' + input_channel).value
        return self.Apx.BenchMode.Meters.GetDisplaySettings(mode, input_channel).Unit

    def _get_meter_value(self, modes, input_channel):
        """

        :param modes:
        :param input_channel:
        :return: [1,2]
        """
        modes = eval('BenchModeMeterTypeEnum.' + modes).value
        input_channel = eval('APxInputSelectionEnum.' + input_channel).value
        return self.BenchMode.Meters.GetReadings(modes, input_channel)

    def get_meter_value(self, modes, input_channel):
        """

        :param modes:
        :param input_channel:
        :return:
        """
        _modes=modes
        _input_channel=input_channel
        modes = eval('BenchModeMeterTypeEnum.' + modes).value
        input_channel = eval('APxInputSelectionEnum.' + input_channel).value
        unit = self.get_meter_unit(_modes, _input_channel)
        return [str(round(i, 3)) + unit for i in self.Apx.BenchMode.Meters.GetReadings(modes, input_channel)]

    def add_meter_type(self, meter_type, input_channel):
        """
        APx.BenchMode.Meters.Add(meterType, APxInputSelection.input)
        :param meter_type:
        :param input_channel:
        :return:
        """
        self.APx.BenchMode.Meters.Add(meter_type, input_channel)

    def show(self):
        self.APx.BenchMode.Meters.Show()
