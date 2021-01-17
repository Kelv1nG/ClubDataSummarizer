from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import uic
from packages.common.WidgetFuncs import get_file_path, display_table, get_agent_details_from_table

import pandas as pd


class View(QObject):
    def __init__(self, model, controller):
        super().__init__()
        self._model = model
        self._controller = controller
        self._ui = QMainWindow()
        uic.loadUi(r'.\packages\resources\DataSummarizer.ui', self._ui)
        self._ui.setWindowTitle('ClubSummarizer')

        # button connections
        self._ui.btn_get_file_path.clicked.connect(self.get_file_path)
        self._ui.btn_generate_summary.clicked.connect(self.generate_summary)

        # listen for model connections
        self._model.file_path_signal.connect(self.display_file_path)
        self._model.agent_fee_signal.connect(self.display_agent_fee)
        self._model.player_fee_signal.connect(self.display_player_fee)

    def get_file_path(self):
        file_path = get_file_path()
        self._controller.set_path(file_path)

    def generate_summary(self):
        self._controller.generate_summary()

    @pyqtSlot(str)
    def display_file_path(self, path):
        self._ui.file_path.setText(path)

    @pyqtSlot(pd.DataFrame)
    def display_agent_fee(self, df):
        display_table(self._ui.table_agent_fee, df)
        self._ui.table_agent_fee.cellDoubleClicked.connect(self.get_agent_details)

    @pyqtSlot(int, int)
    def get_agent_details(self, row, col):
        agent_id, agent = get_agent_details_from_table(self._ui.table_agent_fee, row)
        self._controller.get_player_fee(agent_id, agent)

    @pyqtSlot(pd.DataFrame)
    def display_player_fee(self, df):
        display_table(self._ui.table_player_fee, df)

    def show(self):
        self._ui.show()

