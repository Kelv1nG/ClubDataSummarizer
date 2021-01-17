from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
from packages.model.model import Model
from packages.controller import Controller
from packages.view import View
import logging
import os

except_hook = sys.excepthook


def exception_hook(exc_type, value, traceback):
	except_hook(exc_type, value, traceback)


class DataSummarizer(object):
	def __init__(self):
		self._model = Model()
		self._controller = Controller(self._model)
		self._view = View(self._model, self._controller)

	def show(self):
		self._view.show()


def run():
	sys.excepthook = exception_hook
	app = QApplication(sys.argv)
	window = DataSummarizer()
	window.show()
	sys.exit(app.exec())

