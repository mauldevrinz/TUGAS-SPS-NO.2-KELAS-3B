import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def smoke_sensor_signal(duration=5, sampling_rate=10):
    """
    Simulate a smoke sensor signal based on datasheet equations.

    Parameters:
    - duration: Signal duration in seconds.
    - sampling_rate: Sampling rate in Hz.

    Returns:
    - t: Time array.
    - V_out: Output voltage signal from the sensor.
    """
    Vc = 5.0             # Sensor supply voltage (V)
    RL = 10000           # Load resistance (10 kOhm)
    R0 = 10000           # Sensor resistance in clean air (10 kOhm)
    a = 0.38             # Calibration constant from datasheet
    b = 0.5              # Calibration constant from datasheet

    # Generate time array
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Simulate gas concentration in ppm
    gas_concentration = np.random.uniform(300, 10000, size=len(t))

    # Calculate Rs/R0 from gas concentration using the calibration curve
    Rs_R0 = 10 ** (-a * np.log10(gas_concentration) + b)

    # Calculate sensor resistance Rs
    Rs = Rs_R0 * R0

    # Calculate sensor output voltage V_out
    V_out = (Vc * RL) / (Rs + RL)

    # Interpolation for smoothing
    # Create a finer time array for interpolation
    t_fine = np.linspace(0, duration, int(sampling_rate * duration * 10), endpoint=False)
    interp_func = interp1d(t, V_out, kind='cubic', bounds_error=False, fill_value="extrapolate")
    V_out_smooth = interp_func(t_fine)

    return t_fine, V_out_smooth