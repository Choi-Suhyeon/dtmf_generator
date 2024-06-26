from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.io.wavfile import write
from datetime import datetime
from itertools import repeat

import numpy as np
import subprocess
import sys
import os


class DtmfAnalyzer(QMainWindow):
    __sampling_frequency = 100000
    __duration           = 0.5
    __time_array         = np.linspace(0, __duration, int(__sampling_frequency * __duration))
    __interval_sound     = np.fromiter(repeat(np.int16(0), int(__sampling_frequency * __duration / 4)), dtype=np.int16)
    __dtmf_frequencies   = {
        '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
        '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
        '*': (941, 1209), '0': (941, 1336), '#': (941, 1477),
    }

    __dtmf_signals = dict()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('DTMF Analyzer')
        self.statusBar().showMessage('')
        self.resize(971, 600)
        self.__center()

        self.__central_widget = QWidget(self)
        self.__layout         = QVBoxLayout(self.__central_widget)
        self.__input_field    = QLineEdit(self)
        self.__input_button   = QPushButton('Write', self)
        self.__plot_canvas    = FigureCanvas(Figure(figsize=(5, 6)))

        self.setCentralWidget(self.__central_widget)

        self.__layout.addWidget(self.__input_field)
        self.__layout.addWidget(self.__input_button)
        self.__layout.addWidget(self.__plot_canvas)

        self.__input_field.setPlaceholderText('Enter one or more phone dial numbers')
        self.__input_field.returnPressed.connect(self.__process_input)
        self.__input_button.clicked.connect(self.__process_input)

        self.__ax1 = self.__plot_canvas.figure.add_subplot(211)
        self.__ax2 = self.__plot_canvas.figure.add_subplot(212)

        self.__set_graph1()
        self.__set_graph2()

        self.__plot_canvas.figure.tight_layout()
        self.__plot_canvas.draw()

    @classmethod
    def __get_sin(cls, frequency, *, amplitude=1, time=None, phase=0):
        return amplitude * np.sin(2 * np.pi * frequency * (1 if time is None else time) + phase)

    def __center(self):
        window_frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()

        window_frame.moveCenter(center_point)
        self.move(window_frame.topLeft())

    def __set_graph1(self):
        self.__ax1.clear()
        self.__ax1.set_title('Time-Domain Waveform')
        self.__ax1.set_xlabel('Time (s)')
        self.__ax1.set_ylabel('Amplitude')
        self.__ax1.set_ylim((-2.25, 2.25))
        self.__ax1.grid(True)

    def __set_graph2(self):
        self.__ax2.clear()
        self.__ax2.set_title('Frequency-Domain Waveform')
        self.__ax2.set_xlabel('Frequency (Hz)')
        self.__ax2.set_ylabel('Magnitude')
        self.__ax2.set_xlim((0, 2000))
        self.__ax2.grid(True)

    def __process_input(self):
        text = self.__input_field.text().strip()

        self.__input_field.clear()

        if any(c not in self.__dtmf_frequencies.keys() for c in text):
            self.statusBar().showMessage('Error: illegal phone dial numbers are included')

            return

        self.__dtmf_signals.clear()
        self.__set_graph1()
        self.__set_graph2()

        for c in sorted(set(text)):
            self.__draw_plots(c)

        scaled_concat_wave = np.concatenate([np.int16(0x7FFF * self.__dtmf_signals[c]) if c != '$' else self.__interval_sound for c in '$'.join(text)])
        name_elem_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
        name_elem_nums     = ''.join(text).translate(str.maketrans('*#', 'as'))
        audio_file_name    = f'{name_elem_datetime}_{name_elem_nums}.wav'
        audio_file_path    = os.path.join(os.getcwd(), audio_file_name)

        write(audio_file_name, self.__sampling_frequency, scaled_concat_wave)
        subprocess.run(['start', audio_file_path], shell=True)

        self.statusBar().showMessage('Success: graphs corresponding to the input has been plotted successfully')
        self.__ax2.legend(loc='best', frameon=True)
        self.__plot_canvas.figure.tight_layout()
        self.__plot_canvas.draw()

    def __draw_plots(self, dial_number):
        dtmf_signal      = self.__generate_dtmf_signal(dial_number)
        frequencies      = np.fft.fftfreq(len(dtmf_signal), self.__sampling_frequency ** -1)
        dtmf_fft         = np.fft.fft(dtmf_signal)
        half_frequencies = frequencies[:len(frequencies) >> 1]
        half_dtmf_fft    = dtmf_fft[:len(frequencies) >> 1]

        self.__dtmf_signals[dial_number] = dtmf_signal

        self.__ax1.plot(self.__time_array, dtmf_signal)
        self.__ax2.plot(half_frequencies, np.abs(half_dtmf_fft), label=dial_number)

    def __generate_dtmf_signal(self, dial_num):
        freq1, freq2 = self.__dtmf_frequencies.get(dial_num, (0, 0))
        signal       = self.__get_sin(freq1, time=self.__time_array) + self.__get_sin(freq2, time=self.__time_array)

        return signal


if __name__ == '__main__':
    app      = QApplication(sys.argv)
    analyzer = DtmfAnalyzer()

    analyzer.show()
    sys.exit(app.exec_())
