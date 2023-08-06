from .ap_enum import OutputChannelIndexEnum
class Generator:
    def __init__(self, APx):
        self.APx = APx

    @property
    def on_false(self):
        return self.APx.BenchMode.Generator.On

    @on_false.setter
    def on_false(self, status):
        self.APx.BenchMode.Generator.On = status

    @property
    def waveform(self):
        return self.APx.BenchMode.Generator.Waveform

    @waveform.setter
    def waveform(self, waveform):
        self.APx.BenchMode.Generator.Waveform = waveform

    @property
    def levels_track_ch1(self):
        return self.APx.BenchMode.Generator.Levels.TrackFirstChannel

    @levels_track_ch1.setter
    def levels_track_ch1(self, status):
        self.APx.BenchMode.Generator.Levels.TrackFirstChannel = status

    def get_levels(self, channel):
        return self.APx.BenchMode.Generator.Levels.GetValue(channel)

    def set_levels(self, channel, level):
        """

        :param level: "133mvrms"
        :return:
        """
        _channel = eval('OutputChannelIndexEnum.' + channel).value
        self.APx.BenchMode.Generator.Levels.SetValue(_channel, level)

    @property
    def levels_unit(self):
        return self.APx.BenchMode.Generator.Levels.Unit

    @levels_unit.setter
    def levels_unit(self, unit):
        self.APx.BenchMode.Generator.Levels.Unit = unit

    @property
    def offset(self, channel):
        return self.APx.BenchMode.Generator.Levels.GetOffsetValue(channel)

    @offset.setter
    def offset(self, channel, level):
        self.APx.BenchMode.Generator.SetOffsetValue.SetValue(channel, level)

    @property
    def offset_unit(self):
        return self.APx.BenchMode.Generator.Levels.OffsetUnit

    @offset_unit.setter
    def offset_unit(self, unit):
        self.APx.BenchMode.Generator.Levels.OffsetUnit = unit

    @property
    def frequency(self):
        """

        :return: str  [200khz, 200%hz]
        """
        _frequency = self.APx.BenchMode.Generator.Frequency
        return _frequency.Value, _frequency.Values

    @frequency.setter
    def frequency(self, frequency):
        """

        :param frequency: 200
        :return:
        """

        self.APx.BenchMode.Generator.Frequency.Value = frequency

    @property
    def frequency_unit(self):
        """

        :return: str HZ
        """
        return self.APx.BenchMode.Generator.Frequency.Unit

    @frequency_unit.setter
    def frequency_unit(self, unit):
        """

        :param unit: str KHZ
        :return:
        """
        self.APx.BenchMode.Generator.Frequency.Unit = unit
