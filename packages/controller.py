from PyQt5.QtCore import QObject


class Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    def set_path(self, file_path):
        self._model.file_path = file_path

    def generate_summary(self):
        self._model.generate_summary()

    def get_player_fee(self, agent_id, agent):
        self._model.get_player_fee(agent_id, agent)
