import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def infrared_sensor_signal(duration=2, sampling_rate=10, threshold=0.01):
    """
    Bangkitkan sinyal keluaran sensor inframerah berbasis hukum Stefan-Boltzmann dan ubah ke bentuk digital.
    
    Parameters:
    duration: Durasi sinyal (detik)
    sampling_rate: Laju sampling (Hz)
    threshold: Ambang batas untuk sinyal digital (Volt)
    
    Returns:
    t_fine: Array waktu yang dihaluskan
    V_out_digital: Sinyal keluaran dalam bentuk digital (0 atau 1)
    """
    # Constants
    emissivity = 0.95
    area = 0.01
    ambient_temp = 35
    sigma = 5.67e-8  # Stefan-Boltzmann constant (W/m^2K^4)

    # Time array
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Simulate random object temperatures (T_obj) within range
    T_obj = np.random.uniform(-50, 300, size=len(t))

    # Calculate output voltage based on Stefan-Boltzmann law
    V_out = sigma * emissivity * area * (T_obj**4 - ambient_temp**4)

    # Convert to digital signal based on threshold
    V_out_digital = (V_out > threshold).astype(int)  # 1 if V_out > threshold, else 0

    # Interpolation for smoothing
    t_fine = np.linspace(0, duration, int(sampling_rate * duration * 10), endpoint=False)
    interp_func = interp1d(t, V_out_digital, kind='nearest', bounds_error=False, fill_value="extrapolate")
    V_out_digital_smooth = interp_func(t_fine)

    return t_fine, V_out_digital_smooth
