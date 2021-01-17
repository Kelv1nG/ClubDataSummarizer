from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QTableView
from PyQt5 import QtCore


def get_file_path():
    file_path = QFileDialog.getOpenFileName()[0]
    return file_path


def display_table(widget, df):
    """
    :param widget: pyqt5.TableWidget
    :param df: pandas dataframe
    :return: None, displays df in widget
    """
    rows, cols = df.shape[0], df.shape[1]

    widget.setRowCount(0)
    widget.setColumnCount(cols)

    for row in range(0, rows):
        widget.insertRow(row)
        for col in range(0, cols):
            item = QTableWidgetItem()
            try:
                item.setData(QtCore.Qt.EditRole, int(df.iloc[row, col]))
            except ValueError:
                item.setData(QtCore.Qt.EditRole, str(df.iloc[row, col]))
            finally:
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                widget.setItem(row, col, item)
    widget.setHorizontalHeaderLabels(df.columns)
    widget.setSelectionBehavior(QTableView.SelectRows)
    widget.setSortingEnabled(True)


def get_agent_details_from_table(widget, row):
    agent_id = widget.item(row, 0).text()
    agent = widget.item(row, 1) .text()

    return agent_id, agent










