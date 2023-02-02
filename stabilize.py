from pyrpl import Pyrpl
from pyrpl.async_utils import sleep

import numpy as np
from scipy.signal import find_peaks

class Laser:
    def __init__(self):
        self.transmission = None
        self.peaks = None

DRIVE_FREQUENCY = 1e3

p = Pyrpl(config="scanning-cavity-lock")
r = p.rp

r.scope.input1 = 'in2'
r.scope.input2 = 'in1'

r.scope.trigger_source = 'ch1_positive_edge'
r.scope.trigger_delay = 0
r.scope.threshold = 0.1
r.scope.hysteresis = 0.01

r.scope.duration = 2/DRIVE_FREQUENCY
r.scope.trace_average = 1000

try:
    while True:
        trace = r.scope.curve_async()

        r.asg0.setup(frequency=DRIVE_FREQUENCY, amplitude=0.5, offset=0.5, waveform='sin', trigger_source='immediately', output_direct='out1')
        sleep(0.01)

        control_laser = Laser()
        target_lasers = [Laser()]

        control_laser.transmission, target_lasers[0].transmission = trace.result()

        control_laser.peaks, _ = find_peaks(control_laser.transmission, height=0.2)
        target_lasers[0].peaks, _ = find_peaks(target_lasers[0].transmission, height=-0.011)

        for index, (control_peak, target_peak) in enumerate(zip(control_laser.peaks, target_lasers[0].peaks)):
            delta = r.scope.times[target_peak] - r.scope.times[control_peak]
            print(f"Control: {r.scope.times[control_peak]*1e3:.3f} ms, Target: {r.scope.times[target_peak]*1e3:.3f} ms, Delta: {delta*1e3:.3f} ms.")
except KeyboardInterrupt:
    pass