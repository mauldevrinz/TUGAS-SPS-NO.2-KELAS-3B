import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def flame_signal(R12=1000, R13=2000, R11=1500, R10=1000, R8=500, rbe=100, VH=2, K=1e6, RM2=16000, duration=10, sampling_rate=10):
    """
    Bangkitkan sinyal keluaran sensor flame berbasis hubungan matematis dengan interpolasi.
    
    Parameters:
    R12, R13, R11, R10, R8, rbe: Resistor dalam rangkaian (Ohm)
    VH: Tegangan sumber (Volt)
    K: Gain penguat
    RM2: Resistansi memristor (Ohm)
    duration: Durasi sinyal (detik)
    sampling_rate: Laju sampling (Hz)
    
    Returns:
    t_fine: Array waktu yang dihaluskan
    Vout_smooth: Sinyal tegangan keluaran yang dihaluskan
    """
    # Array waktu
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    I1 = np.random.uniform(1e-6, 1e-3, size=len(t))

    # Hitung Vout berdasarkan rumus
    Vout2 = (R12 + R13) * R11 / ((R10 + R11) * R12) * VH * R13 / R12
    Vout = (K * RM2 * (R8 + rbe)) / (I1 * K)

    # Interpolasi untuk sinyal halus
    t_fine = np.linspace(0, duration, int(sampling_rate * duration * 10), endpoint=False)
    interp_func = interp1d(t, Vout, kind='cubic', bounds_error=False, fill_value="extrapolate")
    Vout_smooth = interp_func(t_fine)

    return t_fine, Vout_smooth
