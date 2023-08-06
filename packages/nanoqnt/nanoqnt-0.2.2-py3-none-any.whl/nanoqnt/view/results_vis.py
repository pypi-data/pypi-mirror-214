import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from nanoqnt.view import VIEW_FOLDER


class DataVis(QMainWindow):
    def __init__(self, analyze_model):
        super().__init__()
        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'data_vis.ui'), self)

        self.analyze_model = analyze_model

        self.histogram_channel_selector.currentIndexChanged.connect(self.update_histogram)
        self.histogram_bins.editingFinished.connect(self.update_histogram)

        self.multi_channel_1.currentIndexChanged.connect(self.update_multi_color)
        self.multi_channel_2.currentIndexChanged.connect(self.update_multi_color)

        # Preparing the histogram figure
        layout = self.histogram_plot_widget.layout()

        self.histogram_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.histogram_ax = self.histogram_canvas.figure.subplots()
        layout.addWidget(NavigationToolbar(self.histogram_canvas, self))
        layout.addWidget(self.histogram_canvas)

        # Preparing the multicolor figure
        multi_layout = self.multi_color_plot_widget.layout()
        self.multi_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.multi_ax = self.multi_canvas.figure.subplots()
        multi_layout.addWidget(NavigationToolbar(self.multi_canvas, self))
        multi_layout.addWidget(self.multi_canvas)
    def prepare_histograms_tab(self):
        self.histogram_channel_selector.clear()
        for channel_name in self.analyze_model.channels_names:
            self.histogram_channel_selector.addItem(str(channel_name))

    def prepare_multicolor_tab(self):
        self.multi_channel_1.clear()
        self.multi_channel_2.clear()
        for channel_name in self.analyze_model.channels_names:
            self.multi_channel_1.addItem(str(channel_name))
            self.multi_channel_2.addItem(str(channel_name))
    def update_histogram(self, *args):
        bins = int(self.histogram_bins.text())
        channel_number = self.histogram_channel_selector.currentIndex()
        channel_name = self.analyze_model.channels_names[channel_number]
        t1 = self.analyze_model.summary_data[channel_number]
        self.histogram_ax.cla()
        self.histogram_ax.hist(t1[f'i_{channel_number}'], bins=bins)
        self.histogram_ax.set_xlabel('Total Intensity (counts)')
        self.histogram_ax.set_ylabel('Number of particles')
        self.histogram_ax.set_title(f'Channel: {channel_name}')
        self.histogram_canvas.draw_idle()

    def update_multi_color(self, *args):
        channel_1 = self.multi_channel_1.currentIndex()
        channel_2 = self.multi_channel_2.currentIndex()
        self.multi_ax.cla()
        self.multi_ax.plot(self.analyze_model.summary_data[channel_1][f'i_{channel_1}'],
                        self.analyze_model.summary_data[channel_1][f'i_{channel_2}'],
                        'o',
                        alpha=0.1)
        self.multi_ax.set_xlabel(self.analyze_model.channels_names[channel_1], fontsize=14)
        self.multi_ax.set_ylabel(self.analyze_model.channels_names[channel_2], fontsize=14)
        self.multi_canvas.draw_idle()

    def prepare_summary_info(self):
        info = self.analyze_model.generate_info_summary()
        self.summary_data_text.setPlainText(info)

    def show(self):
        self.prepare_histograms_tab()
        self.prepare_multicolor_tab()
        self.prepare_summary_info()
        super().show()