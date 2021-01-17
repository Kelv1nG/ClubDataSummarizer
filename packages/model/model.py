from PyQt5.QtCore import QObject, pyqtSignal
from packages.model.overall import Overall
import pandas as pd


class Model(QObject):
    file_path_signal = pyqtSignal(str)
    agent_fee_signal = pyqtSignal(pd.DataFrame)
    player_fee_signal = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self._file_path = None
        self._overall = None

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path
        self.file_path_signal.emit(self._file_path)

    @property
    def overall(self):
        return self._overall

    @overall.setter
    def overall(self, overall):
        self._overall = overall

    def generate_summary(self):
        self.overall = Overall(self.file_path)
        self.agent_fee_signal.emit(self.overall.agent_fee)

    def get_player_fee(self, agent_id, agent):
        df = self.overall.data

        player_filter = (df['agent_id'] == int(agent_id)) & (df['agent'] == agent)
        df = df.loc[player_filter]

        df.loc[:, 'player_id'] = df['player_id'].astype(int)
        df = df[['player_id', 'nickname', 'player_winnings:overall', 'club_earnings:fee']]
        df.sort_values(by='club_earnings:fee', ascending=False, inplace=True)
        self.player_fee_signal.emit(df)