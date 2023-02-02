from pyrpl import Pyrpl
from pyrpl.async_utils import sleep

import numpy as np
from scipy.signal import find_peaks

DRIVE_FREQUENCY = 1e3

p = Pyrpl(config="scanning-cavity-lock")
r = p.rp

r.scope.input1 = 'asg0'
r.scope.input2 = 'in2'

r.scope.trigger_source = 'ch1_positive_edge'
r.scope.trigger_delay = 0
r.scope.threshold = 0.1
r.scope.hysteresis = 0.01

r.scope.duration = 2/DRIVE_FREQUENCY
r.scope.trace_average = 1000

try:
    while True:
        trace = r.scope.curve_async()

        r.asg0.setup(frequency=DRIVE_FREQUENCY, amplitude=0.2, offset=0, waveform='sin', trigger_source='immediately', output_direct='out1')
        sleep(0.01)

        drive_trace, cavity_trace = trace.result()

        drive_troughs, _ = find_peaks(1 - drive_trace)

        drive_center, _ = find_peaks(drive_trace[drive_troughs[0]:drive_troughs[1]])
        drive_center = drive_troughs[0] + drive_center[0]

        cavity_peaks, _ = find_peaks(cavity_trace[drive_troughs[0]:drive_troughs[1]], height=0.1)
        cavity_peaks = drive_troughs[0] + cavity_peaks
        cavity_center = np.rint(np.mean(cavity_peaks)).astype(int)

        center_difference = r.scope.times[cavity_center] - r.scope.times[drive_center]
        phase_shift = 360 * DRIVE_FREQUENCY * center_difference

        print(f"Phase Shift: {phase_shift:.5f}°")
except KeyboardInterrupt:
    pass