import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def voltage_sensor_signal(amplitude=5, frequency=20, duration=5, sampling_rate=10):
    """
    Simulate the voltage sensor signal based on a voltage divider circuit.

    Parameters:
    - amplitude: The peak amplitude of the voltage signal.
    - frequency: The frequency of the voltage signal.
    - duration: Duration of the signal in seconds.
    - sampling_rate: Sampling rate in Hz.

    Returns:
    - t: Time array.
    - voltage_signal: Simulated voltage signal from the sensor.
    """
    phase = 0
    R1 = 30000  # Resistance 1 (Ohms)
    R2 = 7500   # Resistance 2 (Ohms)
    V_in = 5.0  # Input voltage (V)

    # Generate time array
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Calculate the output voltage using the voltage divider formula
    V_out = V_in * (R2 / (R1 + R2))

    # Add a sine wave component to simulate voltage variations
    voltage_signal = V_out + amplitude * np.sin(2 * np.pi * frequency * t + phase)

    # Interpolation for smoothing
    # Create a finer time array for interpolation
    t_fine = np.linspace(0, duration, int(sampling_rate * duration * 10), endpoint=False)  # Changed to endpoint=False

    # Ensure t_fine does not exceed the maximum value of t
    t_fine = t_fine[t_fine < duration]  # This line ensures t_fine does not exceed duration

    interp_func = interp1d(t, voltage_signal, kind='cubic', bounds_error=False, fill_value="extrapolate")
    voltage_signal_smooth = interp_func(t_fine)

    return t_fine, voltage_signal_smooth