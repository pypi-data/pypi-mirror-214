from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from nanoqnt.view import VIEW_FOLDER


class ChannelSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = []
        self.name_channels = ()

        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'channel_selector.ui'), self)

        self.channel_box.setCurrentIndex(0)
        self.update_channels(1)
        self.channel_box.currentIndexChanged.connect(self.update_box)
        self.accept_button.clicked.connect(self.close)

    def update_info(self, number_channels, name_channels):
        """ Simple work around to update the UI of the channel selector after it has been instantiated.
        """
        self.name_channels = name_channels
        self.update_channels(number_channels)
        self.channel_box.setCurrentIndex(number_channels-1)
    def update_box(self, number):
        """ Another bloated solution for a simple problem. There's an indexing missmatch between the number of
        channels and their names.

        TODO: Remove this method
        """
        self.update_channels(number+1)

    def update_channels(self, number):
        """ Updates the UI to display a given number of QLineEdits that allow to change the names of the channels.
        If the names of the channels are available, they'll be used.

        :param int number: The number of QLineEdits to show (one per channel)
        """
        self.channels = []
        layout = self.channels_widget.layout()
        for i in range(layout.rowCount()):
            layout.removeRow(0)

        for i in range(number):
            if len(self.name_channels) == number:
                self.channels.append(QLineEdit(f"{self.name_channels[i]}"))
            else:
                self.channels.append(QLineEdit(f"Name {i+1}"))
            layout.addRow(QLabel(f"Channel {i}"), self.channels[-1])
