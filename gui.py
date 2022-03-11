import time
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

		global connString, driver, server, user_name, password, database, table, timeout
		connString = driver = server = user_name = password = database = table = False
		timeout = 1

		# Redirect to Data Connection Options page when cancel is clicked
		self.ui.sql_cancel_button.clicked.connect(self.connectionOptionsPage)
		# Redirect to Table Mapping page when ok is clicked
		self.ui.sql_ok_button.clicked.connect(self.tablePage)

		# Populate SQL Driver ComboBox with pyodbc drivers from main
		self.ui.sql_driver_box.addItems(main.pyodbc_drivers)
		
		self.ui.sql_auth_button.clicked.connect(self.useSQLAuth)
		self.ui.windows_auth_button.clicked.connect(self.useWindowsAuth)
		self.ui.set_authentication_button.clicked.connect(self.updateDatabaseList)
		self.ui.sql_ok_button.clicked.connect(self.updateTableList)

		##### ----- TABLE MAPPING PAGE ----- #####
		# Redirect to SQL Connection Manager page when cancel is clicked
		self.ui.table_cancel_button.clicked.connect(self.SQLConnectionPage)
		self.ui.sql_table_box.currentIndexChanged.connect(self.updateColumnList)


	################################################
	#                                              #
	#                   FUNCTIONS                  #
	#                                              #
	################################################

	##### ----- TOP NAV ----- #####
	def openUrl(self):
		url = qtc.QUrl('https://github.com/mjt-21/Closest-Neighbor')
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
		global connString, driver, server, user_name, password, database, table, timeout

		driver = self.ui.sql_driver_box.currentText()
		server = self.ui.server_name_input.text()
		user_name = self.ui.user_name_input.text()
		password = self.ui.password_input.text()
		database = self.ui.database_name_input.currentText()
		table = self.ui.sql_table_box.currentText()

		# Only update connection string variable if all NECESSARY variables are defined (are not False)
		if (driver and server and timeout):
			if (user_name or password):
				connString = "DRIVER={" + driver + "};" + "SERVER=" + server + ";DATABASE=" + database + ";UID=" + user_name + ";PWD=" + password + ";TRUSTED_CONNECTION=no"
			else:
				connString = "DRIVER={" + driver + "};" + "SERVER=" + server + ";DATABASE=" + database + ";TRUSTED_CONNECTION=yes"

	def testSQLConnection(self):
		if (main.testConnection(connString, timeout)):
			return True
		else:
			self.conn_error_box.exec()
			return False

	def updateDatabaseList(self):
		self.updateConnDetails()

		databases = main.getDatabases(connString, timeout)
		self.ui.database_name_input.clear()

		if databases == 1:
			self.conn_error_box.exec()
			self.ui.database_name_label.setDisabled(True)
			self.ui.database_name_input.setDisabled(True)
		else:
			self.ui.database_name_label.setEnabled(True)
			self.ui.database_name_input.setEnabled(True)
			self.ui.database_name_input.addItems(databases)

	def updateTableList(self):
		self.updateConnDetails()

		tables = main.getTables(connString, database, timeout)

		self.ui.sql_table_box.clear()

		if tables == 1:
			self.conn_error_box.exec()
		else:
			self.ui.sql_table_box.addItems(tables)

	def updateColumnList(self):
		self.updateConnDetails()

		columns = main.getColumns(connString, table, timeout)

		self.ui.uid_column_box.clear()
		self.ui.latitude_column_box.clear()
		self.ui.longitude_column_box.clear()

		if columns == 1:
			self.conn_error_box.exec()
		else:
			self.ui.uid_column_box.addItems(columns)
			self.ui.latitude_column_box.addItems(columns)
			self.ui.longitude_column_box.addItems(columns)
			
		

if __name__ == '__main__':
	app = qtw.QApplication([])

	mainWindow = MainWindow()
	mainWindow.show()

	app.exec()