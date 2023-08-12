from GUI import *
from Globals import *
from NiDAQ import *

global_vars = Globals()
daq = NiDAQ(global_vars)
GUI(global_vars, daq)
