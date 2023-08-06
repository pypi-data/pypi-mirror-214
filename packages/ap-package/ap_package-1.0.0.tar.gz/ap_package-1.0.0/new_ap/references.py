class References:
    def __init__(self, apx):
        self.APx = apx

    def analog_dbra(self, value, unit):
        self.APx.BenchMode.Setup.References.AnalogInputReferences.dBrA.Unit = unit
        self.APx.BenchMode.Setup.References.AnalogInputReferences.dBrA.Value = value

    def digital_dbra(self, value, unit):
        self.APx.BenchMode.Setup.References.DigitalInputReferences.dBFS.Unit = unit
        self.APx.BenchMode.Setup.References.DigitalInputReferences.dBFS.Value = value
