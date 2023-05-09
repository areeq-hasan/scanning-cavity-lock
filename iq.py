from pyrpl import Pyrpl
from pyrpl.async_utils import sleep

import numpy as np

import matplotlib.pyplot as plt

p = Pyrpl(config="scanning-cavity-lock")
r = p.rp

r.iq0.setup(input='in1', frequency=1e3, phase=0, quadrature_factor=1, output_signal='quadrature')

r.scope.input1 = 'asg0'
r.scope.input2 = 'iq0'

r.scope.trigger_source = 'ch1_positive_edge'
r.scope.trigger_delay = 0
r.scope.threshold = 0.1
r.scope.hysteresis = 0.01

r.scope.decimation = 16
r.scope.trace_average = 1000

trace = r.scope.curve_async()

r.asg0.setup(frequency=1e3, amplitude=0.5, offset=0.5, waveform='sin', trigger_source='immediately', output_direct='out1')
sleep(0.01)

drive_trace, cavity_trace = trace.result()

print(np.sum(cavity_trace))

plt.plot(r.scope.times, drive_trace, r.scope.times, cavity_trace)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()