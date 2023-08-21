from GUI import *
from Globals import *
from NiDAQ import *
from Testthread import *

global_vars = Globals()
t1 = Testthread(global_vars)
t1.threading()
daq = NiDAQ(global_vars)
GUI(global_vars, daq)
