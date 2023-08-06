"""
导入C#库
"""
import clr

clr.AddReference("System.Drawing")  # Needed for Dialog Boxes
clr.AddReference("System.Windows.Forms")  # Needed for Dialog Boxes
# clr.AddReference("AudioPrecision.API2")  # Adding Reference to the APx API
# clr.AddReference("AudioPrecision.API")  # Adding Reference to the APx API

clr.AddReference(r"D:\AudioPrecision.API2")  # Adding Reference to the APx API
clr.AddReference(r"D:\AudioPrecision.API")  # Adding Reference to the APx API
