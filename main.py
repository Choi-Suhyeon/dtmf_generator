from scipy.io.wavfile import write

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os


dtmf_frequencies = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477),
}


def get_sin_wave(amplitude, frequency, time, phase):
    return amplitude * np.sin(2 * np.pi * frequency * time + phase)


if __name__ == '__main__':
    sampling_frequency = 100000
    duration           = 0.5
    time_array         = np.linspace(0, duration, int(sampling_frequency * duration))
    f1, f2             = dtmf_frequencies['2']
    dtmf_signal        = get_sin_wave(1, f1, time_array, 0) + get_sin_wave(1, f2, time_array, 0)
    frequencies        = np.fft.fftfreq(len(dtmf_signal), sampling_frequency ** -1)
    dtmf_fft           = np.fft.fft(dtmf_signal)
    half_frequencies   = frequencies[:len(frequencies) >> 1]
    half_dtmf_fft      = dtmf_fft[:len(frequencies) >> 1]
    fig, axes          = plt.subplots(2, 1, figsize=(12, 8))
    scaled_wave        = np.int16(dtmf_signal * 0x7FFF)
    audio_file_name    = 'dtmf.wav'

    axes[0].plot(time_array, dtmf_signal)
    axes[0].set_title('Time-Domain Waveform')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Amplitude')
    axes[0].grid(True)

    axes[1].plot(half_frequencies, np.abs(half_dtmf_fft))
    axes[1].set_title('Frequency-Domain Waveform')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Magnitude')
    axes[1].set_xlim((0, 2000))
    axes[1].grid(True)

    write(audio_file_name, sampling_frequency, scaled_wave)
    subprocess.run(['start', os.path.join(os.getcwd(), audio_file_name)], shell=True)

    plt.tight_layout()
    plt.show()
