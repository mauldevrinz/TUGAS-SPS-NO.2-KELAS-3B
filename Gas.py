import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def gas_signal(Vcc=5.0, Rl=10e3, k=1e3, n=-0.4, duration=2, sampling_rate=10):
    """
    Bangkitkan sinyal keluaran sensor gas berbasis hubungan matematis dengan interpolasi.
    
    Args:
    Vcc : float : Tegangan suplai (Volt)
    Rl : float : Resistor beban (Ohm)
    k : float : Konstanta kalibrasi
    n : float : Eksponen sensitivitas
    duration : float : Durasi sinyal (detik)
    sampling_rate : float : Laju sampling (Hz)
    
    Returns:
    t_fine : ndarray : Array waktu halus
    V_out_smooth : ndarray : Sinyal tegangan keluaran yang dihaluskan
    """
    # Time array
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Simulate random gas concentrations (C) within range (300 to 10000 ppm)
    concentrations = np.random.uniform(300, 10000, size=len(t))

    # Calculate sensor resistance (Rs) and output voltage (V_out)
    Rs = k * (concentrations ** n)  # Rs = k * C^n
    V_out = Vcc * (Rl / (Rs + Rl))  # Voltage divider formula

    # Interpolation for smoothing
    # Create a finer time array for interpolation
    t_fine = np.linspace(0, duration, int(sampling_rate * duration * 10), endpoint=False)
    interp_func = interp1d(t, V_out, kind='cubic', bounds_error=False, fill_value="extrapolate")
    V_out_smooth = interp_func(t_fine)

    return t_fine, V_out_smooth


