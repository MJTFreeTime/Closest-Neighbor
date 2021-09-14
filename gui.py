from closest_neighbor import Ui_MainWindow
import main

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        def openUrl(self):
            url = qtc.QUrl('https://github.com/MJTFreeTime')
            if not qtg.QDesktopServices.openUrl(url):
                qtg.QMessageBox.warning(self, 'Open Url', 'Could not open url')
        
        self.ui.github_action.triggered.connect(openUrl)


if __name__ == '__main__':
    app = qtw.QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()