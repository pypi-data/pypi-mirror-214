from .ap_enum import SwitcherAddressEnum, SwitcherChannelSelectionEnum


class InputSwitcher:
    def __init__(self, apx):
        self.APx = apx

    @property
    def switcher_enabled(self):
        return self.APx.BenchMode.Setup.UseInputSwitcher

    @switcher_enabled.setter
    def switcher_enabled(self, value):
        self.APx.BenchMode.Setup.UseInputSwitcher = value

    def set_cha(self, address, channel):
        _address = eval('SwitcherAddressEnum.' + address).value
        _channel = eval('SwitcherChannelSelectionEnum.' + channel).value

        self.APx.BenchMode.Setup.InputSwitcherConfiguration.SetChannelA(_address,
                                                                        _channel)

    def set_chb(self, address, channel):
        _address = eval('SwitcherAddressEnum.' + address).value
        _channel = eval('SwitcherChannelSelectionEnum.' + channel).value

        self.APx.BenchMode.Setup.InputSwitcherConfiguration.SetChannelB(_address,
                                                                        _channel)
