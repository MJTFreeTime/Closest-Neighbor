from closest_neighbor import Ui_MainWindow
import main

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):

        ################################################
        #                                              #
        #             WINDOW INITIALIZATION            #
        #                                              #
        ################################################

        super().__init__(*args, **kwargs)

        ##### ----- MAIN WINDOW ----- #####
        # Initialize main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Closest Neighbor")
        self.setFixedSize(800, 600) 

        # Start application on connection options page
        self.connectionOptionsPage()

        ################################################
        #                                              #
        #                    EVENTS                    #
        #                                              #
        ################################################

        ##### ----- TOP NAV ----- #####

        # Link github_action button to project's GitHub page
        self.ui.github_action.triggered.connect(self.openUrl)

        ##### ----- DATA CONNECTION OPTIONS PAGE ----- #####

        # Redirect to SQL Connection Manager page when SQL is chosen
        self.ui.sql_option_button.clicked.connect(self.SQLConnectionPage)

        ##### ----- SQL CONNECTION MANAGER PAGE ----- #####

        # Redirect to Data Connection Options page when cancel is clicked
        self.ui.sql_cancel_button.clicked.connect(self.connectionOptionsPage)

    ################################################
    #                                              #
    #                   FUNCTIONS                  #
    #                                              #
    ################################################

    ##### ----- TOP NAV ----- #####
    def openUrl(self):
        url = qtc.QUrl('https://github.com/MJTFreeTime/Closest-Neighbor')
        if not qtg.QDesktopServices.openUrl(url):
            qtg.QMessageBox.warning(self, 'Open Url', 'Could not open url')

    # Function to switch over to Data Connection Options page
    def connectionOptionsPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.connection_page)

    # Function to switch over to SQL Connection Manager page
    def SQLConnectionPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.sql_page)


if __name__ == '__main__':
    app = qtw.QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()