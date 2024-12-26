import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt

# Import sensor signal functions
from Gas import gas_signal
from smoke import smoke_sensor_signal
from fire import flame_signal
from Voltage import voltage_sensor_signal
from infrared import infrared_sensor_signal

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, parent, label_text, values, selection_callback):
        super().__init__(parent)

        self.label = customtkinter.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.var = customtkinter.StringVar(value=values[0])  # Default to first value
        for i, value in enumerate(values):
            radiobutton = customtkinter.CTkRadioButton(
                self, text=value, variable=self.var, value=value, command=selection_callback
            )
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

    def get(self):
        return self.var.get()

class MyNewFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add matplotlib figure to the frame
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure frame grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_graph(self, t, signal, title):
        """Update the matplotlib graph with new data."""
        self.ax.clear()
        self.ax.plot(t, signal, label=title)
        self.ax.set_title(f"{title} Signal")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.legend()
        self.canvas.draw()

class MyControlFrame(customtkinter.CTkFrame):
    def __init__(self, parent, amplitude_callback, frequency_callback):
        super().__init__(parent)

        # Amplitude slider for noise
        self.amplitude_label = customtkinter.CTkLabel(self, text="Noise Amplitude")
        self.amplitude_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.amplitude_slider = customtkinter.CTkSlider(self, from_=0, to=10, command=amplitude_callback)
        self.amplitude_slider.set(1)  # Default value
        self.amplitude_slider.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Amplitude value display
        self.amplitude_value = customtkinter.CTkLabel(self, text="1.0")
        self.amplitude_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Frequency slider for noise
        self.frequency_label = customtkinter.CTkLabel(self, text="Noise Frequency")
        self.frequency_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.frequency_slider = customtkinter.CTkSlider(self, from_=1, to=100, command=frequency_callback)
        self.frequency_slider.set(10)  # Default value
        self.frequency_slider.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Frequency value display
        self.frequency_value = customtkinter.CTkLabel(self, text="10.0")
        self.frequency_value.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Configure frame grid
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_columnconfigure((0, 1), weight=1)


class MyOperationFrame(customtkinter.CTkFrame):
    def __init__(self, parent, low_pass_callback, moving_average_callback):
        super().__init__(parent)

        # Button for Low Pass Filter
        self.low_pass_button = customtkinter.CTkButton(self, text="Low Pass Filter", command=low_pass_callback)
        self.low_pass_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Button for Moving Average
        self.moving_average_button = customtkinter.CTkButton(self, text="Moving Average", command=moving_average_callback)
        self.moving_average_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

class MyResultFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add matplotlib figure to the frame
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure frame grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_graph(self, t, signal, title, color='red'):
        self.ax.clear()
        self.ax.plot(t, signal, label=title, color=color)
        self.ax.set_title(f"{title} Signal")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.legend()
        self.canvas.draw()

class MyDFTFrame(customtkinter.CTkFrame):
    def __init__(self, parent, sensor_signal_callback, filtered_signal_callback):
        super().__init__(parent)

        # Button for Discrete Fourier Transform of the sensor signal
        self.dft_sensor_button = customtkinter.CTkButton(self, text="DFT Sensor Signal", command=sensor_signal_callback)
        self.dft_sensor_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Button for Discrete Fourier Transform of the filtered signal
        self.dft_filtered_button = customtkinter.CTkButton(self, text="DFT Filtered Signal", command=filtered_signal_callback)
        self.dft_filtered_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

class MyDFTGraphFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add matplotlib figure to the frame
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure frame grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_graph(self, f, signal, title, color='purple'):
        """Update the DFT graph with frequency domain data."""
        self.ax.clear()
        self.ax.plot(f, np.abs(signal), label=title, color=color)
        self.ax.set_title(f"{title} DFT")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude")
        self.ax.legend()
        self.canvas.draw()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graphic Visualization by Akhmad Maulvin Nazir Zakaria")
        self.geometry("1500x800")
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Sensor options
        self.sensor_options = ["Gas", "Smoke", "Flame", "Voltage", "Infrared"]
        self.amplitude = 1  # Default noise amplitude
        self.frequency = 10  # Default noise frequency

        # Radiobutton frame
        self.radiobutton_frame = MyRadiobuttonFrame(
            self, "Select Sensor", self.sensor_options, self.update_graph
        )
        self.radiobutton_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Frame for displaying original signal
        self.signal_frame = MyNewFrame(self)
        self.signal_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Frame for control sliders
        self.control_frame = MyControlFrame(self, self.update_amplitude, self.update_frequency)
        self.control_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # Frame for displaying noise signal
        self.noise_frame = MyNewFrame(self)
        self.noise_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # Operation frame for filter buttons
        self.operation_frame = MyOperationFrame(self, self.apply_low_pass_filter, self.apply_moving_average)
        self.operation_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Frame for displaying result of operations
        self.result_frame = MyResultFrame(self)
        self.result_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # DFT Frame
        self.dft_frame = MyDFTFrame(self, self.show_dft_sensor_signal, self.show_dft_filtered_signal)
        self.dft_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # Frame for displaying DFT graph
        self.dft_graph_frame = MyDFTGraphFrame(self)
        self.dft_graph_frame.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

        # Display initial graph
        self.update_graph()

    def update_graph(self):
        """Update the original graph based on the selected sensor."""
        selected_sensor = self.radiobutton_frame.get()

        # Generate base signal for the selected sensor
        if selected_sensor == "Gas":
            t, signal = gas_signal()
        elif selected_sensor == "Smoke":
            t, signal = smoke_sensor_signal(duration=5, sampling_rate=5)
        elif selected_sensor == "Flame":
            t, signal = flame_signal()
        elif selected_sensor == "Voltage":
            t, signal = voltage_sensor_signal(amplitude=5, frequency=20, duration=5, sampling_rate=5)
        elif selected_sensor == "Infrared":
            t, signal = infrared_sensor_signal()
        else:
            t, signal = [], []

        # Store the signal and time for later use
        self.signal = signal
        self.t = t
        self.selected_sensor = selected_sensor

        # Update the original signal frame
        self.signal_frame.update_graph(t, signal, selected_sensor)

        # Apply noise dynamically
        self.apply_noise()

    def generate_noise(self):
        """Generate a sinusoidal noise signal based on slider values."""
        amplitude = self.amplitude  # Get the current amplitude from the slider
        frequency = self.frequency    # Get the current frequency from the slider
        t_noise = self.t             # Use the time array from the selected sensor signal
        noise_signal = amplitude * np.sin(2 * np.pi * frequency * t_noise)
        return noise_signal

    def apply_noise(self):
        """Apply noise dynamically based on slider values."""
        # Generate noise
        noise = self.generate_noise()

        # Scale the noise based on the maximum value of the sensor signal
        max_signal = np.max(np.abs(self.signal))
        scaled_noise = (self.amplitude / max_signal) * noise if max_signal != 0 else noise

        # Combine the sensor signal with the scaled noise
        noisy_signal = self.signal + scaled_noise

        # Update the noise signal frame
        self.noise_frame.update_graph(self.t, noisy_signal, f"{self.selected_sensor} + Noise")
        
    def apply_low_pass_filter(self):
        """Apply a low pass filter to the noisy signal."""
        # Define a low pass filter
        def low_pass_filter(signal, cutoff, fs, order=5):
            nyquist = 0.5 * fs
            normal_cutoff = cutoff / nyquist
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            y = filtfilt(b, a, signal)
            return y

        # Apply the filter
        self.result_signal = low_pass_filter(self.signal, cutoff=2.5, fs=20)
        self.result_frame.update_graph(self.t, self.result_signal, "Low Pass Filtered Signal")

    def apply_moving_average(self):
        """Apply a moving average filter to the noisy signal."""
        def moving_average(signal, window_size):
            return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

        # Apply the moving average
        self.result_signal = moving_average(self.signal, window_size=5)
        self.result_frame.update_graph(self.t, self.result_signal, "Moving Average Signal")

    def update_amplitude(self, value):
        """Update noise amplitude and display it."""
        self.amplitude = float(value)
        self.control_frame.amplitude_value.configure(text=f"{self.amplitude:.1f}")
        self.apply_noise()  # Update noise dynamically

    def update_frequency(self, value):
        """Update noise frequency and display it."""
        self.frequency = float(value)
        self.control_frame.frequency_value.configure(text=f"{self.frequency:.1f}")
        self.apply_noise()  # Update noise dynamically

    def show_dft_sensor_signal(self):
        """Display the DFT of the noisy sensor signal."""
        # Generate noise and add it to the sensor signal
        noisy_signal = self.signal + self.generate_noise()

        # Compute the DFT of the noisy signal
        f, dft_signal = self.compute_dft(noisy_signal)

        # Update the DFT graph with the noisy signal
        self.dft_graph_frame.update_graph(f, dft_signal, f"DFT of {self.selected_sensor}", color='purple')

    def show_dft_filtered_signal(self):
        """Display the DFT of the filtered signal."""
        if hasattr(self, 'result_signal'):  # Assuming result_signal holds the filtered data
            # Compute the DFT of the filtered signal
            f, dft_signal = self.compute_dft(self.result_signal)

            # Update the DFT graph with the filtered signal
            self.dft_graph_frame.update_graph(f, dft_signal, "DFT of Filtered Signal", color='purple')
        else:
            print("No filtered signal available.")

    def compute_dft(self, signal):
        N = len(signal)
        dft_result = np.zeros(N, dtype=complex)
        
        # Compute the DFT using the formula: X[k] = sum(x[n] * exp(-2pi * j * k * n / N)) for all n
        for k in range(N):
            for n in range(N):
                dft_result[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)
        
        # Calculate frequency bins
        sample_rate = 1 / (self.t[1] - self.t[0])  # Sampling rate from time data
        freqs = np.linspace(0, sample_rate / 2, N // 2)
        
        # Return frequency bins (positive frequencies only) and DFT result
        return freqs, dft_result[:N // 2]  

if __name__ == "__main__":
    app = App()
    app.mainloop()