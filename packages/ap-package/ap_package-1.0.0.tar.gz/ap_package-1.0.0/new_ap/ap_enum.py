import enum

from AudioPrecision.API import APxOperatingMode, OutputConnectorType, InputConnectorType, BenchModeMeterType, \
    InputFrequencyScalingType, \
    APxInputSelection, SingleInputChannelIndex, AnalogInputTermination, SwitcherAddress, SwitcherChannelSelection, \
    LowpassFilterModeAnalog, SignalPathWeightingFilterType, OutputChannelIndex


class ChangeMode(enum.Enum):
    """
    切换模式
    """
    bench_mode = APxOperatingMode.BenchMode
    sequence_mode = APxOperatingMode.SequenceMode


class APxConnectorType(enum.Enum):
    AnalogUnbalanced = OutputConnectorType.AnalogUnbalanced
    AnalogBalanced = OutputConnectorType.AnalogBalanced
    # AnalogBalancedAdcTest = OutputConnectorType.AnalogBalancedAdcTest
    DigitalUnbalanced = OutputConnectorType.DigitalUnbalanced
    DigitalBalanced = OutputConnectorType.DigitalBalanced
    DigitalOptical = OutputConnectorType.DigitalOptical
    TransducerInterface = OutputConnectorType.TransducerInterface
    ASIO = OutputConnectorType.ASIO
    # none = eval('OutputConnectorType.' + 'None')


class InputConnectorTypeEnum(enum.Enum):
    AnalogUnbalanced = InputConnectorType.AnalogUnbalanced
    AnalogBalanced = InputConnectorType.AnalogBalanced
    # AnalogBalancedAdcTest = OutputConnectorType.AnalogBalancedAdcTest
    DigitalUnbalanced = InputConnectorType.DigitalUnbalanced
    DigitalBalanced = InputConnectorType.DigitalBalanced
    DigitalOptical = InputConnectorType.DigitalOptical
    TransducerInterface = InputConnectorType.TransducerInterface
    ASIO = InputConnectorType.ASIO


class BenchModeMeterTypeEnum(enum.Enum):
    AverageJitterLevelMeter = BenchModeMeterType.AverageJitterLevelMeter
    BandpassLevelMeter = BenchModeMeterType.BandpassLevelMeter
    BitErrorMeter = BenchModeMeterType.BitErrorMeter
    BitsMeter = BenchModeMeterType.BitsMeter
    RmsLevelMeter = BenchModeMeterType.RmsLevelMeter
    ThdNRatioMeter = BenchModeMeterType.ThdNRatioMeter
    FrequencyMeter = BenchModeMeterType.FrequencyMeter


class InputFrequencyScalingTypeEnum(enum.Enum):
    InputRate = InputFrequencyScalingType.InputRate
    OutputSampleRate = InputFrequencyScalingType.OutputSampleRate
    FixedRate = InputFrequencyScalingType.FixedRate


class APxInputSelectionEnum(enum.Enum):
    input_1 = APxInputSelection.Input1
    input_2 = APxInputSelection.Input2


class SingleInputChannelIndexEnum(enum.Enum):
    Ch1 = SingleInputChannelIndex.Ch1
    Ch2 = SingleInputChannelIndex.Ch2


class AnalogInputTerminationEnum(enum.Enum):
    InputTermination_600 = AnalogInputTermination.InputTermination_600


class SwitcherAddressEnum(enum.Enum):
    Switcher0 = SwitcherAddress.Switcher0
    Switcher1 = SwitcherAddress.Switcher1
    Switcher2 = SwitcherAddress.Switcher2
    Switcher3 = SwitcherAddress.Switcher3
    Switcher4 = SwitcherAddress.Switcher4
    Switcher5 = SwitcherAddress.Switcher5
    Switcher6 = SwitcherAddress.Switcher6
    Switcher7 = SwitcherAddress.Switcher7
    Switcher8 = SwitcherAddress.Switcher8
    Switcher9 = SwitcherAddress.Switcher9
    Switcher10 = SwitcherAddress.Switcher10
    Switcher11 = SwitcherAddress.Switcher11
    Switcher12 = SwitcherAddress.Switcher12
    Switcher13 = SwitcherAddress.Switcher13
    Switcher14 = SwitcherAddress.Switcher14
    Switcher15 = SwitcherAddress.Switcher15


class SwitcherChannelSelectionEnum(enum.Enum):
    Ch1 = SwitcherChannelSelection.Ch1
    Ch2 = SwitcherChannelSelection.Ch2
    Ch3 = SwitcherChannelSelection.Ch3
    Ch4 = SwitcherChannelSelection.Ch4
    Ch5 = SwitcherChannelSelection.Ch5
    Ch6 = SwitcherChannelSelection.Ch6
    Ch7 = SwitcherChannelSelection.Ch7
    Ch8 = SwitcherChannelSelection.Ch8
    Ch9 = SwitcherChannelSelection.Ch9
    Ch10 = SwitcherChannelSelection.Ch10
    Ch11 = SwitcherChannelSelection.Ch11
    Ch12 = SwitcherChannelSelection.Ch12
    Chnone = getattr(SwitcherChannelSelection, 'None')


class LowpassFilterModeAnalogEnum(enum.Enum):
    """
    low pass
    """
    AdcPassband = LowpassFilterModeAnalog.AdcPassband
    LpAes17_20k = LowpassFilterModeAnalog.LpAes17_20k
    LpAes17_40k = LowpassFilterModeAnalog.LpAes17_40k
    Butterworth = LowpassFilterModeAnalog.Butterworth
    Elliptic = LowpassFilterModeAnalog.Elliptic


class SignalPathWeightingFilterTypeEnum(enum.Enum):
    wt_A = SignalPathWeightingFilterType.wt_A
    wt_B = SignalPathWeightingFilterType.wt_B
    wt_C = SignalPathWeightingFilterType.wt_C
    wt_None = SignalPathWeightingFilterType.wt_None


class OutputChannelIndexEnum(enum.Enum):
    Ch1 = OutputChannelIndex.Ch1
    Ch2 = OutputChannelIndex.Ch2
    Ch3 = OutputChannelIndex.Ch3
    Ch4 = OutputChannelIndex.Ch4
    Ch5 = OutputChannelIndex.Ch5
    Ch6 = OutputChannelIndex.Ch6
    Ch7 = OutputChannelIndex.Ch7
    Ch8 = OutputChannelIndex.Ch8
    Ch9 = OutputChannelIndex.Ch9
    Ch10 = OutputChannelIndex.Ch10
    Ch11 = OutputChannelIndex.Ch11
    Ch12 = OutputChannelIndex.Ch12
    Ch13 = OutputChannelIndex.Ch13
    Ch14 = OutputChannelIndex.Ch14
    Ch15 = OutputChannelIndex.Ch15
    Ch16 = OutputChannelIndex.Ch16
