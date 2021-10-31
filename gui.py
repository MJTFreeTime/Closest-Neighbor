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

        self.conn_error_box = qtw.QMessageBox()
        self.conn_error_box.setIcon(qtw.QMessageBox.Critical)
        self.conn_error_box.setText("ERROR:\n\nA connection could not be not established.")
        self.conn_error_box.setWindowTitle("Connection Error")

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

        global driver, server, user_name, password, database

        # Redirect to Data Connection Options page when cancel is clicked
        self.ui.sql_cancel_button.clicked.connect(self.connectionOptionsPage)
        # Redirect to Table Mapping page when ok is clicked
        self.ui.sql_ok_button.clicked.connect(self.tablePage)

        # Populate SQL Driver ComboBox with pyodbc drivers from main
        self.ui.sql_driver_box.addItems(main.pyodbc_drivers)

        self.ui.sql_test_connection_button.clicked.connect(self.testSQLConnection)
        self.ui.sql_auth_button.clicked.connect(self.useSQLAuth)
        self.ui.windows_auth_button.clicked.connect(self.useWindowsAuth)
        self.ui.set_authentication_button.clicked.connect(self.updateDatabaseList)
        self.ui.sql_ok_button.clicked.connect(self.updateTableList)
        
        ##### ----- CALCULATION PAGE ----- #####
        # Redirect to SQL Connection Manager page when cancel is clicked
        self.ui.table_cancel_button.clicked.connect(self.SQLConnectionPage)


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
        self.ui.main_pages.setCurrentWidget(self.ui.connection_page)

    # Function to switch over to SQL Connection Manager page
    def SQLConnectionPage(self):
        self.ui.main_pages.setCurrentWidget(self.ui.sql_page)

    # Function to switch over to Calculation page
    def tablePage(self):
        self.ui.main_pages.setCurrentWidget(self.ui.table_page)

    def useSQLAuth(self):
        self.ui.user_name_label.setEnabled(True)
        self.ui.user_name_input.setEnabled(True)
        self.ui.password_label.setEnabled(True)
        self.ui.password_input.setEnabled(True)

    def useWindowsAuth(self):
        self.ui.user_name_label.setDisabled(True)
        self.ui.user_name_input.setDisabled(True)
        self.ui.password_label.setDisabled(True)
        self.ui.password_input.setDisabled(True)

    def updateConnDetails(self):
        global driver, server, user_name, password, database
        driver = self.ui.sql_driver_box.currentText()
        server = self.ui.server_name_input.text()
        user_name = self.ui.user_name_input.text()
        password = self.ui.password_input.text()
        database = self.ui.database_name_input.currentText()

    def testSQLConnection(self):
        self.updateConnDetails()
        if main.testConnection(driver, server, user_name, password, database):
            return True
        else:
            return False

    def updateDatabaseList(self):
        self.updateConnDetails()
        if (self.testSQLConnection):
            self.ui.database_name_label.setEnabled(True)
            self.ui.database_name_input.setEnabled(True)
            databases = main.getDatabases(driver, server, user_name, password, database)
            if databases:
                self.ui.database_name_input.clear()
                self.ui.database_name_input.addItems(databases)
        else:
            self.conn_error_box.exec_()

    def updateTableList(self):
        self.updateConnDetails()
        if (self.testSQLConnection):
            tables = main.getTables(driver, server, user_name, password, database)
            if tables:
                self.ui.sql_table_box.clear()
                self.ui.sql_table_box.addItems(tables)
        else:
            self.conn_error_box.exec_()
        

if __name__ == '__main__':
    app = qtw.QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()