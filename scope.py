from pyrpl import Pyrpl
from pyrpl.async_utils import sleep

import numpy as np
from scipy.signal import find_peaks

import matplotlib.pyplot as plt

DRIVE_FREQUENCY = 1e3

p = Pyrpl(config="scanning-cavity-lock")
r = p.rp

r.scope.input1 = 'asg0'
r.scope.input2 = 'in1'

r.scope.trigger_source = 'ch1_positive_edge'
r.scope.trigger_delay = 0
r.scope.threshold = 0.1
r.scope.hysteresis = 0.01

r.scope.duration = 2/DRIVE_FREQUENCY
r.scope.trace_average = 1000

trace = r.scope.curve_async()

r.asg0.setup(frequency=DRIVE_FREQUENCY, amplitude=0.5, offset=0.5, waveform='sin', trigger_source='immediately', output_direct='out1')
sleep(0.01)

drive_trace, cavity_trace = trace.result()

drive_troughs, _ = find_peaks(1 - drive_trace)

plt.plot(r.scope.times, drive_trace)
plt.plot(r.scope.times, cavity_trace)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")

plt.show()